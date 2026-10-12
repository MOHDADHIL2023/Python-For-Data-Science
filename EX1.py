import matplotlib.pyplot as plt

x = [1,2,3,4,5,6,7,8,9]
y1 = [1,3,5,3,1,3,5,3,1]
y2 = [2,4,6,4,2,4,6,4,2]

plt.plot(x, y1, label="Line L")
plt.plot(x, y2, label="Line H")
plt.plot()

plt.xlabel("x-axis")
plt.ylabel("y-axis")
plt.title("Line  Plot Graph Instance")
plt.legend()
plt.show()