import numpy as np
from numpy.random import choice as np_choice

class AntColony(object):

    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        """
        Args:
            distances (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
            n_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iteration (int): Number of iterations
            decay (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, 0.5 to much faster decay.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1
        Example:
            ant_colony = AntColony(german_distances, 100, 20, 2000, 0.95, alpha=1, beta=2)          
        """

        # Distância referente a cada aresta
        # [[np.inf, 2, 2, 5, 7],
        #  [2, np.inf, 4, 8, 2],
        #  [2, 4, np.inf, 1, 3],
        #  [5, 8, 1, np.inf, 2],
        #  [7, 2, 3, 2, np.inf]]
        self.distances  = distances

        # Feromônio referente a cada aresta
        # [[0.2 0.2 0.2 0.2 0.2]
        #  [0.2 0.2 0.2 0.2 0.2]
        #  [0.2 0.2 0.2 0.2 0.2]
        #  [0.2 0.2 0.2 0.2 0.2]
        #  [0.2 0.2 0.2 0.2 0.2]]
        self.pheromone = np.ones(self.distances.shape) / len(distances)

        # Tupla com cada vértice do grafo sendo identificado por um número
        # (0, 1, 2, 3, 4, 5)
        self.all_inds = range(len(distances))

        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    # Execução completa do algoritmo ACO
    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)

        # Loop de acordo com a quantidade de iterações do algoritmo
        for i in range(self.n_iterations):
            # Descreve o caminho de todas as formigas do algoritmo
            all_paths = self.gen_all_paths()
            # Espalha o feromônio nos caminhos melhores
            self.spread_pheronome(all_paths, self.n_best)
            # Pega o menor Path (de acordo com a distância total)
            shortest_path = min(all_paths, key=lambda x: x[1])
            print(shortest_path)

            # shortest_path = ([(0, 2), (2, 3), (3, 4), (4, 1), (1, 0)], 9.0)

            # atualização do melhor caminho para comparar com o próximo melhor Path da próxima iteração
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
            # Atualização do feromônio conforme a taxa de decaimento (ou evaporação) (hiperparâmetro)     
            self.pheromone = self.pheromone * self.decay
        # Retorna o melhor caminho encontrado de todas as iterações        
        return all_time_shortest_path

    # Espalha o feromônio nos caminhos melhores
    def spread_pheronome(self, all_paths, n_best):
        # Ordenar os caminhos com base na distância total
        # Primeiro os caminhos mais curtos
        sorted_paths = sorted(all_paths, key=lambda x: x[1])

        # Pegamos os N melhores caminhos (hiperparâmetro)
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                # Atualizar a quantidade de feromônio nas arestas dos caminhos
                # Esta atualização está correta?
                self.pheromone[move] += 1.0 / self.distances[move]

    # Descobre a distância para determinado caminho
    def gen_path_dist(self, path):
        # Path = [(0, 2), (2, 3), (3, 4), (4, 1), (1, 0)]

        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    # Descreve o caminho de todas as formigas do algoritmo
    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            # Todas as formigas começam do nó inicial 0, por quê?
            path = self.gen_path(0)
            # Exemplo de elementento de all_paths:
            # ([(0, 2), (2, 3), (3, 4), (4, 1), (1, 0)], 9.0)
            all_paths.append((path, self.gen_path_dist(path)))

        # ([(0, 2), (2, 3), (3, 4), (4, 1), (1, 0)], 9.0) => Formiga 1
        # ([(0, 2), (2, 3), (3, 4), (4, 1), (1, 0)], 9.0) => Formiga 2
        # ([(0, 2), (2, 3), (3, 4), (4, 1), (1, 0)], 9.0) => Formiga 3
        # ([(0, 2), (2, 3), (3, 4), (4, 1), (1, 0)], 9.0) => Formiga 4
        # ([(0, 2), (2, 3), (3, 4), (4, 1), (1, 0)], 9.0) => Formiga 5
        return all_paths

    # Descreve o caminho de determinada formiga
    def gen_path(self, start):
        # Start (representa o nó inicial)

        path = []
        visited = set()
        visited.add(start)
        prev = start

        # Para um grafo com 5 vértices, teremos:
        # self.distances == 5
        # Loop (5x)
        for i in range(len(self.distances) - 1):
            # Escolhe o vértice de destino dada
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            # Caminho sendo formado (nó atual da formiga, nó de destino da formiga)
            path.append((prev, move))
            prev = move
            visited.add(move)
        # Voltando para o nó inicial
        path.append((prev, start))  
        return path

    # Escolher movimento dada uma quantidade de arestas possíveis de um nó do grafo
    def pick_move(self, pheromone, dist, visited):
        # Todas as quantidades de feromônio e distâncias das arestas que contêm um vértice em comum
        # Pheromone = [0.2 0.2 0.2 0.2 0.2]
        # Dist = [np.inf, 2, 2, 5, 7]

        # Visited = {0} ou {0, 1}

        pheromone = np.copy(pheromone)
        # print(pheromone)
        # print(pheromone[list(visited)])
        pheromone[list(visited)] = 0
        # print(pheromone[list(visited)])
        # print()

        # Probabilidade da formiga K sair de X e chegar em Y
        row = pheromone ** self.alpha * (( 1.0 / dist) ** self.beta)
        norm_row = row / row.sum()

        # print(row)            [0.   0.   0.65349985   2.33642176  0.]
        # print(row.sum())                2.9899216041461028
        # print(norm_row)       [0.   0.   0.21856755   0.78143245  0.]

        # Escolherá um vértice do grafo dada a probabilidade associdada a cada aresta
        # (0, 1, 2, 3, 4) | 1 | [0.   0.   0.21856755   0.78143245  0.]
        # Método da Roleta (para decidir qual caminho a formiga escolhe)
        move_array = np_choice(self.all_inds, 1, p=norm_row)
        move = move_array[0]
        return move