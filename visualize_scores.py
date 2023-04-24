import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from config import *


def bar_plot_scores(data, file_name = "score", width = 0.2):
    color_list = list(mcolors.TABLEAU_COLORS.keys())

    models = list(data.keys())
    score_types = list(data[list(data.keys())[0]].keys())

    scores = []
    legends = []
    rects = []

    for m in models:

        model_scores = list(data[m].values())
        scores.append(model_scores)


    N = len(score_types)

    ind = np.arange(N)  # the x locations for the groups
    width = 0.5/N     # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for i in range(len(scores)):
        
        rect = ax.bar(ind+width*i, scores[i], width, color=color_list[i]) #, yerr=menStd)
        legends.append(rect[0])
        rects.append(rect)

    # add some
    ax.set_ylabel('Scores')
    ax.set_title(figure_title)
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels((score_types))

    ax.legend(tuple(legends), tuple(models) )

    for r in rects:
        for bar in r:
            yval = bar.get_height()
            plt.text(bar.get_x(), yval + .005, round(yval, 2))

    plt.show()
    plt.savefig(f'/home/suthomas/evaluation/figures/{file_name}.png')
    print("The visualisation is as saved.")