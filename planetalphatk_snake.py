
from Element import *
from Grid import Grid
import tkinter as tk
import random


class PlanetAlpha(Grid):
    """
    Représente une planète sous forme de grille.
    Chaque cellule peut contenir le sol ou un élément.
    """

    # Directions possibles sous forme de déplacements (ligne, colonne).
    NORTH, EAST, SOUTH, WEST = (-1, 0), (0, 1), (1, 0), (0, -1)
    NORTH_EAST, SOUTH_EAST, SOUTH_WEST, NORTH_WEST = (-1, 1), (1, 1), (1, -1), (-1, -1)

    # Directions permettant de se déplacer uniquement horizontalement ou verticalement.
    CARDINAL_POINTS = (NORTH, EAST, SOUTH, WEST)

    # Ensemble des huit directions possibles, diagonales comprises.
    WIND_ROSE = (NORTH, NORTH_EAST, EAST, SOUTH_EAST, SOUTH, SOUTH_WEST, WEST, NORTH_WEST)

    def __init__(self, name, latitude_cells_count, longitude_cells_count, ground):
        """Initialise la planète avec son nom, son sol et ses dimensions."""
        self.__name = name
        self.__ground = ground

        # Initialise la grille avec le sol dans toutes les cellules.
        super().__init__([[ground for i in range(longitude_cells_count)] for i in range(latitude_cells_count)])

    def get_name(self):
        """Retourne le nom de la planète."""
        return self.__name
    
    def get_ground(self):
        """Retourne le type de sol utilisé sur la planète."""
        return self.__ground

    def get_random_free_place(self):
        """Retourne le numéro d'une cellule contenant du sol, choisie aléatoirement."""
        res = self.get_same_value_cell_numbers(self.__ground)

        # Vérifie qu'il existe au moins une cellule libre.
        if len(res) == 0:
            return -1

        return random.choice(res)
    
    def born(self, cell_number, element):
        """Place un nouvel élément dans une cellule libre."""
        res = self.get_cell(cell_number)

        # Empêche la naissance si la cellule ne contient pas le sol.
        if res != self.__ground:
            return 0

        self.set_cell(cell_number, element)
        return 1
    
    def die(self, cell_number):
        """Supprime l'élément présent dans une cellule et y remet le sol."""
        res = self.get_cell(cell_number)

        # Vérifie qu'un élément est bien présent dans la cellule.
        if res == self.__ground:
            return 0

        self.set_cell(cell_number, self.__ground)
        return 1

    def __repr__(self):
        """Retourne une représentation textuelle de la planète et de ses habitants."""
        sol = self.get_count(self.__ground)
        total = self.get_lines_count() * self.get_columns_count()

        # Le nombre d'habitants correspond au nombre de cellules qui ne contiennent pas le sol.
        res = total - sol

        return self.get_name() + "(" + str(res) + " habitants)\n" + self.get_grid_str('')


class PlanetTk(PlanetAlpha, tk.Canvas):
    """
    Représente une planète graphique à l'aide d'un Canvas Tkinter.
    Hérite de PlanetAlpha pour gérer la grille et de tk.Canvas pour l'affichage.
    """

    def __init__(self, root, name, latitude_cells_count, longitude_cells_count,
                 authorized_classes,
                 background_color='white',
                 foreground_color='dark blue',
                 gridlines_color='white',
                 cell_size=40,
                 gutter_size=0,
                 margin_size=0,
                 show_content=True,
                 show_grid_lines=True,
                 **kw):

        # Initialise la partie logique de la planète avec un sol par défaut.
        PlanetAlpha.__init__(self, name, latitude_cells_count, longitude_cells_count, Ground())

        # Initialise le composant graphique Tkinter.
        tk.Canvas.__init__(self, root, **kw)

        self.__root = root
        self.__cell_size = cell_size
        self.__gutter_size = gutter_size
        self.__margin_size = margin_size
        self.__show_content = show_content
        self.__show_grid_lines = show_grid_lines
        self.__authorized_classes = authorized_classes
        self.__background_color = background_color
        self.__foreground_color = foreground_color
        self.__gridlines_color = gridlines_color

        # Calcule les dimensions du Canvas en fonction du nombre de cellules.
        width = longitude_cells_count * cell_size
        height = latitude_cells_count * cell_size

        # Configure les dimensions et la couleur de fond du Canvas.
        self.config(width=width, height=height, bg=background_color)

        # Ajoute le Canvas à la fenêtre principale.
        self.pack()

        # Dessine la grille puis les éléments qu'elle contient.
        self.draw_grid()
        self.draw_elements()


    def get_root(self):
        """Retourne la fenêtre principale associée au Canvas."""
        return self.__root


    def get_background_color(self):
        """Retourne la couleur de fond du Canvas."""
        return self.__background_color


    def get_foreground_color(self):
        """Retourne la couleur utilisée pour afficher les éléments."""
        return self.__foreground_color


    def draw_grid(self):
        """Dessine les lignes horizontales et verticales de la grille."""

        # Ne dessine rien si l'affichage des lignes est désactivé.
        if not self.__show_grid_lines:
            return

        rows = self.get_lines_count()
        cols = self.get_columns_count()

        # Dessine les lignes horizontales de la grille.
        for i in range(rows + 1):
            y = i * self.__cell_size
            self.create_line(0, y, cols * self.__cell_size, y,
                             fill=self.__gridlines_color)

        # Dessine les lignes verticales de la grille.
        for j in range(cols + 1):
            x = j * self.__cell_size
            self.create_line(x, 0, x, rows * self.__cell_size,
                             fill=self.__gridlines_color)
    

    def draw_elements(self):
        """Affiche les éléments présents dans les cellules du Canvas."""

        # Ne dessine pas les éléments si leur affichage est désactivé.
        if not self.__show_content:
            return

        # Supprime les anciens éléments graphiques pour éviter les doublons.
        self.delete("element")

        rows = self.get_lines_count()
        cols = self.get_columns_count()

        # Parcourt toutes les cellules de la grille.
        for cell_number in range(rows * cols):

            element = PlanetAlpha.get_cell(self, cell_number)

            if element is not None:

                # Convertit le numéro de cellule en coordonnées ligne et colonne.
                row = cell_number // cols
                col = cell_number % cols

                # Calcule le centre de la cellule pour positionner son contenu.
                x = col * self.__cell_size + self.__cell_size // 2
                y = row * self.__cell_size + self.__cell_size // 2

                # Affiche la représentation textuelle de l'élément dans la cellule.
                self.create_text(
                    x,
                    y,
                    text=str(element),
                    fill=self.__foreground_color,
                    font=("Arial", int(self.__cell_size * 0.5)),
                    anchor="center",
                    tags="element"
                )

    
    def born(self, cell_number, element):
        """Ajoute un élément dans une cellule et actualise l'affichage."""
        PlanetAlpha.born(self, cell_number, element)
        self.draw_elements()


    def die(self, cell_number, element=None):
        """Supprime un élément d'une cellule et actualise l'affichage."""
        PlanetAlpha.die(self, cell_number)
        self.draw_elements()


    def born_randomly(self, element):
        """Place un élément dans une cellule libre choisie aléatoirement."""

        cell_number = self.get_random_free_place()

        # Vérifie qu'une cellule libre a été trouvée.
        if cell_number != -1:
            self.born(cell_number, element)


    def populate(self, class_names_count):
        """Remplit la planète avec les quantités demandées pour chaque classe."""

        for c in class_names_count:

            # Vérifie que la classe fait partie des classes autorisées.
            if c in self.__authorized_classes:

                # Crée et place le nombre demandé d'éléments de cette classe.
                for i in range(class_names_count[c]):
                    self.born_randomly(c())


    def move_element(self, cell_number, new_cell_number):
        """Déplace un élément d'une cellule vers une autre."""

        element = PlanetAlpha.get_cell(self, cell_number)

        # Déplace uniquement une cellule qui contient un élément.
        if element is not None:
            self.die(cell_number)
            self.born(new_cell_number, element)


    def get_classes_cell_number(self):
        """Compte le nombre d'éléments présents pour chaque classe."""

        res = {}

        rows = self.get_lines_count()
        cols = self.get_columns_count()

        # Parcourt toutes les cellules de la planète.
        for i in range(rows * cols):

            element = PlanetAlpha.get_cell(self, i)

            if element is not None:

                # Récupère le nom de la classe de l'élément.
                name = type(element).__name__

                # Incrémente le compteur associé à cette classe.
                res[name] = res.get(name, 0) + 1

        return res


    def __repr__(self):
        """Réutilise la représentation textuelle définie dans PlanetAlpha."""
        return PlanetAlpha.__repr__(self)

    # Utilise la même représentation pour str() et repr().
    __str__ = __repr__
