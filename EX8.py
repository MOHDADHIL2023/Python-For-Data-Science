import matplotlib.pyplot as plt
import numpy as np

def random_plots():
    xs = []
    ys = []

    for i in range(20):
        x = i
        y = np.random.randint(10)

        xs.append(x)
        ys.append(y)

    return xs, ys

fig = plt.figure()
ax1 = plt.subplot2grid((5,2), (0,0), rowspan=1, colspan=2)
ax2 = plt.subplot2grid((5,2), (1,0), rowspan=3, colspan=2)
ax3 = plt.subplot2grid((5,2), (4,0), rowspan=1, colspan=1)
ax4 = plt.subplot2grid((5,2), (4,1), rowspan=1, colspan=1)

x, y = random_plots()
ax1.plot(x, y)

x, y = random_plots()
ax2.plot(x, y)

x, y = random_plots()
ax3.plot(x, y)

x, y = random_plots()
ax4.plot(x, y)

plt.tight_layout()
plt.show()