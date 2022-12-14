import numpy as np

def ski(nbr_ski: int, nbr_skieurs: int, tailles_ski: list[float], tailles_skieurs: list[float]):
    """
    :param nbr_ski: nombre de skis
    :param nbr_skieurs: nombre de skieurs
    :param tailles_ski: liste triée des tailles des skis
    :param tailles_skieurs: liste triée des tailles des skieurs
    :return:
    """
    sol: list[list[float]] = [[0 for _ in range(nbr_skieurs+1)] for _ in range(nbr_ski+1)]

    # initialisation
    for i in range(nbr_ski+1):
        for j in range(i+1, nbr_skieurs+1):
            sol[i][j] = np.inf

    for i in range(1, nbr_ski+1):
        for j in range(1, nbr_skieurs+1):
            if j > i:
                pass
            else:
                sol[i][j] = min(
                    sol[i-1][j-1] + abs(tailles_skieurs[j-1]-tailles_ski[i-1]),
                    sol[i-1][j]
                )

    return sol[-1][-1]


# On test avec un exemple simple (on s'attend à 1.4 - le glouton donnerait 1.6)
print(ski(3, 2, [1.90, 3, 3], [1.5, 2]))
