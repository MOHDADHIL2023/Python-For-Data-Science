#3. Ticket Category & Priority Breakdowm

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
# 2. Category vs Priority chart
# -----------------------------
category_priority = pd.crosstab(df['Category'], df['Priority'])

ax = category_priority.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='viridis')

plt.title('IT Tickets by Category and Priority Level', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Ticket Category', fontsize=11)
plt.ylabel('Number of Tickets', fontsize=11)
plt.xticks(rotation=45, ha='right')
plt.legend(title='Priority', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
