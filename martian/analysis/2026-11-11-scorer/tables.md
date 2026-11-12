## Baselines on the corrected Opus data (echo source: fixed Haiku run)

| Rule | Findings | Matched a golden | Goldens | H+C goldens | FP | R | P | F1 | F2 |
|---|---|---|---|---|---|---|---|---|---|
| all findings | 283 | 103 | 117 | 51 | 177 | 67.6 | 39.8 | 50.1 | 59.3 |
| proximity: echoed by Haiku +-10 | 223 | 98 | 111 | 49 | 123 | 64.2 | 47.4 | 54.5 | 59.9 |
| not echoed (second section) | 60 | 5 | 6 | 2 | 54 | 3.5 | 10.0 | 5.2 | 4.0 |

Kept-goldens mark used below: `>=104` as in the brief (stored data) and `>=111` = this corrected proximity row.

## Arm: haiku scorer

### 1. Threshold on score (main section = score >= t)

| t | Main: findings | matched | goldens | H+C | FP | R | P | F1 | F2 | Second: findings | matched | goldens | H+C | FP | mark |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 283 | 103 | 117 | 51 | 177 | 67.6 | 39.8 | 50.1 | 59.3 | 0 | 0 | 0 | 0 | 0 | >=104 >=prox |
| 2 | 283 | 103 | 117 | 51 | 177 | 67.6 | 39.8 | 50.1 | 59.3 | 0 | 0 | 0 | 0 | 0 | >=104 >=prox |
| 3 | 263 | 98 | 111 | 50 | 162 | 64.2 | 40.7 | 49.8 | 57.5 | 20 | 5 | 6 | 1 | 15 | >=104 >=prox |
| 4 | 206 | 79 | 90 | 45 | 125 | 52.0 | 41.9 | 46.4 | 49.6 | 77 | 24 | 27 | 6 | 52 |  |
| 5 | 150 | 66 | 76 | 40 | 82 | 43.9 | 48.1 | 45.9 | 44.7 | 133 | 37 | 41 | 11 | 95 |  |
| 6 | 119 | 57 | 67 | 36 | 61 | 38.7 | 52.3 | 44.5 | 40.9 | 164 | 46 | 50 | 15 | 116 |  |
| 7 | 80 | 46 | 54 | 30 | 33 | 31.2 | 62.1 | 41.5 | 34.7 | 203 | 57 | 63 | 21 | 144 |  |
| 8 | 46 | 30 | 36 | 17 | 15 | 20.8 | 70.6 | 32.1 | 24.2 | 237 | 73 | 81 | 34 | 162 |  |
| 9 | 17 | 12 | 14 | 5 | 5 | 8.1 | 73.7 | 14.6 | 9.8 | 266 | 91 | 103 | 46 | 172 |  |

Highest threshold keeping >= 104 goldens: t=3, 263 findings, 162 FP (proximity: 223 findings, 123 FP, 111 goldens).

Highest threshold keeping >= 111 goldens (the corrected proximity row): t=3, 263 findings, 162 FP.

### 2. Ranking quality

Top N across the 50 PRs; ties at the boundary are broken at random, so FP and goldens are expected values. AUC = probability that a finding that matched a golden outranks a false positive (0.5 = chance).

| Ranking | AUC | Top 100: FP / goldens | Top 150: FP / goldens | Top 200: FP / goldens |
|---|---|---|---|---|
| score (this arm) | 0.634 | 47.4 / 60.7 | 82.0 / 76.0 | 120.4 / 88.5 |
| severity, then confidence (Wachiman labels) | 0.672 | 44.8 / 63.2 | 80.7 / 77.7 | 114.2 / 95.2 |
| echoed by Haiku (binary) | 0.628 | 55.2 / 49.8 | 82.7 / 74.7 | 110.3 / 99.6 |

### 3. Score combined with proximity

| Rule | Findings | Matched a golden | Goldens | H+C goldens | FP | R | P | F1 | F2 |
|---|---|---|---|---|---|---|---|---|---|
| score>=1 OR echo | 283 | 103 | 117 | 51 | 177 | 67.6 | 39.8 | 50.1 | 59.3 |
| score>=1 AND echo | 223 | 98 | 111 | 49 | 123 | 64.2 | 47.4 | 54.5 | 59.9 |
| score>=2 OR echo | 283 | 103 | 117 | 51 | 177 | 67.6 | 39.8 | 50.1 | 59.3 |
| score>=2 AND echo | 223 | 98 | 111 | 49 | 123 | 64.2 | 47.4 | 54.5 | 59.9 |
| score>=3 OR echo | 271 | 101 | 114 | 51 | 167 | 65.9 | 40.6 | 50.2 | 58.6 |
| score>=3 AND echo | 215 | 95 | 108 | 48 | 118 | 62.4 | 47.8 | 54.1 | 58.8 |
| score>=4 OR echo | 260 | 101 | 114 | 51 | 157 | 65.9 | 42.1 | 51.4 | 59.2 |
| score>=4 AND echo | 169 | 76 | 87 | 43 | 91 | 50.3 | 48.9 | 49.6 | 50.0 |
| score>=5 OR echo | 244 | 100 | 113 | 50 | 142 | 65.3 | 44.3 | 52.8 | 59.7 |
| score>=5 AND echo | 129 | 64 | 74 | 39 | 63 | 42.8 | 54.0 | 47.7 | 44.6 |
| score>=6 OR echo | 236 | 99 | 112 | 50 | 135 | 64.7 | 45.3 | 53.3 | 59.6 |
| score>=6 AND echo | 106 | 56 | 66 | 35 | 49 | 38.2 | 57.4 | 45.8 | 40.9 |
| score>=7 OR echo | 229 | 99 | 112 | 50 | 128 | 64.7 | 46.7 | 54.2 | 60.1 |
| score>=7 AND echo | 74 | 45 | 53 | 29 | 28 | 30.6 | 65.4 | 41.7 | 34.3 |
| score>=8 OR echo | 224 | 99 | 112 | 50 | 123 | 64.7 | 47.7 | 54.9 | 60.4 |
| score>=8 AND echo | 45 | 29 | 35 | 16 | 15 | 20.2 | 70.0 | 31.4 | 23.6 |
| score>=9 OR echo | 224 | 99 | 112 | 50 | 123 | 64.7 | 47.7 | 54.9 | 60.4 |
| score>=9 AND echo | 16 | 11 | 13 | 4 | 5 | 7.5 | 72.2 | 13.6 | 9.2 |

### 6. Kind tag vs outcome

| Kind | Findings | Matched a golden | FP | FP / findings | Mean score |
|---|---|---|---|---|---|
| bug | 148 | 60 | 86 | 58% | 6.3 |
| test-gap | 45 | 9 | 36 | 80% | 4.0 |
| style | 30 | 13 | 17 | 57% | 2.9 |
| speculative | 16 | 4 | 11 | 69% | 3.5 |
| docs | 14 | 3 | 11 | 79% | 2.5 |
| security | 13 | 6 | 7 | 54% | 6.5 |
| concurrency | 7 | 4 | 3 | 43% | 5.7 |
| pre-existing | 6 | 3 | 3 | 50% | 3.0 |
| api-contract | 2 | 1 | 1 | 50% | 4.5 |
| data-loss | 2 | 0 | 2 | 100% | 5.5 |

### 5. Groups

- Groups: 271 for 283 findings. Size 1: 260, 2: 10, 3: 1, 4: 0, 5 or more: 0.
- FP that share a group with a finding that matched a golden: 7 of 177 FP.
- Groups made only of FP: 165. Posting each group as one comment would leave 271 comments; at most 12 FP findings disappear (upper bound: 7 FP next to a match + 5 FP findings folded inside all-FP groups).
- Groups that contain 2 or more distinct goldens (over-merge risk): 14 (0 contain 2 or more separate matched findings).

### 7. Cost and wall time

- 50 scorer calls. Cost per PR: median $0.009, mean $0.011, max $0.10, total $0.56 (subscription estimate from `total_cost_usd`).
- Wall time per PR: median 20 s, mean 23 s, max 78 s, total 19 min (two calls in flight).
- Review (Opus 5.5 high alone): median $0.48 per PR, $26.26 total with the corrected rows. Scorer as a share of the review: 2.1%.

## Arm: opus scorer

### 1. Threshold on score (main section = score >= t)

| t | Main: findings | matched | goldens | H+C | FP | R | P | F1 | F2 | Second: findings | matched | goldens | H+C | FP | mark |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 282 | 103 | 117 | 51 | 176 | 67.6 | 39.9 | 50.2 | 59.4 | 1 | 0 | 0 | 0 | 1 | >=104 >=prox |
| 2 | 280 | 102 | 115 | 51 | 175 | 66.5 | 39.7 | 49.7 | 58.6 | 3 | 1 | 2 | 0 | 2 | >=104 >=prox |
| 3 | 249 | 93 | 106 | 49 | 153 | 61.3 | 40.9 | 49.1 | 55.7 | 34 | 10 | 11 | 2 | 24 | >=104  |
| 4 | 184 | 75 | 85 | 44 | 106 | 49.1 | 44.5 | 46.7 | 48.1 | 99 | 28 | 32 | 7 | 71 |  |
| 5 | 135 | 64 | 74 | 39 | 69 | 42.8 | 51.7 | 46.8 | 44.3 | 148 | 39 | 43 | 12 | 108 |  |
| 6 | 91 | 47 | 55 | 33 | 43 | 31.8 | 56.1 | 40.6 | 34.8 | 192 | 56 | 62 | 18 | 134 |  |
| 7 | 58 | 33 | 38 | 22 | 25 | 22.0 | 60.3 | 32.2 | 25.2 | 225 | 70 | 79 | 29 | 152 |  |
| 8 | 27 | 19 | 20 | 12 | 8 | 11.6 | 71.4 | 19.9 | 13.9 | 256 | 84 | 97 | 39 | 169 |  |
| 9 | 11 | 7 | 7 | 4 | 4 | 4.0 | 63.6 | 7.6 | 5.0 | 272 | 96 | 110 | 47 | 173 |  |

Highest threshold keeping >= 104 goldens: t=3, 249 findings, 153 FP (proximity: 223 findings, 123 FP, 111 goldens).

Highest threshold keeping >= 111 goldens (the corrected proximity row): t=2, 280 findings, 175 FP.

### 2. Ranking quality

Top N across the 50 PRs; ties at the boundary are broken at random, so FP and goldens are expected values. AUC = probability that a finding that matched a golden outranks a false positive (0.5 = chance).

| Ranking | AUC | Top 100: FP / goldens | Top 150: FP / goldens | Top 200: FP / goldens |
|---|---|---|---|---|
| score (this arm) | 0.633 | 48.3 / 58.9 | 80.3 / 77.4 | 117.6 / 90.2 |
| severity, then confidence (Wachiman labels) | 0.672 | 44.8 / 63.2 | 80.7 / 77.7 | 114.2 / 95.2 |
| echoed by Haiku (binary) | 0.628 | 55.2 / 49.8 | 82.7 / 74.7 | 110.3 / 99.6 |

### 3. Score combined with proximity

| Rule | Findings | Matched a golden | Goldens | H+C goldens | FP | R | P | F1 | F2 |
|---|---|---|---|---|---|---|---|---|---|
| score>=1 OR echo | 282 | 103 | 117 | 51 | 176 | 67.6 | 39.9 | 50.2 | 59.4 |
| score>=1 AND echo | 223 | 98 | 111 | 49 | 123 | 64.2 | 47.4 | 54.5 | 59.9 |
| score>=2 OR echo | 280 | 102 | 115 | 51 | 175 | 66.5 | 39.7 | 49.7 | 58.6 |
| score>=2 AND echo | 223 | 98 | 111 | 49 | 123 | 64.2 | 47.4 | 54.5 | 59.9 |
| score>=3 OR echo | 269 | 101 | 114 | 51 | 165 | 65.9 | 40.9 | 50.4 | 58.7 |
| score>=3 AND echo | 203 | 90 | 103 | 47 | 111 | 59.5 | 48.1 | 53.2 | 56.8 |
| score>=4 OR echo | 252 | 101 | 114 | 51 | 148 | 65.9 | 43.5 | 52.4 | 59.7 |
| score>=4 AND echo | 155 | 72 | 82 | 42 | 81 | 47.4 | 50.3 | 48.8 | 48.0 |
| score>=5 OR echo | 241 | 100 | 113 | 50 | 139 | 65.3 | 44.8 | 53.2 | 59.9 |
| score>=5 AND echo | 117 | 62 | 72 | 38 | 53 | 41.6 | 57.6 | 48.3 | 44.1 |
| score>=6 OR echo | 230 | 99 | 112 | 50 | 129 | 64.7 | 46.5 | 54.1 | 60.0 |
| score>=6 AND echo | 84 | 46 | 54 | 32 | 37 | 31.2 | 59.3 | 40.9 | 34.5 |
| score>=7 OR echo | 228 | 99 | 112 | 50 | 127 | 64.7 | 46.9 | 54.4 | 60.2 |
| score>=7 AND echo | 53 | 32 | 37 | 21 | 21 | 21.4 | 63.8 | 32.0 | 24.7 |
| score>=8 OR echo | 224 | 99 | 112 | 50 | 123 | 64.7 | 47.7 | 54.9 | 60.4 |
| score>=8 AND echo | 26 | 18 | 19 | 11 | 8 | 11.0 | 70.4 | 19.0 | 13.2 |
| score>=9 OR echo | 224 | 99 | 112 | 50 | 123 | 64.7 | 47.7 | 54.9 | 60.4 |
| score>=9 AND echo | 10 | 6 | 6 | 3 | 4 | 3.5 | 60.0 | 6.6 | 4.3 |

### 6. Kind tag vs outcome

| Kind | Findings | Matched a golden | FP | FP / findings | Mean score |
|---|---|---|---|---|---|
| bug | 142 | 63 | 77 | 54% | 5.7 |
| test-gap | 45 | 10 | 35 | 78% | 3.9 |
| style | 32 | 12 | 20 | 62% | 2.4 |
| speculative | 17 | 3 | 13 | 76% | 3.3 |
| docs | 15 | 2 | 13 | 87% | 2.1 |
| security | 13 | 5 | 8 | 62% | 6.0 |
| api-contract | 7 | 3 | 4 | 57% | 4.4 |
| concurrency | 6 | 3 | 3 | 50% | 4.8 |
| pre-existing | 4 | 1 | 3 | 75% | 3.0 |
| data-loss | 2 | 1 | 1 | 50% | 8.0 |

### 5. Groups

- Groups: 269 for 283 findings. Size 1: 255, 2: 14, 3: 0, 4: 0, 5 or more: 0.
- FP that share a group with a finding that matched a golden: 6 of 177 FP.
- Groups made only of FP: 164. Posting each group as one comment would leave 269 comments; at most 13 FP findings disappear (upper bound: 6 FP next to a match + 7 FP findings folded inside all-FP groups).
- Groups that contain 2 or more distinct goldens (over-merge risk): 15 (1 contain 2 or more separate matched findings).

### 7. Cost and wall time

- 50 scorer calls. Cost per PR: median $0.188, mean $0.227, max $1.00, total $11.36 (subscription estimate from `total_cost_usd`).
- Wall time per PR: median 23 s, mean 25 s, max 57 s, total 21 min (two calls in flight).
- Review (Opus 5.5 high alone): median $0.48 per PR, $26.26 total with the corrected rows. Scorer as a share of the review: 43.3%.

## 4. Split sample (A = Cal.com + Sentry, 77 goldens; B = Grafana + Discourse + Keycloak, 96 goldens)

| Rule | A: kept / goldens / FP | A: R / P / F1 | B: kept / goldens / FP | B: R / P / F1 |
|---|---|---|---|---|
| all findings | 136 / 56 / 85 | 72.7 / 39.7 / 51.4 | 147 / 61 / 92 | 63.5 / 39.9 / 49.0 |
| proximity: echoed +-10 | 102 / 51 / 56 | 66.2 / 47.7 / 55.4 | 121 / 60 / 67 | 62.5 / 47.2 / 53.8 |
| haiku: score>=8 OR echo (best by F1) | 103 / 52 / 56 | 67.5 / 48.1 / 56.2 | 121 / 60 / 67 | 62.5 / 47.2 / 53.8 |
| haiku: score>=1 AND echo (best by F1) | 102 / 51 / 56 | 66.2 / 47.7 / 55.4 | 121 / 60 / 67 | 62.5 / 47.2 / 53.8 |
| opus: score>=8 OR echo (best by F1) | 103 / 52 / 56 | 67.5 / 48.1 / 56.2 | 121 / 60 / 67 | 62.5 / 47.2 / 53.8 |
| opus: score>=1 AND echo (best by F1) | 102 / 51 / 56 | 66.2 / 47.7 / 55.4 | 121 / 60 / 67 | 62.5 / 47.2 / 53.8 |

Held-out check: threshold chosen on A by F1, evaluated on B (and the reverse).

| Arm | Family | t chosen on A | B result: kept / goldens / FP / F1 | t chosen on B | A result: kept / goldens / FP / F1 |
|---|---|---|---|---|---|
| haiku | score>=t | 1 | 147 / 61 / 92 / 49.0 | 3 | 125 / 52 / 77 / 50.5 |
| haiku | score>=t OR echo | 8 | 121 / 60 / 67 / 53.8 | 8 | 103 / 52 / 56 / 56.2 |
| haiku | score>=t AND echo | 1 | 121 / 60 / 67 / 53.8 | 1 | 102 / 51 / 56 / 55.4 |
| opus | score>=t | 1 | 146 / 61 / 91 / 49.2 | 1 | 136 / 56 / 85 / 51.4 |
| opus | score>=t OR echo | 8 | 121 / 60 / 67 / 53.8 | 8 | 103 / 52 / 56 / 56.2 |
| opus | score>=t AND echo | 1 | 121 / 60 / 67 / 53.8 | 1 | 102 / 51 / 56 / 55.4 |

## False positives set aside per golden set aside (second section)

Higher is better: how many false alarms leave the main section for each known bug that leaves with them. Whole-set baseline: 177 FP over 117 goldens.

| Rule | Second section: FP | Goldens | H+C goldens | FP per golden |
|---|---|---|---|---|
| proximity (not echoed) | 54 | 6 | 2 | 9.0 |
| haiku score < 3 | 15 | 6 | 1 | 2.5 |
| haiku score < 4 | 52 | 27 | 6 | 1.9 |
| haiku score < 5 | 95 | 41 | 11 | 2.3 |
| haiku score < 6 | 116 | 50 | 15 | 2.3 |
| haiku score < 7 | 144 | 63 | 21 | 2.3 |
| haiku score < 8 | 162 | 81 | 34 | 2.0 |
| haiku score < 9 | 172 | 103 | 46 | 1.7 |
| opus score < 3 | 24 | 11 | 2 | 2.2 |
| opus score < 4 | 71 | 32 | 7 | 2.2 |
| opus score < 5 | 108 | 43 | 12 | 2.5 |
| opus score < 6 | 134 | 62 | 18 | 2.2 |
| opus score < 7 | 152 | 79 | 29 | 1.9 |
| opus score < 8 | 169 | 97 | 39 | 1.7 |
| opus score < 9 | 173 | 110 | 47 | 1.6 |

## Agreement between the two scorers

- Spearman rho between Haiku and Opus scores over 283 findings: 0.88. Same score: 45%; within 1 point: 88%.
- Mean score: Haiku 5.12, Opus 4.66.

| Score | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| haiku findings | 0 | 0 | 20 | 57 | 56 | 31 | 39 | 34 | 29 | 16 | 1 |
| opus findings | 1 | 2 | 31 | 65 | 49 | 44 | 33 | 31 | 16 | 10 | 1 |
| haiku FP | 0 | 0 | 15 | 37 | 43 | 21 | 28 | 18 | 10 | 5 | 0 |
| haiku goldens | 0 | 0 | 6 | 21 | 14 | 9 | 13 | 18 | 22 | 13 | 1 |
| opus FP | 1 | 1 | 22 | 47 | 37 | 26 | 18 | 17 | 4 | 4 | 0 |
| opus goldens | 0 | 2 | 9 | 21 | 11 | 19 | 17 | 18 | 13 | 6 | 1 |
