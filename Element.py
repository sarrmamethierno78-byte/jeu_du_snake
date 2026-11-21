
import random

from copy import deepcopy


class Element:
    """Classe de base représentant un élément de la planète."""

    def __init__(self, char_repr):
        # Caractère ou symbole utilisé pour représenter l'élément.
        self.__char_repr = char_repr

    def __repr__(self):
        # Retourne la représentation textuelle de l'élément.
        return self.__char_repr

    def __eq__(self, other):
        # Deux éléments sont égaux s'ils sont de la même classe
        # et possèdent le même caractère de représentation.
        return isinstance(other, self.__class__) and self.__char_repr == other.__char_repr


class Resource(Element):
    """Classe représentant une ressource pouvant être consommée."""

    def __init__(self, char_repr, value):
        # Valeur nutritive ou énergétique de la ressource.
        self.__value = value
        super().__init__(char_repr)

    def get_value(self):
        # Retourne la valeur de la ressource.
        return self.__value


class Water(Resource):
    """Ressource représentant l'eau."""

    def __init__(self):
        # L'eau est représentée par un poisson et possède une valeur de 1.
        super().__init__('\U0001F41F', 1)


class Herb(Resource):
    """Ressource représentant l'herbe."""

    def __init__(self):
        # L'herbe est représentée par un brin d'herbe et possède une valeur de 3.
        super().__init__('\U0001F33F', 3)


class Animal(Element):
    """Classe de base représentant un animal de la planète."""

    def __init__(self, char_repr, life_max):
        super().__init__(char_repr)

        # Âge initial de l'animal.
        self.__age = 0

        # Sexe attribué aléatoirement : 0 ou 1.
        self.__gender = random.randint(0, 1)

        # Barre de vie : [points de vie actuels, points de vie maximum].
        self.__bar_life = [life_max, life_max]

        # Génération aléatoire de la direction initiale de déplacement.
        liste = [-1, 0, 1]
        x = random.choice(liste)

        # Évite que les deux coordonnées soient nulles :
        # l'animal doit avoir une direction de déplacement.
        if x == 0:
            res = [-1, 1]
            y = random.choice(res)
        else:
            y = random.choice(liste)

        self.__current_direction = [x, y]

    def get_age(self):
        # Retourne l'âge actuel de l'animal.
        return self.__age

    def ageing(self, years=1):
        """
        Ajoute le nombre d'années indiqué à l'âge de l'animal.
        Par défaut, l'âge augmente d'une année.
        """
        self.age += years

    def get_gender(self):
        # Retourne le sexe de l'animal.
        return self.__gender

    def get_life_max(self):
        # Retourne le nombre maximal de points de vie.
        return self.__life_max

    def get_life(self):
        # Retourne les points de vie actuels.
        return self.__bar_life[0]

    def is_alive(self):
        # Vérifie si l'animal possède encore des points de vie.
        return self.__bar_life[0] > 0

    def is_dead(self):
        # Vérifie si l'animal n'a plus aucun point de vie.
        return self.__bar_life[0] == 0

    def recovering_life(self, value):
        # Augmente les points de vie si l'animal n'a pas atteint son maximum.
        if self.__bar_life[0] < self.__bar_life[1]:
            self.__bar_life[0] += value

    def losing_life(self, value):
        # Diminue les points de vie sans passer sous zéro.
        if self.__bar_life[0] - value > 0:
            self.__bar_life[0] -= value

    def get_current_direction(self):
        # Retourne la direction actuelle de déplacement.
        return self.__current_direction

    def set_current_direction(line_direction, column_direction):
        # Modifie la direction uniquement si les deux coordonnées
        # appartiennent à l'ensemble {-1, 0, 1}.
        liste = [-1, 0, 1]
        if column_direction in liste and line_direction in liste:
            res = [line_direction, column_direction]
            self.__current_direction = deepcopy(res)


class Cow(Animal):
    """Animal représentant une vache."""

    def __init__(self):
        # Une vache possède 100 points de vie maximum.
        super().__init__('\U0001F42E', 100)


class Dragon(Animal):
    """Animal représentant un dragon."""

    def __init__(self):
        # Un dragon possède 1000 points de vie maximum.
        super().__init__('\U0001F432', 1000)


class Lion(Animal):
    """Animal représentant un lion."""

    def __init__(self):
        # Un lion possède 500 points de vie maximum.
        super().__init__('\U0001F981', 500)


class Mouse(Animal):
    """Animal représentant une souris."""

    def __init__(self):
        # Une souris possède 10 points de vie maximum.
        super().__init__('\U0001F42D', 10)


class Ground(Element):
    """Élément représentant le sol, sans symbole visible."""

    def __init__(self):
        super().__init__('')


if __name__ == '__main__':
    # Quelques tests de représentation et de comparaison des objets Ground.
    print(Ground(), str(Ground()))
    print(Ground() == str(Ground()))
    print(Ground() == Ground())
    print(Ground() is Ground())
