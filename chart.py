import matplotlib.pyplot as plt

def plotChart(sampleList, xlabel, ylabel, title, color, chartTuple):
    row, col, pos = chartTuple
    plt.subplot(row, col, pos)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(list(range(len(sampleList))), sampleList, color)

def viewChart():
    plt.show()