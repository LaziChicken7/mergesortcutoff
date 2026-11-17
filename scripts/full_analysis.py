import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

Path('results/charts').mkdir(parents=True, exist_ok=True)

df = pd.read_csv('results/all_runs.csv')
df['stem'] = df['input'].apply(lambda s: Path(s).stem)
df[['dtype', 'size']] = df['stem'].str.rsplit('_', n=1, expand=True)
df['size'] = df['size'].astype(int)
df['time_ms'] = df['time_ns'] / 1e6

# Detailed summary per (dataset, dtype, size, cutoff)
summary = (
    df.groupby(['stem', 'dtype', 'size', 'cutoff'], as_index=False)['time_ms']
    .agg(
        n='count',
        mean_ms='mean',
        median_ms='median',
        stdev_ms=lambda s: s.std(ddof=1),
        min_ms='min',
        max_ms='max',
    )
)
summary['cv_pct'] = summary['stdev_ms'] / summary['mean_ms'] * 100.0

# Baseline (cutoff == 0) per dataset
base_med = summary[summary['cutoff'] == 0].set_index('stem')['median_ms']
base_mean = summary[summary['cutoff'] == 0].set_index('stem')['mean_ms']

summary['speedup_median'] = summary['stem'].map(base_med) / summary['median_ms']
summary['speedup_mean'] = summary['stem'].map(base_mean) / summary['mean_ms']
summary = summary.sort_values(['dtype', 'size', 'cutoff']).reset_index(drop=True)
summary.to_csv('results/detailed_summary.csv', index=False)

# Overall ranking using geometric mean of speedup_median & speedup_mean
def geom_mean(vals):
    vals = [v for v in vals if v > 0]
    return math.exp(sum(math.log(v) for v in vals) / len(vals))

ranking_rows = []
for cutoff, grp in summary.groupby('cutoff'):
    gm_med = geom_mean(grp['speedup_median'].tolist())
    gm_mean = geom_mean(grp['speedup_mean'].tolist())
    am_norm_med = (1.0 / grp['speedup_median']).mean()
    avg_cv = grp['cv_pct'].mean()
    ranking_rows.append({
        'cutoff': int(cutoff),
        'geom_mean_speedup_median': gm_med,
        'geom_mean_speedup_mean': gm_mean,
        'mean_normalized_median': am_norm_med,
        'avg_cv_pct': avg_cv,
    })

ranking_df = pd.DataFrame(ranking_rows).sort_values(
    'geom_mean_speedup_median', ascending=False
).reset_index(drop=True)
ranking_df['rank'] = ranking_df.index + 1
ranking_df.to_csv('results/detailed_ranking.csv', index=False)

best_overall = int(ranking_df.iloc[0]['cutoff'])

print("=== OVERALL RANKING (by Geometric Mean of Median Speedup) ===")
print(ranking_df[['rank', 'cutoff', 'geom_mean_speedup_median', 'geom_mean_speedup_mean', 'avg_cv_pct']].to_string(index=False))

print("\n=== BEST CUTOFF PER SIZE (by Geometric Mean of Median Speedup) ===")
for sz, grp in summary.groupby('size'):
    best_c, best_sp = max(
        ((c, geom_mean(g['speedup_median'].tolist())) for c, g in grp.groupby('cutoff')),
        key=lambda x: x[1]
    )
    sp7 = geom_mean(grp[grp['cutoff'] == 7]['speedup_median'].tolist())
    sp10 = geom_mean(grp[grp['cutoff'] == 10]['speedup_median'].tolist())
    print(f"N={sz:6d}: best=CUTOFF {best_c:2d} (speedup={best_sp:.4f}x) | C7={sp7:.4f}x | C10={sp10:.4f}x")

print("\n=== BEST CUTOFF PER DATA TYPE (by Geometric Mean of Median Speedup) ===")
for dt, grp in summary.groupby('dtype'):
    best_c, best_sp = max(
        ((c, geom_mean(g['speedup_median'].tolist())) for c, g in grp.groupby('cutoff')),
        key=lambda x: x[1]
    )
    sp7 = geom_mean(grp[grp['cutoff'] == 7]['speedup_median'].tolist())
    sp10 = geom_mean(grp[grp['cutoff'] == 10]['speedup_median'].tolist())
    print(f"type={dt:10s}: best=CUTOFF {best_c:2d} (speedup={best_sp:.4f}x) | C7={sp7:.4f}x | C10={sp10:.4f}x")

print("\n=== N=500000 DETAILS (CUTOFF 0, 7, 10, BEST) ===")
sub500 = summary[(summary['size'] == 500000) & (summary['cutoff'].isin([0, 7, 10, best_overall]))]
print(sub500[['dtype', 'cutoff', 'mean_ms', 'median_ms', 'stdev_ms', 'min_ms', 'max_ms', 'speedup_median']].to_string(index=False))

# Set clean academic plot style
plt.rcParams.update({
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'legend.fontsize': 9,
})

dtypes_order = ['random', 'ascending', 'descending', 'duplicates']
dtype_labels = {
    'random': 'Random',
    'ascending': 'Ascending (Sorted)',
    'descending': 'Descending (Reversed)',
    'duplicates': 'Many Duplicates',
}

# Chart 1: CUTOFF vs Mean Time (N=500,000 across 4 data types)
fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True)
for ax, dt in zip(axes.flat, dtypes_order):
    sub = summary[(summary['size'] == 500000) & (summary['dtype'] == dt)].sort_values('cutoff')
    ax.plot(sub['cutoff'], sub['mean_ms'], marker='o', linewidth=1.8, label='Mean (ms)')
    ax.plot(sub['cutoff'], sub['median_ms'], marker='s', linestyle='--', linewidth=1.4, label='Median (ms)')
    best_row = sub.loc[sub['mean_ms'].idxmin()]
    ax.scatter([best_row['cutoff']], [best_row['mean_ms']], color='red', zorder=5, s=60,
               label=f"Min Mean: C={int(best_row['cutoff'])} ({best_row['mean_ms']:.2f} ms)")
    ax.set_title(f'{dtype_labels[dt]} (N = 500,000)')
    ax.set_ylabel('Time (milliseconds)')
    ax.grid(alpha=0.3)
    ax.legend()
axes[1, 0].set_xlabel('CUTOFF')
axes[1, 1].set_xlabel('CUTOFF')
fig.suptitle('Biểu đồ 1: Thời gian chạy trung bình và trung vị theo CUTOFF (N = 500,000)', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('results/charts/chart1_cutoff_vs_mean_time.png', dpi=150)
plt.close()

# Chart 2: Compare CUTOFF 0, 7, 10, and Best Overall (N=500,000)
compare_cutoffs = sorted(list({0, 7, 10, best_overall}))
fig, ax = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(dtypes_order))
width = 0.2
for idx, c in enumerate(compare_cutoffs):
    vals = [
        summary[(summary['size'] == 500000) & (summary['dtype'] == dt) & (summary['cutoff'] == c)]['median_ms'].values[0]
        for dt in dtypes_order
    ]
    label = f'CUTOFF = {c}' + (' (Baseline)' if c == 0 else (' (Best)' if c == best_overall else ''))
    bars = ax.bar(x + (idx - (len(compare_cutoffs) - 1) / 2) * width, vals, width, label=label)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.3, f'{v:.1f}', ha='center', va='bottom', fontsize=8)

ax.set_xticks(x)
ax.set_xticklabels([dtype_labels[dt] for dt in dtypes_order])
ax.set_ylabel('Median Time (milliseconds)')
ax.set_title(f'Biểu đồ 2: So sánh thời gian trung vị giữa CUTOFF 0, 7, 10 và {best_overall} (N = 500,000)', fontweight='bold')
ax.grid(axis='y', alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig('results/charts/chart2_compare_0_7_10_best.png', dpi=150)
plt.close()

# Chart 3: Speedup vs Baseline (CUTOFF = 0)
fig, ax = plt.subplots(figsize=(11, 5.5))
for dt in dtypes_order:
    sub = summary[summary['dtype'] == dt]
    sp_by_c = [(c, geom_mean(g['speedup_median'].tolist())) for c, g in sub.groupby('cutoff')]
    sp_by_c.sort(key=lambda t: t[0])
    ax.plot([t[0] for t in sp_by_c], [t[1] for t in sp_by_c], marker='.', alpha=0.7, label=dtype_labels[dt])

rk_sorted = ranking_df.sort_values('cutoff')
ax.plot(rk_sorted['cutoff'], rk_sorted['geom_mean_speedup_median'], marker='o', color='black', linewidth=2.4,
        label='Geometric Mean (All Datasets)')
ax.axhline(1.0, color='gray', linestyle=':', linewidth=1.2, label='Baseline (CUTOFF = 0, 1.00x)')
best_sp_val = ranking_df.iloc[0]['geom_mean_speedup_median']
ax.annotate(f'Best: C={best_overall} ({best_sp_val:.3f}x)',
            xy=(best_overall, best_sp_val), xytext=(best_overall + 4, best_sp_val + 0.03),
            arrowprops=dict(arrowstyle='->', color='red'), fontweight='bold', color='red')
ax.set_xlabel('CUTOFF')
ax.set_ylabel('Speedup = T(CUTOFF=0) / T(CUTOFF=k)')
ax.set_title('Biểu đồ 3: Speedup so với MergeSort cơ bản (CUTOFF = 0) trên các dạng dữ liệu', fontweight='bold')
ax.grid(alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig('results/charts/chart3_speedup_vs_baseline.png', dpi=150)
plt.close()

# Chart 4: Effect of Array Size N on Median Time & Speedup (Random dataset)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
sizes = sorted(summary['size'].unique())
for c in compare_cutoffs:
    sub = summary[(summary['dtype'] == 'random') & (summary['cutoff'] == c)].sort_values('size')
    label = f'CUTOFF = {c}' + (' (Best)' if c == best_overall else '')
    ax1.plot(sub['size'], sub['median_ms'], marker='o', label=label)
    ax2.plot(sub['size'], sub['speedup_median'], marker='o', label=label)

ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xlabel('Array Size N (log scale)')
ax1.set_ylabel('Median Time (milliseconds, log scale)')
ax1.set_title('Thời gian chạy theo kích thước N (Random)')
ax1.grid(True, which='both', alpha=0.3)
ax1.legend()

ax2.set_xscale('log')
ax2.set_xlabel('Array Size N (log scale)')
ax2.set_ylabel('Speedup vs CUTOFF = 0')
ax2.set_title('Speedup theo kích thước N (Random)')
ax2.axhline(1.0, color='gray', linestyle=':')
ax2.grid(True, which='both', alpha=0.3)
ax2.legend()

fig.suptitle('Biểu đồ 4: Ảnh hưởng của kích thước mảng N đến hiệu năng (Dữ liệu Random)', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('results/charts/chart4_array_size_effect.png', dpi=150)
plt.close()

# Chart 5: Variability Boxplot (N=500,000, Random)
fig, ax = plt.subplots(figsize=(12, 5.5))
sub_raw = df[(df['dtype'] == 'random') & (df['size'] == 500000)]
cutoffs_all = sorted(sub_raw['cutoff'].unique())
data_box = [sub_raw[sub_raw['cutoff'] == c]['time_ms'].values for c in cutoffs_all]
bp = ax.boxplot(data_box, tick_labels=[str(c) for c in cutoffs_all], patch_artist=True)
for patch, c in zip(bp['boxes'], cutoffs_all):
    if c == best_overall:
        patch.set_facecolor('#ff9999')
    elif c in (7, 10):
        patch.set_facecolor('#99ccff')
    elif c == 0:
        patch.set_facecolor('#cccccc')
    else:
        patch.set_facecolor('#e6f2ff')

ax.set_xlabel('CUTOFF')
ax.set_ylabel('Execution Time (milliseconds)')
ax.set_title('Biểu đồ 5: Phân bố và độ biến động thời gian chạy qua 15 lần đo (Random, N = 500,000)', fontweight='bold')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('results/charts/chart5_variability_boxplot.png', dpi=150)
plt.close()

print("\nCharts saved to results/charts/")
