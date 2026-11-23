#!/bin/bash
cd "$1"
N="useState useEffect createServer readFile gen effect pipe Struct makeRuntime useCallback setThread dispatch"
P=('*.ts' '*.tsx' '*.js' ':(exclude)node_modules/*' ':(exclude)*/node_modules/*')
now(){ python3 -c 'import time;print(time.time())'; }
t0=$(now); tot=0; for n in $N; do c=$(git grep -n -I -w -F --no-color -e $n -- "${P[@]}" | wc -l); tot=$((tot+c)); done; t1=$(now)
E=(); for n in $N; do E+=(-e $n); done
c1=$(git grep -n -I -w -F --no-color "${E[@]}" -- "${P[@]}" | wc -l); t2=$(now)
c2=$(git grep -n -I -w -F --no-color "${E[@]}" -- "${P[@]}" ':(exclude).repos/*' | wc -l); t3=$(now)
python3 -c "print('12 separate: %.2fs (%d lines) | one pass: %.2fs (%d lines) | one pass w/o .repos: %.2fs (%d lines)'%($t1-$t0,$tot,$t2-$t1,$c1,$t3-$t2,$c2))"
