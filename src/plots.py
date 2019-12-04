import matplotlib.pyplot as plt

def setFont(size = 18, family='normal', weight='normal'):
    font = {'family' : family,
            'weight' : weight,
            'size'   : size}

    plt.rc('font', **font)

def transpose(ys):
    tYs = []
    for i in range(len(ys[0])):
        tYs.append([])
        for j in range(len(ys)):
            tYs[i].append(ys[j][i])
    return tYs


def linePlot(x, ys, transposed=False, title="", xlabel="", left_xlim=None, right_xlim=None, ylabel="", bottom_ylim=None, top_ylim=None, legend=None, fontSize=18):
    setFont(size=fontSize)
    if (not transposed):
        ys = transpose(ys)
    fig, ax = plt.subplots()
    if isinstance(x[0], str):
        xticklabels = x
        x = range(len(xticklabels))
        ax.set_xticks(x)
        ax.set_xticklabels(xticklabels, rotation=90, ha="right")
    else:
        ax.set_xticks(x)
        ax.set_xticklabels(x)
    ax.plot(x, ys)
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
    if (not legend == None):
        ax.legend(legend)
    plt.show()


def barPlot(x, y, title="", xlabel="", ylabel="", fontSize=18):
    setFont(size=fontSize)
    fig, ax = plt.subplots()
    if isinstance(x[0], str):
        xticklabels = x
        x = range(len(xticklabels))
        ax.set_xticks(x)
        ax.set_xticklabels(xticklabels, rotation=90, ha="right")
    else:
        ax.set_xticks(x)
        ax.set_xticklabels(x)
    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
    ax.bar(x, y)
    plt.show()


def multiBarPlot(xs, ys, rows, cols, title="", subtitles="", xlabel="", ylabel="", fontSize=18):
    setFont(size=fontSize)
    fig, axs = plt.subplots(rows, cols)
    i = 0
    for r in range(rows):
        if (i == len(xs)):
            break
        for c in range(cols):
            if (i == len(xs)):
                break
            x = xs[i]
            y = ys[i]
            if isinstance(x[0], str):
                xticklabels = x
                x = range(len(xticklabels))
                axs[r][c].set_xticks(x)
                axs[r][c].set_xticklabels(xticklabels, rotation=90, ha="right")
            else:
                axs[r][c].set_xticks(x)
                axs[r][c].set_xticklabels(x)
            if subtitles == "":
                axs[r][c].set(xlabel=xlabel, ylabel=ylabel, title=subtitles)
            else:
                axs[r][c].set(xlabel=xlabel, ylabel=ylabel, title=subtitles[i])
            axs[r][c].bar(x, y)
            i += 1
    fig.subplots_adjust(hspace=1.5)
    fig.suptitle(title)
    plt.show()


if __name__ == "__main__":
    xs = [["a", "b", "c"], ["m", "n", "o"], ["q", "r", "s"], ["x", "y", "z"]]
    ys = [[1, 2, 3], [6, 5, 4], [1, 3, 12], [4, 3, 5]]
    subtitles = ["term1", "term2", "term3", "term4"]
    title = "Terms Found in the Same Sentence as Key Terms"
    xlabel = "Sentence Terms"
    ylabel = "Occurrences"
    multiBarPlot(xs, ys, 2, 3, title = title, subtitles=subtitles, xlabel=xlabel, ylabel=ylabel, fontSize=5)
