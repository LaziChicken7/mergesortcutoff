import argparse
import random
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--sizes', type=int, nargs='+', default=[1000, 10000, 100000, 500000])
a = p.parse_args()

Path('data').mkdir(exist_ok=True)

for n in a.sizes:
    rng = random.Random(20261117 + n)
    base = [rng.randint(-1000000, 1000000) for _ in range(n)]

    cases = {
        'random': base,
        'ascending': sorted(base),
        'descending': sorted(base, reverse=True),
        'duplicates': [rng.randrange(16) for _ in range(n)],
    }

    for kind, values in cases.items():
        path = Path('data') / f'{kind}_{n}.txt'
        path.write_text(
            str(n) + '\n' + ' '.join(map(str, values)) + '\n',
            encoding='utf-8',
        )
        print(path)
