import matplotlib.pyplot as plt

labels = ['S1','S2','S3']
sections = [56,66,42]
colors = ['c','g','y']

plt.pie(sections, labels=labels, colors=colors, startangle=90, explode=(0,0.1,0), autopct='%1.2f%%')
plt.axis('equal')
plt.title('PIE CHART')
plt.show()