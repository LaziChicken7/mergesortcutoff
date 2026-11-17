import argparse
import csv
import platform
import subprocess
import sys
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--trials', type=int, default=15)
p.add_argument(
    '--exe',
    default='./benchmark.exe' if sys.platform == 'win32' else './benchmark',
)
a = p.parse_args()

Path('results').mkdir(exist_ok=True)
Path('results/machine.txt').write_text(
    f'OS: {platform.platform()}\n'
    f'CPU: {platform.processor()}\n'
    f'Trials: {a.trials}\n',
    encoding='utf-8',
)

files = sorted(Path('data').glob('*.txt'))
if not files:
    raise SystemExit('Generate data first')

rows = []
for k, f in enumerate(files):
    out = Path('results') / (f.stem + '.csv')
    subprocess.run(
        [a.exe, str(f), str(a.trials), str(out), str(20261117 + k)],
        check=True,
    )
    with out.open(newline='') as h:
        rows.extend(csv.DictReader(h))

with Path('results/all_runs.csv').open('w', newline='') as h:
    w = csv.DictWriter(h, fieldnames=['input', 'cutoff', 'trial', 'time_ns'])
    w.writeheader()
    w.writerows(rows)

print('Measurements:', len(rows))
