
import tkinter as tk
from projet_snakeGame import *


class MyApp(tk.Tk):
    """
    Classe représentant la fenêtre principale de l'application.

    Elle hérite de tk.Tk afin de bénéficier des fonctionnalités
    de création et de gestion d'une fenêtre Tkinter.
    """

    def __init__(self, game, title, **kw):
        """
        Initialise la fenêtre principale.

        Paramètres :
            game : classe du jeu à utiliser dans l'application.
            title : titre affiché dans la barre de la fenêtre.
            **kw : paramètres supplémentaires transmis à la fenêtre Tkinter.
        """

        # Initialise la fenêtre Tkinter.
        super().__init__(**kw)

        # Conserve une référence à la classe du jeu.
        self.__game = game

        # Définit le titre de la fenêtre.
        self.title(title)

    def start(self):
        """Lance la boucle principale de l'application Tkinter."""
        self.mainloop()

    def get_current_game(self):
        """Retourne la classe du jeu associée à l'application."""
        return self.__game


if __name__ == '__main__':
    # Crée la fenêtre principale avec SnakeGame comme jeu associé.
    root = MyApp(SnakeGame, "snake")

    # Instancie le jeu dans la fenêtre principale.
    game = SnakeGame(root)

    # Lance l'application.
    root.start()
