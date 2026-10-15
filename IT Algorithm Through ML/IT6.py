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
# 2. SLA Breach Rate by Category
# -----------------------------
df['SLA_Breached'] = ~df['SLA_Met']

sla_breach = df.groupby('Category')['SLA_Breached'].mean() * 100
sla_breach = sla_breach.sort_values(ascending=False)

# -----------------------------
# 3. Plotting
# -----------------------------
plt.figure(figsize=(9, 5))
bars = plt.bar(sla_breach.index, sla_breach.values,
               color='#d62728', alpha=0.85, edgecolor='black')

plt.title('SLA Breach Rate (%) by IT Request Category',
          fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Category', fontsize=11)
plt.ylabel('SLA Breach Rate (%)', fontsize=11)
plt.ylim(0, max(sla_breach.values) + 10)

# Add labels
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 1,
             f'{height:.1f}%', ha='center', va='bottom',
             fontsize=10, fontweight='bold')

plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
