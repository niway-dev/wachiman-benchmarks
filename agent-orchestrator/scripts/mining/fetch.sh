#!/bin/bash
n=$1
R=repos/OrchestratorInc/agent-orchestrator/pulls/$n
[ -s c/$n.json ] || gh api --paginate $R/comments?per_page=100 | jq -s 'add' > c/$n.json
[ -s r/$n.json ] || gh api --paginate $R/reviews?per_page=100 | jq -s 'add' > r/$n.json
