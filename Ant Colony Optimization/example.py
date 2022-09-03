import numpy as np
from ant_colony import AntColony

# Cada valor representa a distância da aresta linha-coluna (representada pelo indice correspondente da matriz)
# np.inf é definido como o valor padrão para a aresta que os dois vértices iguais
distances = np.array([[np.inf, 2, 2, 5, 7],
                      [2, np.inf, 4, 8, 2],
                      [2, 4, np.inf, 1, 3],
                      [5, 8, 1, np.inf, 2],
                      [7, 2, 3, 2, np.inf]])

ant_colony = AntColony(distances, 1, 1, 100, 0.95, alpha=1, beta=1)

# total = ant_colony.gen_path_dist([(0, 2), (2, 3), (3, 4), (4, 1), (1, 0)])
# 2 + 1 + 2 + 2 + 2 = 9.0

# ant_colony.pick_move(np.ones([0.2, 0.2, 0.2, 0.2, 0.2]), [np.inf, 2, 2, 5, 7], {0})

shortest_path = ant_colony.run()
print("\n" + "shorted_path: {}".format(shortest_path))