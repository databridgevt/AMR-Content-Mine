import matplotlib.pyplot as plt

data = {'apples': 10, 'oranges': 15, 'lemons': 5, 'limes': 20}
x = list(data.keys())
y = list(data.values())

fig, axs = plt.subplots(1, 3)
xticklabels = x
x = range(len(xticklabels))
axs[0].set_xticks(x)
axs[0].set_xticklabels(xticklabels, rotation=45, ha="right")
axs[0].bar(x, y)
axs[1].scatter(x, y)
axs[2].plot(x, y)


plt.show()
