# Cricket-
its a cricket dashboard with python code which is used to show player perfomances per year in total
# 🏏 Cricket Performance Analysis — IPL (2008–2025)

Analysis of IPL ball-by-ball data using Python, SQL, Pandas, and an interactive HTML dashboard.

## 📊 Dataset
- 2,83,000+ deliveries across 17 seasons
- 65 features including player stats, venues, toss decisions, match outcomes

## 🔍 Key Insights
- V Kohli is the all-time top scorer with 8,880 runs
- YS Chahal leads with 220 wickets
- Teams choosing to **field** after toss win 53.7% of matches vs 45.2% batting
- 2025 season had the highest runs ever scored in IPL history

## 🛠 Tools Used
- Python, Pandas, NumPy
- SQL (SQLite) for aggregation queries
- Matplotlib, Seaborn for visualizations
- HTML + Chart.js for interactive dashboard

## 📁 Files
| File | Description |
|------|-------------|
| `cricket_analysis.py` | Main analysis script with SQL queries and 8 charts |
| `ipl_dashboard.html` | Interactive dark-themed dashboard |
| `IPL.csv` | Raw dataset |

## ▶️ How to Run
```bash
pip install pandas numpy matplotlib seaborn
python cricket_analysis.py
```
Open `ipl_dashboard.html` in any browser for the dashboard.
