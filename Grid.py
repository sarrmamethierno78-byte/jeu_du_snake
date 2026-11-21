
# -*- coding: utf-8 -*-

import random
from copy import deepcopy


class Grid:
    """
    Représente une grille à deux dimensions composée de lignes et de colonnes.
    Fournit des méthodes pour manipuler les cellules, leurs valeurs et leurs voisins.
    """

    def __init__(self, grid_init):
        """Initialise la grille à partir d'une grille existante."""
        # Effectue une copie indépendante pour ne pas modifier la grille d'origine.
        self.__grid = deepcopy(grid_init)

        # Mémorise les dimensions de la grille.
        self.__lines_count = len(grid_init)
        self.__columns_count = len(grid_init[0])

    def get_grid(self):
        """Retourne la grille complète."""
        return self.__grid

    def get_lines_count(self):
        """Retourne le nombre de lignes de la grille."""
        return self.__lines_count

    def get_columns_count(self):
        """Retourne le nombre de colonnes de la grille."""
        return self.__columns_count

    def fill_random(self, values):
        """Remplit chaque cellule avec une valeur choisie aléatoirement."""
        for i in range(self.__lines_count):
            for j in range(self.__columns_count):
                self.__grid[i][j] = random.choice(values)

    def get_line(self, line_number):
        """Retourne toutes les valeurs de la ligne indiquée."""
        return self.__grid[line_number]

    def get_column(self, column_number):
        """Retourne toutes les valeurs de la colonne indiquée."""
        return [self.__grid[i][column_number] for i in range(self.__lines_count)]

    def get_diagonal(self):
        """Retourne les valeurs de la diagonale principale."""
        return [self.__grid[i][i] for i in range(self.__lines_count)]

    def get_anti_diagonal(self):
        """Retourne les valeurs de la diagonale secondaire."""
        return [self.__grid[i][self.__columns_count - i - 1] for i in range(self.__lines_count)]

    def get_line_str(self, line_number, separator='\t'):
        """Convertit une ligne en chaîne de caractères avec un séparateur."""
        return separator.join(str(v) for v in self.__grid[line_number])

    def get_grid_str(self, separator='\t'):
        """Convertit toute la grille en chaîne de caractères, ligne par ligne."""
        return '\n'.join(self.get_line_str(i, separator) for i in range(self.__lines_count))

    def has_equal_values(self, value):
        """Vérifie si toutes les cellules de la grille contiennent la valeur indiquée."""
        return all([all([value == grid_value for grid_value in line]) for line in self.__grid])

    def is_square(self):
        """Vérifie si la grille possède autant de lignes que de colonnes."""
        return self.__lines_count == self.__columns_count

    def get_count(self, value):
        """Compte le nombre de cellules contenant la valeur indiquée."""
        return sum(1 for line in self.__grid for v in line if v == value)

    def get_sum(self):
        """Calcule la somme de toutes les valeurs numériques de la grille."""
        return sum(sum(line) for line in self.__grid)

    def get_coordinates_from_cell_number(self, cell_number):
        """Convertit un numéro de cellule en coordonnées (ligne, colonne)."""
        return (cell_number // self.__columns_count,
                cell_number % self.__columns_count)

    def get_cell_number_from_coordinates(self, line_number, column_number):
        """Convertit des coordonnées (ligne, colonne) en numéro de cellule."""
        return line_number * self.__columns_count + column_number

    def get_cell(self, cell_number):
        """Retourne la valeur contenue dans une cellule à partir de son numéro."""
        line, col = self.get_coordinates_from_cell_number(cell_number)
        return self.__grid[line][col]

    def set_cell(self, cell_number, value):
        """Modifie la valeur d'une cellule à partir de son numéro."""
        line, col = self.get_coordinates_from_cell_number(cell_number)
        self.__grid[line][col] = value

    def get_same_value_cell_numbers(self, value):
        """Retourne les numéros de toutes les cellules contenant la valeur indiquée."""
        res = []

        # Parcourt l'ensemble des cellules de la grille.
        for i in range(self.__lines_count):
            for j in range(self.__columns_count):

                # Vérifie si la cellule contient la valeur recherchée.
                if self.__grid[i][j] == value:
                    res.append(self.get_cell_number_from_coordinates(i, j))

        return res

    def get_neighbour(self, line_number, column_number, delta, is_tore=True):
        """
        Retourne la valeur d'une cellule voisine.
        delta représente le déplacement (variation de ligne, variation de colonne).
        Si is_tore est True, les bords opposés de la grille sont reliés.
        """
        dl, dc = delta

        # Calcule les nouvelles coordonnées du voisin.
        new_line = line_number + dl
        new_col = column_number + dc

        if is_tore:
            # Le modulo permet de revenir de l'autre côté de la grille.
            new_line %= self.__lines_count
            new_col %= self.__columns_count
        else:
            # En mode classique, vérifie que le voisin reste dans les limites.
            if not (0 <= new_line < self.__lines_count and
                    0 <= new_col < self.__columns_count):
                return None

        return self.__grid[new_line][new_col]

    def get_neighborhood(self, line_number, column_number, deltas, is_tore=True):
        """Retourne les valeurs des voisins correspondant aux directions fournies."""
        res = []

        # Récupère successivement chaque voisin.
        for delta in deltas:
            neigh = self.get_neighbour(line_number, column_number, delta, is_tore)
            res.append(neigh)

        return res

    def get_cell_neighbour_number(self, cell_number, delta, is_tore=True):
        """Retourne le numéro de la cellule voisine à partir du numéro de la cellule initiale."""
        line, col = self.get_coordinates_from_cell_number(cell_number)
        dl, dc = delta

        # Calcule les coordonnées du voisin.
        new_line = line + dl
        new_col = col + dc

        if is_tore:
            # Relie les bords opposés lorsque la grille fonctionne en mode tore.
            new_line %= self.__lines_count
            new_col %= self.__columns_count
        else:
            # Retourne None si le voisin se trouve en dehors de la grille.
            if not (0 <= new_line < self.__lines_count and
                    0 <= new_col < self.__columns_count):
                return None

        return self.get_cell_number_from_coordinates(new_line, new_col)

    def get_cell_neighborhood_numbers(self, cell_number, deltas, is_tore=True):
        """Retourne les numéros des cellules voisines, triés par ordre croissant."""
        res = []

        # Recherche le numéro de chaque voisin.
        for delta in deltas:
            neigh = self.get_cell_neighbour_number(cell_number, delta, is_tore)

            # Ignore les voisins inexistants en mode non torique.
            if neigh is not None:
                res.append(neigh)

        return sorted(res)


if __name__ == '__main__':

    # Fixe la graine aléatoire afin de rendre les résultats des tests reproductibles.
    random.seed(1000)

    # Constantes représentant les huit directions possibles.
    NORTH, EAST, SOUTH, WEST = (-1, 0), (0, 1), (1, 0), (0, -1)
    NORTH_EAST, SOUTH_EAST, SOUTH_WEST, NORTH_WEST = (-1, 1), (1, 1), (1, -1), (-1, -1)

    # Regroupe les directions cardinales et les huit directions de la rose des vents.
    CARDINAL_POINTS = (NORTH, EAST, SOUTH, WEST)
    WIND_ROSE = (NORTH, NORTH_EAST, EAST, SOUTH_EAST, SOUTH, SOUTH_WEST, WEST, NORTH_WEST)

    # Constantes utilisées pour configurer les tests.
    LINES_COUNT_TEST, COLUMNS_COUNT_TEST = 5, 7
    LINE_NUMBER_TEST, COLUMN_NUMBER_TEST = 1, 6
    CELL_NUMBER_TEST = 13
    VALUE_TEST = 0
    VALUES_TEST = list(range(2))
    IS_TORE_TEST = True
    DIRECTION_TEST = EAST

    # Crée une grille initiale de 5 lignes et 7 colonnes remplie de zéros.
    GRID_INIT_TEST = [[VALUE_TEST] * COLUMNS_COUNT_TEST
                      for _ in range(LINES_COUNT_TEST)]

    CELL_SIZE_TEST = 100
    MARGIN_TEST = 20
    SHOW_VALUES_TEST = True

    # Création de la grille de test et remplissage aléatoire de ses cellules.
    GRID_TEST = Grid(GRID_INIT_TEST)
    GRID_TEST.fill_random(VALUES_TEST)

    # Vérifie la récupération d'une ligne et d'une colonne.
    assert GRID_TEST.get_line(LINE_NUMBER_TEST) == [1, 0, 0, 0, 1, 1, 0]
    assert GRID_TEST.get_column(COLUMN_NUMBER_TEST) == [0, 0, 0, 0, 1]

    # Vérifie la récupération des deux diagonales.
    assert GRID_TEST.get_diagonal() == [1, 0, 1, 0, 0]
    assert GRID_TEST.get_anti_diagonal() == [0, 1, 0, 0, 0]

    # Vérifie la conversion des lignes et de la grille en chaînes de caractères.
    assert GRID_TEST.get_line_str(2) == '1	0	1	0	0	1	0'
    assert GRID_TEST.get_grid_str('') == '1011010\n1000110\n1010010\n1100100\n0101001'

    # Vérifie si toutes les cellules possèdent la même valeur.
    assert not GRID_TEST.has_equal_values(GRID_INIT_TEST[0][0])

    GRID_TEST2 = Grid([[1 for _ in range(10)] for _ in range(10)])
    assert GRID_TEST2.has_equal_values(1)

    # Vérifie si les grilles sont carrées.
    assert not GRID_TEST.is_square()
    assert GRID_TEST2.is_square()

    # Vérifie le comptage des valeurs et le calcul de leur somme.
    assert GRID_TEST.get_count(1) == GRID_TEST.get_sum() == 16

    # Vérifie la conversion entre numéros de cellules et coordonnées.
    assert GRID_TEST.get_coordinates_from_cell_number(13) == (1, 6)
    assert GRID_TEST.get_cell_number_from_coordinates(LINE_NUMBER_TEST, COLUMN_NUMBER_TEST) == 13

    # Vérifie la lecture et la modification d'une cellule.
    assert GRID_TEST.get_cell(9) == 0
    GRID_TEST.set_cell(9, 1)
    assert GRID_TEST.get_cell(9) == 1

    # Vérifie la recherche des cellules contenant une valeur donnée.
    assert GRID_TEST.get_same_value_cell_numbers(1) == [0, 2, 3, 5, 7, 9, 11, 12, 14, 16, 19, 21, 22, 25, 29, 31, 34]

    # Vérifie la récupération des voisins en mode tore et en mode classique.
    assert GRID_TEST.get_neighbour(LINE_NUMBER_TEST, COLUMN_NUMBER_TEST, DIRECTION_TEST, IS_TORE_TEST) == 1
    assert not GRID_TEST.get_neighbour(LINE_NUMBER_TEST, COLUMN_NUMBER_TEST, DIRECTION_TEST, not IS_TORE_TEST)

    # Vérifie la récupération des huit voisins d'une cellule.
    assert GRID_TEST.get_neighborhood(LINE_NUMBER_TEST, COLUMN_NUMBER_TEST, WIND_ROSE, IS_TORE_TEST) == [0, 1, 1, 1, 0, 1, 1, 1]
    assert GRID_TEST.get_neighborhood(LINE_NUMBER_TEST, COLUMN_NUMBER_TEST, WIND_ROSE, not IS_TORE_TEST) == [0, None, None, None, 0, 1, 1, 1]

    # Vérifie la récupération des numéros des cellules voisines.
    assert GRID_TEST.get_cell_neighbour_number(CELL_NUMBER_TEST, DIRECTION_TEST, IS_TORE_TEST) == 7
    assert not GRID_TEST.get_cell_neighbour_number(CELL_NUMBER_TEST, DIRECTION_TEST, not IS_TORE_TEST)

    # Vérifie les numéros des huit voisins, avec et sans connexion des bords.
    assert GRID_TEST.get_cell_neighborhood_numbers(CELL_NUMBER_TEST, WIND_ROSE, IS_TORE_TEST) == [0, 5, 6, 7, 12, 14, 19, 20]
    assert GRID_TEST.get_cell_neighborhood_numbers(CELL_NUMBER_TEST, WIND_ROSE, not IS_TORE_TEST) == [5, 6, 12, 19, 20]

    # Affiche un message si tous les tests ont réussi.
    print("Tests all OK")
