from pydtmc import (
    MarkovChain,
    plot_graph
)

from pytest import (
    mark
)
import matplotlib.pyplot as plt
p = [[0.2, 0.7, 0.0, 0.1], [0.0, 0.6, 0.3, 0.1], [0.0, 0.0, 1.0, 0.0], [0.5, 0.0, 0.5, 0.0]]
mc = MarkovChain(p, ['s1', 's2', 's3', 's4'])
print(mc)
plt.figure.Figure = plot_graph(mc)[0]
plt.subplots.figure = plot_graph(mc)[1]
#pp.axes._subplots.AxesSubplot = plot_graph(mc)[1]
plt.savefig("figure.png")
print(type(plot_graph(mc)[0]))
print(type(plot_graph(mc)[1]))



#s1/s2/s3/r1/r4/s2/s3/r4/r3/s2/s1/r3/r2/
#counter[s1/r2]: 90%
#counter[s1se1se2/r2]: 80%