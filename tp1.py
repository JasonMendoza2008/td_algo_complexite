import matplotlib.pyplot as plt
import random
import tkinter as tk

from heapq import *
from timeit import timeit


# Initialisation
def read_map(filename):
    f = open(file=filename, mode="r", encoding="utf-8")

    map_ = {}
    while True:  # reading list of cities from file
        ligne = f.readline().rstrip()
        if ligne == "--":
            break
        info = ligne.split(":")
        map_[info[0]] = {"coords": (int(info[1]), int(info[2])), "next": {}}

    while True:  # reading list of distances from file
        ligne = f.readline().rstrip()
        if ligne == "":
            break
        info = ligne.split(":")
        map_[info[0]]["next"][info[1]] = int(info[2])
        map_[info[1]]["next"][info[0]] = int(info[2])

    return map_


toy_map = {
    "A": {"coords": (100, 100), "next": {"B": 140, "E": 200, "F": 200}},
    "B": {"coords": (200, 140), "next": {"A": 140, "C": 260, "F": 140}},
    "C": {"coords": (360, 40), "next": {"B": 260, "D": 360}},
    "D": {"coords": (320, 360), "next": {"C": 360, "F": 280}},
    "E": {"coords": (80, 280), "next": {"A": 200, "F": 120}},
    "F": {"coords": (160, 240), "next": {"A": 200, "B": 140, "D": 280, "E": 120}},
}

assert read_map("territoire_jouet.map") == toy_map


def draw_map(map_, hospitals=[], l=800, h=800):
    w = tk.Tk()
    c = tk.Canvas(w, width=l, height=h)

    for city in map_:
        for vname in map_[city]["next"]:
            if city < vname:
                x1, y1 = map_[city]["coords"]
                x2, y2 = map_[vname]["coords"]
                c.create_line(x1, y1, x2, y2, dash=True)
                c.create_text(
                    (x1 + x2) // 2, (y1 + y2) // 2, text=map_[city]["next"][vname]
                )

    for city in map_:
        x, y = map_[city]["coords"]
        color = "red" if city in hospitals else "black"
        c.create_rectangle(x - 5, y - 5, x + 5, y + 5, fill=color)
        c.create_text(x + 12, y + 12, text=city)

    c.pack()
    w.mainloop()


# draw_map(toy_map, ["A", "C"])  # pensez à commenter cette ligne après le test


def random_grid_map(n, step):
    map_ = {
        f"{i}_{j}": {"coords": (j * step, i * step), "next": {}}
        for i in range(1, n + 1)
        for j in range(1, n + 1)
    }

    for i in range(1, n + 1):
        for j in range(1, n):
            d = random.randint(step + 1, 2 * step)
            map_[f"{i}_{j}"]["next"][f"{i}_{j + 1}"] = d
            map_[f"{i}_{j + 1}"]["next"][f"{i}_{j}"] = d

    for i in range(1, n):
        for j in range(1, n + 1):
            d = random.randint(step + 1, 2 * step)
            map_[f"{i}_{j}"]["next"][f"{i + 1}_{j}"] = d
            map_[f"{i + 1}_{j}"]["next"][f"{i}_{j}"] = d

    return map_


# draw_map(random_grid_map(5, 100))


# Question 1
def random_dense_map(n: int, d_max: int):
    map_ = {
        f"{i}": {
            "coords": (random.randint(1, d_max), random.randint(1, d_max)),
            "next": {},
        }
        for i in range(n)
    }

    for n1 in map_:
        for n2 in map_:
            if n1 < n2:
                d = random.randint(1, d_max)
                map_[n1]["next"][n2] = d
                map_[n2]["next"][n1] = d

    return map_


def check_map(map_, complete=False):
    for city in map_:
        for voisin in map_[city]["next"]:
            if voisin not in map_:
                print("Error : Le voisin", voisin, "de la ville", city, "n existe pas")
                return False
            if city not in map_[voisin]["next"]:
                print(
                    "Error : La ville",
                    city,
                    "et la ville",
                    voisin,
                    "ne sont pas voisines reciproquement",
                )
                return False
            if map_[city]["next"][voisin] != map_[voisin]["next"][city]:
                print(
                    "Error : La ville",
                    city,
                    "et la ville",
                    voisin,
                    "ne sont pas a la meme distance reciproquement",
                )
                return False
        if complete:
            if len(map_[city]["next"]) < len(map_) - 1:
                print(
                    "Error : Le graphe n est pas complet, il manque des voisins au noeud :",
                    city,
                )
                return False
    return True


def q_1():
    complete_map = random_dense_map(10, 500)
    assert len(complete_map) == 10 and check_map(complete_map, complete=True)
    draw_map(complete_map)


# q_1()


# Question 2
def extract_min_dist(frontier, dist):
    x = min(frontier, key=lambda k: dist[k])
    frontier.remove(x)
    return x


def neighbors(graph, x):
    return graph[x]["next"].keys()


assert neighbors(toy_map, "A") == {"B", "E", "F"}


def distance(graph, x, y):
    return graph[x]["next"][y]


assert distance(toy_map, "A", "B") == 140


def PCCs_naive(graph, s):
    frontier = [s]
    dist = {s: 0}

    while len(frontier) > 0:

        ### extraction du noeud de la frontière ayant la distance minimal    ###
        x = extract_min_dist(frontier, dist)

        ### pour chaque voisin mise à jour de la frontière et de sa distance ###
        for y in neighbors(graph, x):
            if y not in dist:
                frontier.append(y)

            new_dist = dist[x] + distance(graph, x, y)
            if y not in dist or dist[y] > new_dist:
                dist[y] = new_dist

    return dist


assert PCCs_naive(toy_map, "A") == {
    "A": 0,
    "B": 140,
    "E": 200,
    "F": 200,
    "C": 400,
    "D": 480,
}


# Question 3
# tas = [(1, "a"), (0, "b")]
# print(type(tas))
# print(tas)
# heapify(tas)  ### création en O(n)
# print(type(tas))
# print(tas)
# heappush(tas, (0, "c"))  ### insertion en O(log n)
# print(heappop(tas))  ### extraction de (0, 'c') en O(log n)
# print(heappop(tas)[0])  ### extraction >>> '1'
# print(len(tas))  ### mesure en O(1) >>> 1
# print(heappop(tas)[1])  ### extraction >>> 'b'


def PCCs_heap(map_, s):
    frontier = []
    heappush(frontier, (0, s))
    done = set()
    dist = {s: 0}

    while len(frontier) > 0:

        dx, x = heappop(frontier)
        if x in done:
            continue

        done.add(x)  # is done when extracted a first time from the frontier

        for y, dxy in map_[x]["next"].items():
            dy = dx + dxy

            if y not in dist or dist[y] > dy:
                heappush(frontier, (dy, y))
                dist[y] = dy

    return dist


assert PCCs_heap(toy_map, "A") == {
    "A": 0,
    "B": 140,
    "E": 200,
    "F": 200,
    "C": 400,
    "D": 480,
}


# Question 4
def all_distances(map_, PCCs=PCCs_heap):
    d = {(u, v): None for u in map_ for v in map_}
    for u in map_:
        for v, duv in PCCs(map_, u).items():
            d[(u, v)] = duv
    return d


assert all_distances(toy_map) == {
    ("A", "A"): 0,
    ("A", "B"): 140,
    ("A", "C"): 400,
    ("A", "D"): 480,
    ("A", "E"): 200,
    ("A", "F"): 200,
    ("B", "A"): 140,
    ("B", "B"): 0,
    ("B", "C"): 260,
    ("B", "D"): 420,
    ("B", "E"): 260,
    ("B", "F"): 140,
    ("C", "A"): 400,
    ("C", "B"): 260,
    ("C", "C"): 0,
    ("C", "D"): 360,
    ("C", "E"): 520,
    ("C", "F"): 400,
    ("D", "A"): 480,
    ("D", "B"): 420,
    ("D", "C"): 360,
    ("D", "D"): 0,
    ("D", "E"): 400,
    ("D", "F"): 280,
    ("E", "A"): 200,
    ("E", "B"): 260,
    ("E", "C"): 520,
    ("E", "D"): 400,
    ("E", "E"): 0,
    ("E", "F"): 120,
    ("F", "A"): 200,
    ("F", "B"): 140,
    ("F", "C"): 400,
    ("F", "D"): 280,
    ("F", "E"): 120,
    ("F", "F"): 0,
}

map_grid = random_grid_map(10, 100)
# assert all_distances(map_grid, PCCs_heap) == all_distances(map_grid, PCCs_naive)

map_dense = random_dense_map(100, 1000)


# assert all_distances(map_dense, PCCs_heap) == all_distances(map_dense, PCCs_naive)


# Question 5
def benchmark():
    Time_heap_grid = []
    Time_naive_grid = []
    Time_heap_dense = []
    Time_naive_dense = []

    n_list = []

    for N in range(10, 30):
        print(N)  # pour voir que ça avance!

        n = N * N
        n_list.append(n)

        # on compare sur des cartes non-denses: grille de côté N contient N*N villes
        map_grid = random_grid_map(n=N, step=100)

        # on calcule une moyenne sur N lancements en tirant aléatoirement une ville de départ à chaque fois
        Time_naive_grid.append(
            timeit(
                lambda: PCCs_naive(map_grid, random.choice(list(map_grid))), number=N
            )
            / N
        )
        Time_heap_grid.append(
            timeit(lambda: PCCs_heap(map_grid, random.choice(list(map_grid))), number=N)
            / N
        )

        # on compare sur des cartes denses
        map_dense = random_dense_map(n=N * N, d_max=10000)

        Time_naive_dense.append(
            timeit(
                lambda: PCCs_naive(map_dense, random.choice(list(map_dense))), number=N
            )
            / N
        )
        Time_heap_dense.append(
            timeit(
                lambda: PCCs_heap(map_dense, random.choice(list(map_dense))), number=N
            )
            / N
        )

    plt.subplot(2, 1, 1)
    plt.xlabel("N")
    plt.ylabel("T")
    plt.plot(n_list, Time_naive_grid, "r^", label="naive grid")
    plt.plot(n_list, Time_heap_grid, "b^", label="heap grid")
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.xlabel("N")
    plt.ylabel("T")
    plt.plot(n_list, Time_naive_dense, "r*", label="naive dense")
    plt.plot(n_list, Time_heap_dense, "b*", label="heap dense")
    plt.legend()

    plt.show()


# benchmark()

# Question 6
def all_combis_print(candidates):
    x = len(candidates)
    for i in range(1 << x):
        print([candidates[j] for j in range(x) if (i & (1 << j))])


all_combis_print(["A", "B", "C", "D"])


# Question 7
def all_combis_k(candidates, k):
    x = len(candidates)
    for i in range(1 << x):
        combi = [candidates[j] for j in range(x) if (i & (1 << j))]
        if len(combi) == k:
            yield combi


# for combi in all_combis_k(['A','B','C','D'], k=2):
#     print(combi)
