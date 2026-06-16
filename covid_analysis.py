"""
COVID-19 Global Analysis — Deaths & Recovery by Country
Author: Mohit Mahajan | github.com/Mohit0702
Tools: Python, Pandas, NumPy, Matplotlib, Seaborn

Dataset: country_wise_latest.csv | 187 countries | 15 features
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ─── CONFIG ───────────────────────────────────────────────────────────────────
DARK_BG = '#0a0f1a'
SURFACE = '#151e30'
TEAL    = '#2dd4bf'
BLUE    = '#38bdf8'
RED     = '#fb7185'
AMBER   = '#fbbf24'
GREEN   = '#4ade80'
PURPLE  = '#a78bfa'
TEXT    = '#e6edf7'
MUTED   = '#6b7e99'

plt.rcParams.update({
    'figure.facecolor': DARK_BG,
    'axes.facecolor':   SURFACE,
    'axes.edgecolor':   '#233047',
    'axes.labelcolor':  TEXT,
    'text.color':       TEXT,
    'xtick.color':      MUTED,
    'ytick.color':      MUTED,
    'grid.color':       '#233047',
    'grid.linewidth':   0.5,
    'font.family':      'DejaVu Sans',
})

# ─── LOAD DATA ────────────────────────────────────────────────────────────────
print("Loading COVID-19 dataset...")
df = pd.read_csv('country_wise_latest.csv')
print(f"  Shape: {df.shape[0]} countries x {df.shape[1]} columns")

# ─── COMPUTED METRICS ─────────────────────────────────────────────────────────
top_confirmed = df.nlargest(10, 'Confirmed')[['Country/Region', 'Confirmed', 'Deaths', 'Recovered', 'Active']]
top_deaths    = df.nlargest(10, 'Deaths')[['Country/Region', 'Deaths', 'Confirmed', 'Deaths / 100 Cases']]
top_recovered = df.nlargest(10, 'Recovered')[['Country/Region', 'Recovered', 'Confirmed', 'Recovered / 100 Cases']]

# Death rate / recovery rate leaders (filter small outbreaks for meaningful rates)
sizeable = df[df['Confirmed'] > 1000]
top_death_rate    = sizeable.nlargest(10, 'Deaths / 100 Cases')[['Country/Region', 'Deaths / 100 Cases']]
top_recovery_rate = sizeable.nlargest(10, 'Recovered / 100 Cases')[['Country/Region', 'Recovered / 100 Cases']]

# WHO region rollups
region_df = (df.groupby('WHO Region')[['Confirmed', 'Deaths', 'Recovered', 'Active']]
              .sum().sort_values('Confirmed', ascending=False).reset_index())

# Fastest-growing outbreaks (1 week % increase)
fastest_growth = df.nlargest(8, '1 week % increase')[['Country/Region', '1 week % increase', 'Confirmed']]

# Global totals & rates
totals = df[['Confirmed', 'Deaths', 'Recovered', 'Active']].sum()
global_death_rate    = round(totals['Deaths'] / totals['Confirmed'] * 100, 2)
global_recovery_rate = round(totals['Recovered'] / totals['Confirmed'] * 100, 2)

print(f"\n  Global Confirmed : {totals['Confirmed']:,}")
print(f"  Global Deaths    : {totals['Deaths']:,}  ({global_death_rate}% of confirmed)")
print(f"  Global Recovered : {totals['Recovered']:,}  ({global_recovery_rate}% of confirmed)")
print(f"  Global Active    : {totals['Active']:,}")
print(f"  Worst-hit country (Confirmed) : {top_confirmed.iloc[0]['Country/Region']}")
print(f"  Highest death count           : {top_deaths.iloc[0]['Country/Region']}")
print(f"  Highest recovery count        : {top_recovered.iloc[0]['Country/Region']}")

# ─── PLOTTING ─────────────────────────────────────────────────────────────────
print("\nGenerating charts...")
fig = plt.figure(figsize=(22, 18), facecolor=DARK_BG)
fig.suptitle('COVID-19 Global Analysis  ·  Deaths & Recovery by Country',
              fontsize=20, fontweight='bold', color=TEAL, y=0.97)

gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.38)

# 1. Top 10 Confirmed Cases
ax1 = fig.add_subplot(gs[0, :2])
ax1.barh(top_confirmed['Country/Region'][::-1], top_confirmed['Confirmed'].values[::-1],
         color=BLUE, alpha=0.85, edgecolor='none')
ax1.set_title('Top 10 Countries — Confirmed Cases', color=TEAL, fontsize=11, pad=10)
ax1.tick_params(labelsize=9)
ax1.grid(True, axis='x', alpha=0.4)
for i, val in enumerate(top_confirmed['Confirmed'].values[::-1]):
    ax1.text(val, i, f' {val:,}', va='center', fontsize=8, color=TEXT)

# 2. Global Pie (Recovered / Active / Deaths)
ax2 = fig.add_subplot(gs[0, 2])
ax2.pie([totals['Recovered'], totals['Active'], totals['Deaths']],
        labels=['Recovered', 'Active', 'Deaths'],
        colors=[GREEN, BLUE, RED],
        autopct='%1.1f%%', startangle=90,
        textprops={'fontsize': 9, 'color': TEXT})
ax2.set_title('Global Case Outcome Split', color=TEAL, fontsize=11, pad=10)

# 3. Top 10 Deaths
ax3 = fig.add_subplot(gs[1, 0])
ax3.barh(top_deaths['Country/Region'][::-1], top_deaths['Deaths'].values[::-1],
         color=RED, alpha=0.85, edgecolor='none')
ax3.set_title('Top 10 Countries — Total Deaths', color=TEAL, fontsize=11, pad=10)
ax3.tick_params(labelsize=8)
ax3.grid(True, axis='x', alpha=0.4)
for i, val in enumerate(top_deaths['Deaths'].values[::-1]):
    ax3.text(val, i, f' {val:,}', va='center', fontsize=7, color=TEXT)

# 4. Top 10 Recovered
ax4 = fig.add_subplot(gs[1, 1])
ax4.barh(top_recovered['Country/Region'][::-1], top_recovered['Recovered'].values[::-1],
         color=GREEN, alpha=0.85, edgecolor='none')
ax4.set_title('Top 10 Countries — Total Recovered', color=TEAL, fontsize=11, pad=10)
ax4.tick_params(labelsize=8)
ax4.grid(True, axis='x', alpha=0.4)
for i, val in enumerate(top_recovered['Recovered'].values[::-1]):
    ax4.text(val, i, f' {val:,}', va='center', fontsize=7, color=TEXT)

# 5. Highest Death Rates
ax5 = fig.add_subplot(gs[1, 2])
ax5.barh(top_death_rate['Country/Region'][::-1], top_death_rate['Deaths / 100 Cases'].values[::-1],
         color=AMBER, alpha=0.85, edgecolor='none')
ax5.set_title('Highest Death Rate (per 100 cases)', color=TEAL, fontsize=11, pad=10)
ax5.tick_params(labelsize=8)
ax5.grid(True, axis='x', alpha=0.4)

# 6. Highest Recovery Rates
ax6 = fig.add_subplot(gs[2, 0])
ax6.barh(top_recovery_rate['Country/Region'][::-1], top_recovery_rate['Recovered / 100 Cases'].values[::-1],
         color=PURPLE, alpha=0.85, edgecolor='none')
ax6.set_title('Highest Recovery Rate (per 100 cases)', color=TEAL, fontsize=11, pad=10)
ax6.tick_params(labelsize=8)
ax6.grid(True, axis='x', alpha=0.4)

# 7. WHO Region Confirmed
ax7 = fig.add_subplot(gs[2, 1])
ax7.bar(region_df['WHO Region'], region_df['Confirmed'],
        color=BLUE, alpha=0.85, edgecolor='none')
ax7.set_title('Confirmed Cases by WHO Region', color=TEAL, fontsize=11, pad=10)
ax7.tick_params(axis='x', rotation=45, labelsize=7)
ax7.grid(True, axis='y', alpha=0.4)

# 8. Fastest Growing Outbreaks (1-week % increase)
ax8 = fig.add_subplot(gs[2, 2])
ax8.barh(fastest_growth['Country/Region'][::-1], fastest_growth['1 week % increase'].values[::-1],
         color=RED, alpha=0.85, edgecolor='none')
ax8.set_title('Fastest Growing (1-Week % Increase)', color=TEAL, fontsize=11, pad=10)
ax8.tick_params(labelsize=8)
ax8.grid(True, axis='x', alpha=0.4)

plt.savefig('covid_analysis.png', dpi=150, bbox_inches='tight',
            facecolor=DARK_BG, edgecolor='none')
print("  Saved -> covid_analysis.png")
plt.show()

# ─── SUMMARY ──────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("  ANALYSIS SUMMARY")
print("="*60)
print(f"  Countries covered : {df['Country/Region'].nunique()}")
print(f"  WHO Regions       : {df['WHO Region'].nunique()}")
print(f"  Global Confirmed  : {totals['Confirmed']:,}")
print(f"  Global Deaths     : {totals['Deaths']:,} ({global_death_rate}%)")
print(f"  Global Recovered  : {totals['Recovered']:,} ({global_recovery_rate}%)")
print(f"  Global Active     : {totals['Active']:,}")
print(f"  Worst-hit (cases) : {top_confirmed.iloc[0]['Country/Region']} — {top_confirmed.iloc[0]['Confirmed']:,}")
print(f"  Most deaths       : {top_deaths.iloc[0]['Country/Region']} — {int(top_deaths.iloc[0]['Deaths']):,}")
print(f"  Most recovered    : {top_recovered.iloc[0]['Country/Region']} — {top_recovered.iloc[0]['Recovered']:,}")
print(f"  Highest death rate: {top_death_rate.iloc[0]['Country/Region']} — {top_death_rate.iloc[0]['Deaths / 100 Cases']}%")
print(f"  Highest recovery  : {top_recovery_rate.iloc[0]['Country/Region']} — {top_recovery_rate.iloc[0]['Recovered / 100 Cases']}%")
print("="*60)
