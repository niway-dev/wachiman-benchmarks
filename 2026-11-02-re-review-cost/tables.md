### Cost and turns per case

| Case | base | base2 | T | F | TFR |
| --- | --- | --- | --- | --- | --- |
| 478-392778f | $0.56 · 12t · 6r · 1f · 14tr | $0.49 · 11t · 6r · 1f · 14tr | $0.50 · 12t · 7r · 2f · 7tr | $0.43 · 12t · 8r · 2f · 6tr | $0.44 · 11t · 8r · 1f · 7tr |
| 478-64db30b | $0.62 · 9t · 5r · 1f · 13tr | $0.66 · 10t · 5r · 1f · 8tr | $0.62 · 10t · 5r · 0f · 6tr | $0.53 · 8t · 6r · 1f · 6tr | $0.55 · 7t · 4r · 2f · 10tr |
| 479-413ee15 | $0.60 · 17t · 8r · 2f · 4tr | $0.65 · 18t · 11r · 2f · 4tr | $0.52 · 13t · 8r · 1f · 4tr | $0.55 · 15t · 8r · 1f · 4tr | $0.37 · 12t · 7r · 1f · 4tr |
| 482-ad0fa5c | $0.48 · 9t · 5r · 0f · 0tr | $0.36 · 11t · 6r · 0f · 0tr | $0.47 · 13t · 8r · 0f · 0tr | $0.35 · 12t · 7r · 0f · 10tr | $0.24 · 8t · 4r · 0f · 0tr |
| 483-0253fd7 | $0.51 · 14t · 6r · 1f · 0tr | $0.52 · 12t · 7r · 1f · 0tr | $0.48 · 14t · 7r · 1f · 0tr | $0.31 · 9t · 6r · 0f · 0tr | $0.38 · 13t · 8r · 0f · 2tr |
| 484-59f6d48 | $0.21 · 6t · 3r · 1f · 1tr | $0.28 · 8t · 4r · 1f · 1tr | $0.28 · 7t · 3r · 1f · 1tr | $0.28 · 7t · 3r · 1f · 1tr | $0.13 · 4t · 2r · 1f · 1tr |
| **Total** | **$2.99** · 67t · 33r | **$2.97** · 70t · 39r | **$2.87** · 69t · 38r | **$2.46** · 63t · 38r | **$2.11** · 55t · 33r |

### Tool calls (= turns − 1) by class, summed over the cases

| Class | base | base2 | T | F | TFR |
| --- | --- | --- | --- | --- | --- |
| read-changed-full | 7 | 4 | 5 | 3 | 1 |
| read-changed-part | 14 | 21 | 18 | 16 | 14 |
| read-unchanged | 6 | 7 | 7 | 4 | 6 |
| search | 17 | 15 | 16 | 21 | 17 |
| read-threads | 6 | 6 | 5 | 6 | 5 |
| read-pr | 5 | 5 | 6 | 1 | 0 |
| read-evidence | 0 | 0 | 0 | 0 | 0 |
| final-output | 6 | 6 | 6 | 6 | 6 |
| no-tool | 0 | 0 | 0 | 0 | 0 |

### Cost by what entered the context (USD, summed over the cases)

| Part | base | base2 | T | F | TFR |
| --- | --- | --- | --- | --- | --- |
| prompt | 0.880 | 0.907 | 0.893 | 0.807 | 0.755 |
| output | 0.766 | 0.833 | 0.822 | 0.621 | 0.592 |
| read-changed-full | 0.303 | 0.092 | 0.181 | 0.160 | 0.006 |
| read-changed-part | 0.332 | 0.519 | 0.416 | 0.324 | 0.343 |
| read-unchanged | 0.052 | 0.085 | 0.094 | 0.028 | 0.056 |
| search | 0.198 | 0.182 | 0.238 | 0.239 | 0.285 |
| read-threads | 0.291 | 0.309 | 0.107 | 0.311 | 0.114 |
| read-pr | 0.176 | 0.164 | 0.194 | 0.041 | 0.000 |
| reported total | 2.991 | 2.972 | 2.871 | 2.461 | 2.106 |

### Result chars by class (what each class put into context), summed

| Class | base | base2 | T | F | TFR |
| --- | --- | --- | --- | --- | --- |
| read-changed-full | 86025 | 27910 | 52973 | 48080 | 1615 |
| read-changed-part | 116044 | 151441 | 136589 | 106957 | 103470 |
| read-unchanged | 13287 | 20363 | 25602 | 7382 | 17464 |
| search | 46632 | 31861 | 49225 | 42651 | 59146 |
| read-threads | 87633 | 87633 | 31842 | 87633 | 31842 |
| read-pr | 52641 | 45819 | 54915 | 10877 | 0 |
| read-evidence | 0 | 0 | 0 | 0 | 0 |
