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
# 2. Agent performance summary
# -----------------------------
agent_perf = df.groupby('Agent').agg(
    Total_Tickets=('Ticket_ID', 'count'),
    SLA_Compliance_Rate=('SLA_Met', lambda x: (x.sum() / len(x)) * 100)
).reset_index()

agent_perf = agent_perf.sort_values(by='Total_Tickets', ascending=True)

# -----------------------------
# 3. Plotting horizontal bar chart
# -----------------------------
fig, ax1 = plt.subplots(figsize=(10, 5))

bars = ax1.barh(agent_perf['Agent'], agent_perf['Total_Tickets'],
                color='#aec7e8', edgecolor='#1f77b4', height=0.6)

ax1.set_xlabel('Total Tickets Assigned', fontsize=11, color='#1f77b4')
ax1.set_ylabel('Support Agent', fontsize=11)
ax1.tick_params(axis='x', labelcolor='#1f77b4')
ax1.set_title('IT Service Desk Agent Workload & Volume',
              fontsize=14, fontweight='bold', pad=15)

# Add labels
for bar in bars:
    width = bar.get_width()
    ax1.text(width + 2, bar.get_y() + bar.get_height()/2,
             f'{int(width)}', va='center', ha='left',
             fontsize=10, fontweight='bold')

plt.grid(axis='x', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.show()
