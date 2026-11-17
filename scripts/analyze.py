import csv
import statistics
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt

rows = defaultdict(list)

with open('results/all_runs.csv', newline='') as f:
    for r in csv.DictReader(f):
        key = (Path(r['input']).stem, int(r['cutoff']))
        rows[key].append(int(r['time_ns']) / 1e6)

summary = []
for (name, c), times in sorted(rows.items()):
    summary.append(dict(
        dataset=name,
        cutoff=c,
        n=len(times),
        mean_ms=statistics.mean(times),
        median_ms=statistics.median(times),
        stdev_ms=statistics.stdev(times) if len(times) > 1 else 0,
    ))

with open('results/summary.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(summary[0]))
    w.writeheader()
    w.writerows(summary)

groups = defaultdict(list)
for r in summary:
    groups[r['dataset']].append(r)

scores = defaultdict(list)
for name, rs in groups.items():
    baseline = next(x['median_ms'] for x in rs if x['cutoff'] == 0)
    if baseline:
        for r in rs:
            scores[r['cutoff']].append(r['median_ms'] / baseline)

    rs.sort(key=lambda x: x['cutoff'])

    plt.figure(figsize=(8, 4))
    plt.plot(
        [x['cutoff'] for x in rs],
        [x['median_ms'] for x in rs],
        marker='o',
    )
    plt.xlabel('CUTOFF')
    plt.ylabel('Median (ms)')
    plt.title(name)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('results/chart_' + name + '.png', dpi=140)
    plt.close()

ranking = sorted((statistics.mean(v), c) for c, v in scores.items())

with open('results/ranking.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['cutoff', 'mean_normalized_median'])
    w.writerows((c, score) for score, c in ranking)

print('Best aggregate cutoff:', ranking[0][1], 'score:', ranking[0][0])
print('Review per-dataset charts, 7 vs 10, and noise before concluding.')
