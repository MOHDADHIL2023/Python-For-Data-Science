import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 1. Generate the dataset first
# -----------------------------
np.random.seed(42)

n_tickets = 500
dates = pd.date_range(start='2026-01-01', end='2026-10-01', periods=n_tickets)

categories = ['Hardware', 'Software', 'Network', 'Access Control', 'Printer']
priorities = ['Low', 'Medium', 'High', 'Critical']
agents = ['Alex Smith', 'Maria Garcia', 'John Doe', 'Sarah Connor', 'Dev Patel']

data = {
    'Ticket_ID': [f'INC-{1000 + i}' for i in range(n_tickets)],
    'Date': np.random.choice(dates, n_tickets),
    'Category': np.random.choice(categories, n_tickets, p=[0.25, 0.35, 0.15, 0.15, 0.10]),
    'Priority': np.random.choice(priorities, n_tickets, p=[0.40, 0.35, 0.20, 0.05]),
    'Agent': np.random.choice(agents, n_tickets),
    'Resolution_Hours': np.random.exponential(scale=12, size=n_tickets) + 1,
    'SLA_Met': np.random.choice([True, False], n_tickets, p=[0.82, 0.18])
}

df = pd.DataFrame(data)
df = df.sort_values('Date').reset_index(drop=True)

# -----------------------------
# 2. Resolution time statistics
# -----------------------------
resolution_times = df['Resolution_Hours'].values

mean_time = np.mean(resolution_times)
median_time = np.median(resolution_times)
p90_time = np.percentile(resolution_times, 90)

print(f"--- Resolution Time Statistics (Hours) ---")
print(f"Mean Resolution Time:   {mean_time:.2f} hrs")
print(f"Median Resolution Time: {median_time:.2f} hrs")
print(f"90th Percentile (P90):  {p90_time:.2f} hrs\n")

# -----------------------------
# 3. Histogram plot
# -----------------------------
plt.figure(figsize=(10, 5))
plt.hist(resolution_times, bins=30, color='#2ca02c', edgecolor='black', alpha=0.8)

plt.axvline(mean_time, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_time:.1f}h')
plt.axvline(median_time, color='orange', linestyle='-', linewidth=2, label=f'Median: {median_time:.1f}h')

plt.title('Distribution of Ticket Resolution Times', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Resolution Time (Hours)', fontsize=11)
plt.ylabel('Frequency (Number of Tickets)', fontsize=11)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
