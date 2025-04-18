import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load data
with open('performance_data.json', 'r') as f:
    data = json.load(f)

# Prepare data for plotting
algorithms = ['bfs', 'dfs', 'ucs', 'astar']
metrics = ['times', 'memory', 'nodes']
plot_data = []

for algo in algorithms:
    for metric in metrics:
        for value in data[algo][metric]:
            plot_data.append({
                'Algorithm': algo.upper(),
                'Metric': metric.capitalize(),
                'Value': value
            })

df = pd.DataFrame(plot_data)

# Create box plots
plt.figure(figsize=(15, 10))

# Search Time
plt.subplot(3, 1, 1)
sns.boxplot(x='Algorithm', y='Value', data=df[df['Metric'] == 'Times'])
plt.title('Search Time (ms)')
plt.ylabel('Time (ms)')

# Memory Usage
plt.subplot(3, 1, 2)
sns.boxplot(x='Algorithm', y='Value', data=df[df['Metric'] == 'Memory'])
plt.title('Memory Usage (bytes)')
plt.ylabel('Memory (bytes)')

# Expanded Nodes
plt.subplot(3, 1, 3)
sns.boxplot(x='Algorithm', y='Value', data=df[df['Metric'] == 'Nodes'])
plt.title('Expanded Nodes')
plt.ylabel('Nodes')

plt.tight_layout()
plt.savefig('performance_plots.png')
plt.show()