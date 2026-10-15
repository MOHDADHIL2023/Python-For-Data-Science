import matplotlib.pyplot as plt
import numpy as np 
import seaborn as sns

num_points = 20
x = 5 + np.arange(num_points) + np.random.randn(num_points)
y = 10 + np.arange(num_points) + 5 * np.random.randn(num_points)

sns.regplot(x=x, y=y)
plt.show()