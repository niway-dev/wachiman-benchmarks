#!/usr/bin/env bash
# bench.sh - set up, run and collect a code-review benchmark on replayed kaipu-record PRs.
#
#   bench.sh create <wachi|pullfrog|coderabbit> <repo-name> [manifest]
#   bench.sh open <repo-name> [manifest]
#   bench.sh rounds <repo-name> <k...>
#   bench.sh collect <repo-name> <out-dir> [label]
#
# Add --dry-run anywhere to print every gh/git command instead of running it.
# Details: docs/benchmark/replay/README.md. bash 3.2 compatible (macOS default).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_MANIFEST="${BENCH_MANIFEST:-${SCRIPT_DIR}/manifest-2026-10-31.tsv}"

OWNER="niway-dev"
SOURCE_REPO="niway-dev/kaipu-record"
CLONE="${KAIPU_CLONE:-/tmp/kaipu-mine/repo}"
# pullfrog.yml is read from this ref of the clone (it is not in older checkouts).
PULLFROG_REF="${KAIPU_PULLFROG_REF:-origin/main}"
SSH_HOST="github-csdev"
GH_LOGIN="csdev19"
GIT_EMAIL="cristiansotomayor.dev@gmail.com"
GIT_NAME="${BENCH_GIT_NAME:-$(git config --get user.name 2>/dev/null || true)}"
if [ -z "${GIT_NAME}" ]; then GIT_NAME="Cristian Sotomayor"; fi
# Workflows that arrive with the replayed commits and must not run next to the reviewer under test.
DISABLE_WORKFLOWS="agent-review.yml pr-checks.yml"
WAIT_SECONDS=90
METHOD_URL="https://github.com/niway-dev/wachiman/tree/main/docs/benchmark"
BENCH_URL="https://github.com/niway-dev/wachiman/blob/main/docs/benchmark/replay/bench.sh"

DRY_RUN=0
TMP_WORK=""
M_COUNT=0
M_N=()
M_BASE=()
M_HEAD=()
M_TITLE=()
NEW_PR_NUM=""

trap 'if [ -n "${TMP_WORK}" ]; then rm -rf "${TMP_WORK}"; fi' EXIT

# ---------------------------------------------------------------- output helpers

die() { printf 'bench.sh: error: %s\n' "$*" >&2; exit 1; }
warn() { printf 'bench.sh: warning: %s\n' "$*" >&2; }
step() { printf '\n==> %s\n' "$*"; }
note() { printf '    %s\n' "$*"; }

usage() {
  cat <<'EOF'
Usage:
  bench.sh create <wachi|pullfrog|coderabbit> <repo-name> [manifest]
  bench.sh open <repo-name> [manifest]
  bench.sh rounds <repo-name> <k...>
  bench.sh collect <repo-name> <out-dir> [label]

  --dry-run   print every gh/git command instead of running it (anywhere in the arguments)

<repo-name> is niway-dev/<repo-name>, normally kaipu-bench-<reviewer>[-vN]; open, rounds and
collect infer the reviewer from it. [manifest] defaults to manifest-2026-10-31.tsv next to this
script (or $BENCH_MANIFEST). Environment: KAIPU_CLONE (kaipu-record clone, default
/tmp/kaipu-mine/repo), KAIPU_PULLFROG_REF (ref holding pullfrog.yml, default origin/main).
EOF
}

usage_die() { printf 'bench.sh: usage: bench.sh %s\n' "$*" >&2; exit 2; }

# Quote one argument for display. Multi-line arguments (PR bodies) show their first line only.
quote_arg() {
  local a="$1" first esc
  case "${a}" in
    *$'\n'*)
      first="${a%%$'\n'*}"
      esc="${first//\'/\'\\\'\'}"
      printf "'%s [...]'" "${esc}"
      return 0
      ;;
    "") printf "''"; return 0 ;;
    *[!A-Za-z0-9_./:@%+=,-]*)
      esc="${a//\'/\'\\\'\'}"
      printf "'%s'" "${esc}"
      return 0
      ;;
  esac
  printf '%s' "${a}"
}

show_cmd() {
  local out="+" a
  for a in "$@"; do
    out="${out} $(quote_arg "${a}")"
  done
  printf '%s\n' "${out}"
}

# Run a command, or only print it under --dry-run.
x() {
  if [ "${DRY_RUN}" = 1 ]; then
    show_cmd "$@"
  else
    "$@"
  fi
}

# ---------------------------------------------------------------- shared helpers

valid_reviewer() {
  case "$1" in
    wachi|pullfrog|coderabbit) return 0 ;;
    *) return 1 ;;
  esac
}

reviewer_label() {
  case "$1" in
    wachi) printf 'Wachi Reviewer' ;;
    pullfrog) printf 'Pullfrog' ;;
    coderabbit) printf 'CodeRabbit' ;;
  esac
}

# kaipu-bench-<reviewer>[-vN] -> <reviewer>
reviewer_of() {
  local repo="$1" r
  case "${repo}" in
    kaipu-bench-*) r="${repo#kaipu-bench-}" ;;
    *) die "cannot infer the reviewer from '${repo}': expected kaipu-bench-<wachi|pullfrog|coderabbit>[-vN]" ;;
  esac
  r="${r%%-v[0-9]*}"
  if ! valid_reviewer "${r}"; then
    die "cannot infer the reviewer from '${repo}': '${r}' is not wachi, pullfrog or coderabbit"
  fi
  printf '%s' "${r}"
}

check_repo_name() {
  case "$1" in
    ""|*[!A-Za-z0-9._-]*) die "invalid repository name: '$1'" ;;
  esac
}

git_url() { printf 'git@%s:%s/%s.git' "${SSH_HOST}" "${OWNER}" "$1"; }

# The gh account must be the csdev one (see ~/GITHUB_ACCOUNTS.md); never switch it silently.
preflight_gh() {
  local login
  if [ "${DRY_RUN}" = 1 ]; then
    show_cmd gh api --hostname github.com user --jq .login
    note "(must print ${GH_LOGIN})"
    return 0
  fi
  login="$(gh api --hostname github.com user --jq .login)"
  if [ "${login}" != "${GH_LOGIN}" ]; then
    die "gh is logged in as '${login}', expected '${GH_LOGIN}'. Run: gh auth switch --hostname github.com --user ${GH_LOGIN}"
  fi
}

# Fill M_* from a manifest: PR number, base SHA, head SHA, title (tab-separated).
load_manifest() {
  local file="$1" n base head title lineno=0 re='^[0-9a-f]{40}$'
  [ -f "${file}" ] || die "manifest not found: ${file}"
  M_COUNT=0
  M_N=()
  M_BASE=()
  M_HEAD=()
  M_TITLE=()
  while IFS=$'\t' read -r n base head title || [ -n "${n}" ]; do
    lineno=$((lineno + 1))
    case "${n}" in
      ""|"#"*) continue ;;
    esac
    case "${n}" in
      *[!0-9]*) die "${file}:${lineno}: PR number '${n}' is not a number" ;;
    esac
    [[ ${base} =~ $re ]] || die "${file}:${lineno}: base '${base}' is not a 40-character SHA"
    [[ ${head} =~ $re ]] || die "${file}:${lineno}: head '${head}' is not a 40-character SHA"
    [ -n "${title}" ] || die "${file}:${lineno}: missing title"
    M_N[M_COUNT]="${n}"
    M_BASE[M_COUNT]="${base}"
    M_HEAD[M_COUNT]="${head}"
    M_TITLE[M_COUNT]="${title}"
    M_COUNT=$((M_COUNT + 1))
  done < "${file}"
  if [ "${M_COUNT}" -eq 0 ]; then die "manifest has no rows: ${file}"; fi
}

# Every SHA in the manifest must exist in the kaipu-record clone before anything is pushed.
check_clone() {
  local i
  if [ ! -d "${CLONE}/.git" ] && [ ! -f "${CLONE}/HEAD" ]; then
    if [ "${DRY_RUN}" = 1 ]; then
      warn "kaipu-record clone not found at ${CLONE}; skipping the commit check (dry run)"
      return 0
    fi
    die "kaipu-record clone not found at ${CLONE} (set KAIPU_CLONE)"
  fi
  i=0
  while [ "${i}" -lt "${M_COUNT}" ]; do
    git -C "${CLONE}" cat-file -e "${M_BASE[$i]}^{commit}" 2>/dev/null \
      || die "base ${M_BASE[$i]} of PR ${M_N[$i]} is not in ${CLONE}; fetch it first"
    git -C "${CLONE}" cat-file -e "${M_HEAD[$i]}^{commit}" 2>/dev/null \
      || die "head ${M_HEAD[$i]} of PR ${M_N[$i]} is not in ${CLONE}; fetch it first"
    i=$((i + 1))
  done
}

ensure_label() {
  x gh label create replay -R "${OWNER}/$1" --color 5319e7 \
    --description "Replayed kaipu-record pull request; never merged" --force
}

# Print the number of an open PR from <head> into <base>, or nothing.
open_pr_number() {
  gh pr list -R "${OWNER}/$1" --state open --base "$2" --head "$3" --json number --jq '.[0].number // empty'
}

# Create a labelled replay PR; sets NEW_PR_NUM.
create_replay_pr() {
  local repo="$1" base="$2" head="$3" title="$4" body="$5" url
  if [ "${DRY_RUN}" = 1 ]; then
    show_cmd gh pr create -R "${OWNER}/${repo}" --base "${base}" --head "${head}" --label replay \
      --title "${title}" --body "${body}"
    NEW_PR_NUM="<new-pr-number>"
    return 0
  fi
  url="$(gh pr create -R "${OWNER}/${repo}" --base "${base}" --head "${head}" --label replay \
    --title "${title}" --body "${body}")"
  NEW_PR_NUM="${url##*/}"
}

original_body() {
  if [ "${DRY_RUN}" = 1 ]; then
    show_cmd gh pr view "$1" -R "${SOURCE_REPO}" --json body --jq .body >&2
    printf '<original description of %s#%s>' "${SOURCE_REPO}" "$1"
    return 0
  fi
  gh pr view "$1" -R "${SOURCE_REPO}" --json body --jq .body
}

# Ask the reviewer under test to start (nothing for Pullfrog, which runs when the PR opens).
trigger_review() {
  local reviewer="$1" repo="$2" num="$3"
  case "${reviewer}" in
    wachi) x gh pr comment "${num}" -R "${OWNER}/${repo}" --body "/wachi review" ;;
    coderabbit) x gh pr comment "${num}" -R "${OWNER}/${repo}" --body "@coderabbitai review" ;;
    pullfrog) note "Pullfrog starts on its own when the PR opens" ;;
  esac
}

# ---------------------------------------------------------------- create

write_readme() {
  local dst="$1" reviewer="$2" repo="$3" manifest="$4"
  if [ "${DRY_RUN}" = 1 ]; then
    note "# write ${dst} (repo-README.md under a header naming ${OWNER}/${repo})"
    return 0
  fi
  {
    # shellcheck disable=SC2016 # backticks are literal Markdown
    printf '> **This repository:** `%s/%s` · **Reviewer:** %s · **Replay manifest:** `%s` · set up with [`bench.sh`](%s)\n\n' \
      "${OWNER}" "${repo}" "$(reviewer_label "${reviewer}")" "$(basename "${manifest}")" "${BENCH_URL}"
    cat "${SCRIPT_DIR}/repo-README.md"
  } > "${dst}"
}

# Copy a file into the work tree (creating its directory).
put_file() {
  local src="$1" dst="$2"
  if [ "${DRY_RUN}" = 1 ]; then
    note "# copy ${src} -> ${dst}"
    return 0
  fi
  mkdir -p "$(dirname "${dst}")"
  cp "${src}" "${dst}"
}

build_main() {
  local reviewer="$1" repo="$2" manifest="$3" url work msg src_sha
  url="$(git_url "${repo}")"
  if [ "${DRY_RUN}" = 1 ]; then
    work="<tmpdir>"
    note "# mktemp -d (a throwaway work tree for the single main commit)"
  else
    TMP_WORK="$(mktemp -d "${TMPDIR:-/tmp}/bench-main.XXXXXX")"
    work="${TMP_WORK}"
  fi
  x git -C "${work}" init -q
  x git -C "${work}" symbolic-ref HEAD refs/heads/main
  x git -C "${work}" config user.email "${GIT_EMAIL}"
  x git -C "${work}" config user.name "${GIT_NAME}"
  write_readme "${work}/README.md" "${reviewer}" "${repo}" "${manifest}"
  msg="chore: ${reviewer} benchmark repository"
  case "${reviewer}" in
    wachi)
      put_file "${SCRIPT_DIR}/wachi-workflow.yml" "${work}/.github/workflows/wachi-bench.yml"
      ;;
    pullfrog)
      if [ "${DRY_RUN}" = 1 ]; then
        show_cmd git -C "${CLONE}" show "${PULLFROG_REF}:.github/workflows/pullfrog.yml"
        note "# write the output to ${work}/.github/workflows/pullfrog.yml"
        src_sha="<sha of ${PULLFROG_REF}>"
      else
        git -C "${CLONE}" cat-file -e "${PULLFROG_REF}:.github/workflows/pullfrog.yml" 2>/dev/null \
          || die "no .github/workflows/pullfrog.yml at ${PULLFROG_REF} in ${CLONE} (set KAIPU_PULLFROG_REF)"
        mkdir -p "${work}/.github/workflows"
        git -C "${CLONE}" show "${PULLFROG_REF}:.github/workflows/pullfrog.yml" \
          > "${work}/.github/workflows/pullfrog.yml"
        src_sha="$(git -C "${CLONE}" rev-parse "${PULLFROG_REF}")"
      fi
      msg="${msg}

pullfrog.yml copied unchanged from ${SOURCE_REPO}@${src_sha}"
      ;;
    coderabbit) ;;
  esac
  x git -C "${work}" add -A
  x git -C "${work}" commit -q -m "${msg}"
  x git -C "${work}" push -q "${url}" main
  if [ "${DRY_RUN}" = 1 ]; then
    note "# rm -rf ${work}"
  else
    rm -rf "${TMP_WORK}"
    TMP_WORK=""
  fi
}

# Push replay/pr-<n>/{base,head} for every manifest row, then check the remote SHAs.
push_replays() {
  local repo="$1" url i refs=() expected
  url="$(git_url "${repo}")"
  i=0
  while [ "${i}" -lt "${M_COUNT}" ]; do
    refs+=("${M_BASE[$i]}:refs/heads/replay/pr-${M_N[$i]}/base" "${M_HEAD[$i]}:refs/heads/replay/pr-${M_N[$i]}/head")
    i=$((i + 1))
  done
  x git -C "${CLONE}" push -q "${url}" "${refs[@]}"
  if [ "${DRY_RUN}" = 1 ]; then
    show_cmd git ls-remote "${url}" 'refs/heads/replay/*'
    note "(every pushed branch must report the SHA from the manifest)"
    return 0
  fi
  expected="$(git ls-remote "${url}" 'refs/heads/replay/*')"
  i=0
  while [ "${i}" -lt "${M_COUNT}" ]; do
    printf '%s\n' "${expected}" | grep -qxF "$(printf '%s\trefs/heads/replay/pr-%s/base' "${M_BASE[$i]}" "${M_N[$i]}")" \
      || die "replay/pr-${M_N[$i]}/base is not at ${M_BASE[$i]} on ${repo}"
    printf '%s\n' "${expected}" | grep -qxF "$(printf '%s\trefs/heads/replay/pr-%s/head' "${M_HEAD[$i]}" "${M_N[$i]}")" \
      || die "replay/pr-${M_N[$i]}/head is not at ${M_HEAD[$i]} on ${repo}"
    i=$((i + 1))
  done
  note "all $((M_COUNT * 2)) replay branches are at the manifest SHAs"
}

# Register the replayed commits' own workflows, then disable them (see README: why).
neutralize_replayed_workflows() {
  local repo="$1" setup_num paths waited=0 f missing registered
  step "Open a draft setup PR so GitHub registers the replayed workflows"
  create_setup_pr "${repo}"
  setup_num="${NEW_PR_NUM}"

  step "Disable the replayed workflows (${DISABLE_WORKFLOWS})"
  if [ "${DRY_RUN}" = 1 ]; then
    show_cmd gh workflow list -R "${OWNER}/${repo}" --all --limit 100 --json path --jq '.[].path'
    note "(polled every 5 s for up to ${WAIT_SECONDS} s until all of them are listed; continues if they never appear)"
    for f in ${DISABLE_WORKFLOWS}; do
      show_cmd gh workflow disable "${f}" -R "${OWNER}/${repo}"
    done
  else
    while :; do
      paths="$(gh workflow list -R "${OWNER}/${repo}" --all --limit 100 --json path --jq '.[].path' 2>/dev/null || true)"
      missing=""
      for f in ${DISABLE_WORKFLOWS}; do
        case "${paths}" in
          *".github/workflows/${f}"*) ;;
          *) missing="${missing} ${f}" ;;
        esac
      done
      if [ -z "${missing}" ]; then break; fi
      if [ "${waited}" -ge "${WAIT_SECONDS}" ]; then
        warn "after ${WAIT_SECONDS} s GitHub has not registered:${missing}"
        break
      fi
      sleep 5
      waited=$((waited + 5))
    done
    for f in ${DISABLE_WORKFLOWS}; do
      registered=0
      case "${paths}" in
        *".github/workflows/${f}"*) registered=1 ;;
      esac
      if [ "${registered}" = 1 ]; then
        gh workflow disable "${f}" -R "${OWNER}/${repo}"
        note "disabled ${f}"
      else
        warn "${f} is not registered; disable it by hand under Actions before adding any API key secret"
      fi
    done
  fi

  step "Close the setup PR"
  x gh pr close "${setup_num}" -R "${OWNER}/${repo}" \
    --comment "Setup only: the replayed workflows are registered and disabled. Never merged."
}

create_setup_pr() {
  local repo="$1" url
  local base="replay/pr-${M_N[0]}/base" head="replay/pr-${M_N[0]}/head"
  local title="[setup] register and disable the replayed workflows (closed, never merged)"
  local body="Setup only. Opening any replay pair makes GitHub register the workflow files that arrive with the replayed commits (\`agent-review.yml\`, \`pr-checks.yml\`) so they can be disabled before an API key secret exists. This PR is closed right after."
  if [ "${DRY_RUN}" = 1 ]; then
    show_cmd gh pr create -R "${OWNER}/${repo}" --draft --base "${base}" --head "${head}" \
      --title "${title}" --body "${body}"
    NEW_PR_NUM="<setup-pr-number>"
    return 0
  fi
  url="$(gh pr create -R "${OWNER}/${repo}" --draft --base "${base}" --head "${head}" \
    --title "${title}" --body "${body}")"
  NEW_PR_NUM="${url##*/}"
}

cmd_create() {
  if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then usage_die "create <wachi|pullfrog|coderabbit> <repo-name> [manifest]"; fi
  local reviewer="$1" repo="$2" manifest="${3:-${DEFAULT_MANIFEST}}" inferred
  valid_reviewer "${reviewer}" || die "unknown reviewer '${reviewer}': use wachi, pullfrog or coderabbit"
  check_repo_name "${repo}"
  case "${repo}" in
    kaipu-bench-*)
      inferred="$(reviewer_of "${repo}")"
      if [ "${inferred}" != "${reviewer}" ]; then
        die "repository '${repo}' reads as a ${inferred} repository but the reviewer is ${reviewer}"
      fi
      ;;
  esac
  load_manifest "${manifest}"
  check_clone
  preflight_gh

  step "Create ${OWNER}/${repo} (public)"
  x gh repo create "${OWNER}/${repo}" --public \
    --description "Code-review benchmark: replayed ${SOURCE_REPO} pull requests reviewed by $(reviewer_label "${reviewer}")"

  step "Build main as one fresh commit (reviewer files: ${reviewer})"
  build_main "${reviewer}" "${repo}" "${manifest}"

  step "Push the replay branches (${M_COUNT} pairs from ${manifest##*/})"
  push_replays "${repo}"

  neutralize_replayed_workflows "${repo}"

  step "Done"
  note "The setup PR took #1, so the benchmark PRs of this repository start at #2."
  print_setup_links "${reviewer}" "${repo}"
}

print_setup_links() {
  local reviewer="$1" repo="$2"
  printf '\nNext steps for the repository owner (not automated):\n'
  printf '  1. GitHub App access (Pullfrog / CodeRabbit: add this repository to the app):\n'
  printf '     https://github.com/organizations/%s/settings/installations\n' "${OWNER}"
  case "${reviewer}" in
    wachi|pullfrog)
      printf '  2. Repository secret ANTHROPIC_API_KEY:\n'
      printf '     https://github.com/%s/%s/settings/secrets/actions\n' "${OWNER}" "${repo}"
      ;;
    coderabbit)
      printf '  2. Enable the repository in CodeRabbit:\n'
      printf '     https://app.coderabbit.ai/settings/repositories\n'
      ;;
  esac
  printf '  Then open the replays:  bench.sh open %s\n' "${repo}"
}

# ---------------------------------------------------------------- open

preamble_open() {
  # shellcheck disable=SC2016 # backticks are literal Markdown
  printf '> **Replay of [%s#%s](https://github.com/%s/pull/%s)** for the code-review benchmark. Base `%s`, head `%s`: the same commits the original reviewers saw, so the diff is byte-identical. Never merged. Method and scoring: [wachiman/docs/benchmark](%s). The original description follows.' \
    "${SOURCE_REPO}" "$1" "${SOURCE_REPO}" "$1" "${2:0:7}" "${3:0:7}" "${METHOD_URL}"
}

cmd_open() {
  if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then usage_die "open <repo-name> [manifest]"; fi
  local repo="$1" manifest="${2:-${DEFAULT_MANIFEST}}" reviewer i existing orig body
  check_repo_name "${repo}"
  reviewer="$(reviewer_of "${repo}")"
  load_manifest "${manifest}"
  preflight_gh

  step "Open the replay PRs in ${OWNER}/${repo} (${reviewer})"
  ensure_label "${repo}"
  i=0
  while [ "${i}" -lt "${M_COUNT}" ]; do
    existing=""
    if [ "${DRY_RUN}" = 1 ]; then
      show_cmd gh pr list -R "${OWNER}/${repo}" --state open --base "replay/pr-${M_N[$i]}/base" \
        --head "replay/pr-${M_N[$i]}/head" --json number --jq '.[0].number // empty'
    else
      existing="$(open_pr_number "${repo}" "replay/pr-${M_N[$i]}/base" "replay/pr-${M_N[$i]}/head")"
    fi
    if [ -n "${existing}" ]; then
      note "kaipu#${M_N[$i]}: already open as #${existing}, skipped (no new trigger)"
    else
      orig="$(original_body "${M_N[$i]}")"
      body="$(preamble_open "${M_N[$i]}" "${M_BASE[$i]}" "${M_HEAD[$i]}")

---

${orig}"
      create_replay_pr "${repo}" "replay/pr-${M_N[$i]}/base" "replay/pr-${M_N[$i]}/head" \
        "[replay] ${M_TITLE[$i]}" "${body}"
      note "kaipu#${M_N[$i]} -> #${NEW_PR_NUM}"
      trigger_review "${reviewer}" "${repo}" "${NEW_PR_NUM}"
    fi
    i=$((i + 1))
  done
  x gh pr list -R "${OWNER}/${repo}" --label replay --json number,title --jq '.[] | "#\(.number) \(.title)"'
}

# ---------------------------------------------------------------- rounds

preamble_round() {
  # shellcheck disable=SC2016 # backticks are literal Markdown
  printf '> **Replay of [%s#%s](https://github.com/%s/pull/%s), run %s** for the code-review benchmark. Same base and head commits as the round-1 replay (a second branch name on the same commit, so the reviewer sees a fresh pull request). Never merged. Method: [wachiman/docs/benchmark](%s).' \
    "${SOURCE_REPO}" "$1" "${SOURCE_REPO}" "$1" "$2" "${METHOD_URL}"
}

cmd_rounds() {
  if [ "$#" -lt 2 ]; then usage_die "rounds <repo-name> <k...>"; fi
  local repo="$1" reviewer url i k refs=() existing orig body
  shift
  check_repo_name "${repo}"
  reviewer="$(reviewer_of "${repo}")"
  if [ "${reviewer}" != "wachi" ]; then die "rounds applies to wachi repositories only (got ${reviewer})"; fi
  for k in "$@"; do
    case "${k}" in
      ""|*[!0-9]*) die "round '${k}' is not a number" ;;
    esac
  done
  load_manifest "${DEFAULT_MANIFEST}"
  check_clone
  preflight_gh
  url="$(git_url "${repo}")"

  step "Push replay/pr-<n>/head-r<k> at the head SHAs (rounds: $*)"
  i=0
  while [ "${i}" -lt "${M_COUNT}" ]; do
    for k in "$@"; do
      refs+=("${M_HEAD[$i]}:refs/heads/replay/pr-${M_N[$i]}/head-r${k}")
    done
    i=$((i + 1))
  done
  x git -C "${CLONE}" push -q "${url}" "${refs[@]}"

  step "Open one PR per round and PR, then ask Wachi to review"
  ensure_label "${repo}"
  for k in "$@"; do
    i=0
    while [ "${i}" -lt "${M_COUNT}" ]; do
      existing=""
      if [ "${DRY_RUN}" = 1 ]; then
        show_cmd gh pr list -R "${OWNER}/${repo}" --state open --base "replay/pr-${M_N[$i]}/base" \
          --head "replay/pr-${M_N[$i]}/head-r${k}" --json number --jq '.[0].number // empty'
      else
        existing="$(open_pr_number "${repo}" "replay/pr-${M_N[$i]}/base" "replay/pr-${M_N[$i]}/head-r${k}")"
      fi
      if [ -n "${existing}" ]; then
        note "round ${k}: kaipu#${M_N[$i]} already open as #${existing}, skipped (no new trigger)"
      else
        orig="$(original_body "${M_N[$i]}")"
        body="$(preamble_round "${M_N[$i]}" "${k}")

---

${orig}"
        create_replay_pr "${repo}" "replay/pr-${M_N[$i]}/base" "replay/pr-${M_N[$i]}/head-r${k}" \
          "[replay r${k}] ${M_TITLE[$i]}" "${body}"
        note "round ${k}: kaipu#${M_N[$i]} -> #${NEW_PR_NUM}"
        trigger_review wachi "${repo}" "${NEW_PR_NUM}"
      fi
      i=$((i + 1))
    done
  done
}

# ---------------------------------------------------------------- collect

# Prints the row after the "Cost ($)" header of a Pullfrog run log (`gh run view --log` lines are
# "<job>\t<step>\t<timestamp> <text>"); separator lines of a table are skipped.
# shellcheck disable=SC2016 # awk program, not shell
COST_AWK='
{
  n = split($0, f, "\t")
  if (n >= 3) {
    c = f[3]
    for (i = 4; i <= n; i++) c = c "\t" f[i]
    sub(/^[^ ]+ /, "", c)
  } else {
    c = $0
  }
  gsub(/\033\[[0-9;]*m/, "", c)
  if (grab) {
    t = c
    gsub(/[|+:=[:space:]-]/, "", t)
    if (t == "") next
    print c
    exit
  }
  if (c ~ /Cost \(\$\)/) grab = 1
}
'

collect_one() {
  local file="$1" heading="$2" empty="$3" endpoint="$4" filter="$5" out
  if [ "${DRY_RUN}" = 1 ]; then
    show_cmd gh api "${endpoint}" --paginate --jq "${filter}"
    note "(written to ${file})"
    return 0
  fi
  out="$(gh api "${endpoint}" --paginate --jq "${filter}")"
  {
    printf '%s\n\n' "${heading}"
    if [ -n "${out}" ]; then printf '%s\n' "${out}"; else printf '%s\n' "${empty}"; fi
  } > "${file}"
  note "wrote ${file}"
}

collect_costs() {
  local repo="$1" file="$2" run_id created conclusion title row log runs
  if [ "${DRY_RUN}" = 1 ]; then
    show_cmd gh run list -R "${OWNER}/${repo}" --workflow pullfrog.yml --limit 200 \
      --json databaseId,createdAt,conclusion,displayTitle \
      --jq '.[] | "\(.databaseId)\t\(.createdAt)\t\(.conclusion)\t\(.displayTitle)"'
    show_cmd gh run view "<run-id>" -R "${OWNER}/${repo}" --log
    note "(per run: the line after the 'Cost (\$)' header is written to ${file})"
    return 0
  fi
  runs="$(gh run list -R "${OWNER}/${repo}" --workflow pullfrog.yml --limit 200 \
    --json databaseId,createdAt,conclusion,displayTitle \
    --jq '.[] | "\(.databaseId)\t\(.createdAt)\t\(.conclusion)\t\(.displayTitle)"')"
  {
    printf '# run_id\tcreated_at\tconclusion\ttitle\tcost row (the line after the "Cost ($)" header)\n'
    while IFS=$'\t' read -r run_id created conclusion title; do
      if [ -z "${run_id}" ]; then continue; fi
      log="$(gh run view "${run_id}" -R "${OWNER}/${repo}" --log 2>/dev/null </dev/null || true)"
      row="$(printf '%s\n' "${log}" | awk "${COST_AWK}")"
      if [ -z "${row}" ]; then row="(no cost row found in the log)"; fi
      printf '%s\t%s\t%s\t%s\t%s\n' "${run_id}" "${created}" "${conclusion}" "${title}" "${row}"
    done <<EOF
${runs}
EOF
  } > "${file}"
  note "wrote ${file}"
}

cmd_collect() {
  if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then usage_die "collect <repo-name> <out-dir> [label]"; fi
  local repo="$1" out="$2" label="${3:-}" reviewer list i num title base
  local PR_NUMS=() PR_TITLES=()
  check_repo_name "${repo}"
  reviewer="$(reviewer_of "${repo}")"
  if [ -z "${label}" ]; then label="${repo#kaipu-bench-}"; fi
  preflight_gh
  x mkdir -p "${out}"

  step "List the replay PRs of ${OWNER}/${repo}"
  if [ "${DRY_RUN}" = 1 ]; then
    show_cmd gh pr list -R "${OWNER}/${repo}" --label replay --state all --limit 200 --json number,title \
      --jq '.[] | "\(.number)\t\(.title)"'
    PR_NUMS=("<pr-number>")
    PR_TITLES=("<title>")
  else
    list="$(gh pr list -R "${OWNER}/${repo}" --label replay --state all --limit 200 --json number,title \
      --jq '.[] | "\(.number)\t\(.title)"' | sort -n)"
    while IFS=$'\t' read -r num title; do
      if [ -z "${num}" ]; then continue; fi
      PR_NUMS+=("${num}")
      PR_TITLES+=("${title}")
    done <<EOF
${list}
EOF
    if [ "${#PR_NUMS[@]}" -eq 0 ]; then die "no PR labelled 'replay' in ${OWNER}/${repo}"; fi
    note "${#PR_NUMS[@]} replay PRs"
  fi

  step "Save bot reviews and comments to ${out}"
  i=0
  while [ "${i}" -lt "${#PR_NUMS[@]}" ]; do
    num="${PR_NUMS[$i]}"
    title="${PR_TITLES[$i]}"
    base="${out}/${label}-pr-${num}"
    collect_one "${base}-reviews.md" "# ${repo}#${num} ${title} - bot reviews" "_No bot reviews._" \
      "repos/${OWNER}/${repo}/pulls/${num}/reviews" \
      '.[] | select(.user.type=="Bot") | "## \(.user.login) · \(.state) · \(.submitted_at) · commit \(.commit_id[0:7])\n\n\(.body // "")\n"'
    collect_one "${base}-comments.md" "# ${repo}#${num} ${title} - bot inline comments" "_No bot inline comments._" \
      "repos/${OWNER}/${repo}/pulls/${num}/comments" \
      '.[] | select(.user.type=="Bot") | "## \(.path):\(.line // .original_line // "?") · \(.user.login) · \(.created_at)\(if .in_reply_to_id then " · reply" else "" end)\n\n\(.body)\n"'
    if [ "${reviewer}" = "coderabbit" ]; then
      collect_one "${base}-issue-comments.md" "# ${repo}#${num} ${title} - bot issue comments" "_No bot issue comments._" \
        "repos/${OWNER}/${repo}/issues/${num}/comments" \
        '.[] | select(.user.type=="Bot") | "## \(.user.login) · \(.created_at)\n\n\(.body)\n"'
    fi
    i=$((i + 1))
  done

  if [ "${reviewer}" = "pullfrog" ]; then
    step "Extract Pullfrog's cost row from each run log"
    collect_costs "${repo}" "${out}/${label}-costs.txt"
  fi
}

# ---------------------------------------------------------------- main

main() {
  local n=$# a
  while [ "${n}" -gt 0 ]; do
    a="$1"
    shift
    n=$((n - 1))
    if [ "${a}" = "--dry-run" ]; then DRY_RUN=1; else set -- "$@" "${a}"; fi
  done
  if [ "$#" -eq 0 ]; then usage >&2; exit 2; fi
  local cmd="$1"
  shift
  if [ "${DRY_RUN}" = 1 ]; then printf '# dry run: nothing below is executed\n'; fi
  case "${cmd}" in
    create) cmd_create "$@" ;;
    open) cmd_open "$@" ;;
    rounds) cmd_rounds "$@" ;;
    collect) cmd_collect "$@" ;;
    -h|--help|help) usage ;;
    *) usage >&2; die "unknown subcommand '${cmd}'" ;;
  esac
}

main "$@"
