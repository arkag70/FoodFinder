import matplotlib.pyplot as plt
legends = []

def plotChart(sampleList, xlabel, ylabel, title, color, legend, chartTuple):
    row, col, pos = chartTuple
    plt.subplot(row, col, pos)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    legends.append(legend)
    plt.plot(list(range(len(sampleList))), sampleList, color)

def viewChart():
    plt.legend(legends, loc="lower right")
    plt.show()