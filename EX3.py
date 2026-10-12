import matplotlib.pyplot as plt
import numpy as np

n = 5 + np.random.randn(1000)
m = [m for m in range(len(n))]

plt.bar(m,n)
plt.title("Raw Data")
plt.show()

plt.hist(n, bins=20)
plt.title("Histagram")
plt.show()

plt.hist(n, cumulative=True, bins=20)
plt.title("Cumulative Histagram")
plt.show()