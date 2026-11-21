
from Element import *
from planetalphatk_snake import *


class Snake(Element):
    """
    Classe représentant le serpent dans le jeu.

    Attributs :
        NORTH, EAST, SOUTH, WEST : directions possibles du serpent.
        __body : liste des coordonnées des cases occupées par le serpent.
        __size : taille actuelle du serpent.
        __speed : vitesse du serpent.
        __direction : direction actuelle du déplacement.
        __running : indique si le serpent est en mouvement.
        __grow : nombre de segments supplémentaires à ajouter.
        __canvas : zone graphique sur laquelle dessiner le serpent.
        __cell_size : dimension d'une cellule du plateau.

    Auteur : Mame Thierno Sarr.
    """

    # Directions possibles : (déplacement vertical, déplacement horizontal).
    NORTH, EAST, SOUTH, WEST = (-1, 0), (0, 1), (1, 0), (0, -1)

    def __init__(self, size, speed, canvas, cell_size):
        """
        Initialise le serpent avec sa taille, sa vitesse et sa direction initiale.

        Paramètres :
            size : taille initiale du serpent.
            speed : vitesse initiale du serpent.
            canvas : zone graphique sur laquelle dessiner le serpent.
            cell_size : taille de chaque cellule du plateau.
        """
        super().__init__('')

        # Initialise le corps du serpent sur une même ligne.
        # Chaque segment est représenté par un couple (ligne, colonne).
        self.__body = [(7, i) for i in range(size - 1, -1, -1)]

        self.__size = size
        self.__speed = speed

        # Le serpent commence en se dirigeant vers la droite.
        self.__direction = self.EAST

        self.__running = False
        self.__grow = 0
        self.__canvas = canvas
        self.__cell_size = cell_size

    def get_size(self):
        """Retourne la taille actuelle du serpent."""
        return self.__size

    def get_speed(self):
        """Retourne la vitesse actuelle du serpent."""
        return self.__speed

    def get_direction(self):
        """Retourne la direction actuelle sous la forme (ligne, colonne)."""
        return self.__direction

    def get_running(self):
        """Indique si le serpent est actuellement en mouvement."""
        return self.__running

    def get_grow(self):
        """Retourne le nombre de segments supplémentaires à ajouter."""
        return self.__grow

    def turn_left(self):
        """Change la direction du serpent pour effectuer un virage à gauche."""

        if self.__direction == self.NORTH:
            self.__direction = self.WEST
        elif self.__direction == self.WEST:
            self.__direction = self.SOUTH
        elif self.__direction == self.SOUTH:
            self.__direction = self.WEST
        elif self.__direction == self.EAST:
            self.__direction = self.NORTH

    def turn_right(self):
        """Change la direction du serpent pour effectuer un virage à droite."""

        if self.__direction == self.NORTH:
            self.__direction = self.EAST
        elif self.__direction == self.EAST:
            self.__direction = self.SOUTH
        elif self.__direction == self.SOUTH:
            self.__direction = self.EAST
        elif self.__direction == self.WEST:
            self.__direction = self.NORTH

    def grow(self, eat=1):
        """
        Prévoit l'agrandissement du serpent après avoir mangé.

        Paramètre :
            eat : nombre de segments supplémentaires à ajouter.
        """
        self.__grow += eat

    def draw(self):
        """Dessine le serpent sur le Canvas Tkinter."""

        # Supprime l'ancien dessin du serpent avant de le redessiner.
        self.__canvas.delete("snake")

        # Parcourt les segments du corps pour dessiner chaque cellule.
        for i, (row, col) in enumerate(self.__body):
            # Conversion des coordonnées de la grille en pixels.
            x1 = col * self.__cell_size
            y1 = row * self.__cell_size
            x2 = x1 + self.__cell_size
            y2 = y1 + self.__cell_size

            # La tête possède une couleur différente du reste du corps.
            color = "#1a7a1a" if i == 0 else "#2ecc40"
            outline = "#145214" if i == 0 else "#27ae60"

            self.__canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline=outline,
                width=2,
                tags="snake"
            )


class Food(Element):
    """Classe représentant la nourriture du serpent."""

    def __init__(self):
        """Initialise la nourriture avec une représentation en forme de pomme."""
        Element.__init__(self, '\U0001F34E')


class Trap(Element):
    """Classe représentant un piège dans le jeu."""

    def __init__(self):
        """Initialise un piège avec une représentation en forme de bombe."""
        Element.__init__(self, '\U0001F4A3')


class SnakeGame(PlanetTk):
    """
    Classe principale représentant le jeu Snake.

    Elle hérite de PlanetTk afin de réutiliser le plateau graphique
    et les fonctionnalités de gestion des cellules.

    Attributs :
        __root : fenêtre principale de l'application.
        __lines : nombre de lignes du plateau.
        __cols : nombre de colonnes du plateau.
        __running : indique si une partie est en cours.
        __speed : délai entre deux déplacements du serpent.
        __snake : objet représentant le serpent.
        __b_frame : zone contenant les boutons de contrôle.
        __b_start : bouton permettant de commencer la partie.
        __b_quit : bouton permettant de quitter le jeu.
        __score : étiquette affichant le score et la vitesse.
    """

    def __init__(self, root, lines=15, cols=15, cell_size=40):
        """
        Initialise le jeu Snake et ses composants graphiques.

        Paramètres :
            root : fenêtre principale Tkinter.
            lines : nombre de lignes du plateau.
            cols : nombre de colonnes du plateau.
            cell_size : dimension des cellules en pixels.
        """

        # Initialise le plateau hérité de PlanetTk.
        PlanetTk.__init__(
            self,
            root=root,
            name="SnakeWorld",
            latitude_cells_count=lines,
            longitude_cells_count=cols,
            authorized_classes=[Snake, Food, Trap],
            cell_size=cell_size
        )

        self.__root = root
        self.__lines = lines
        self.__cols = cols
        self.__running = False

        # Le délai initial entre deux déplacements est de 200 ms.
        self.__speed = 200
        self.__cell_size = cell_size

        # Création du serpent avec une taille initiale de 5 segments.
        self.__snake = Snake(size=5, speed=3, canvas=self, cell_size=cell_size)

        # Création de la zone contenant les boutons.
        self.__b_frame = tk.Frame(root)
        self.__b_frame.pack()

        # Bouton de démarrage.
        self.__b_start = tk.Button(
            self.__b_frame,
            text="Commencer",
            width=12,
            command=self.__start
        )
        self.__b_start.grid(row=0, column=0, padx=5, pady=5)

        # Bouton permettant de fermer la fenêtre.
        self.__b_quit = tk.Button(
            self.__b_frame,
            text="Quitter",
            width=12,
            command=root.destroy
        )
        self.__b_quit.grid(row=0, column=1, padx=5, pady=5)

        # Affichage initial de la taille et de la vitesse.
        self.__score = tk.Label(
            root,
            text="Taille : 5  |  Vitesse : 3",
            font=("Arial", 12)
        )
        self.__score.pack()

        # Bouton permettant de recommencer une partie.
        self.__b_restart = tk.Button(
            self.__b_frame,
            text="Recommencer",
            width=12,
            command=self.restart_game
        )
        self.__b_restart.grid(row=0, column=2, padx=5, pady=5)

        # Association des touches directionnelles aux changements de direction.
        root.bind("<Left>", lambda e: self.__snake.turn_left())
        root.bind("<Right>", lambda e: self.__snake.turn_right())

        # Placement initial de deux nourritures et d'un piège.
        self.spawn_food()
        self.spawn_food()
        self.spawn_trap()

    def __snake_to_cells(self):
        """
        Convertit les coordonnées des segments du serpent en numéros de cellules.

        Cela permet de comparer facilement les positions du serpent
        avec les numéros des cellules du plateau.
        """

        return [
            self.get_cell_number_from_coordinates(line, col)
            for line, col in self.__snake._Snake__body
        ]

    def spawn_food(self):
        """Fait apparaître une nourriture sur une cellule libre choisie aléatoirement."""

        cell = self.get_random_free_place()

        # Vérifie qu'une cellule libre a bien été trouvée.
        if cell != -1:
            self.born(cell, Food())

    def spawn_trap(self):
        """Fait apparaître un piège sur une cellule libre choisie aléatoirement."""

        cell = self.get_random_free_place()

        if cell != -1:
            self.born(cell, Trap())

    def __start(self):
        """Démarre la partie si aucune partie n'est déjà en cours."""

        if not self.__running:
            self.__running = True

            # Modifie le texte du bouton pour indiquer que la partie a commencé.
            self.__b_start.config(text="jeu en cours...")

            # Lance la première étape du jeu.
            self.__step()

    def __step(self):
        """
        Effectue une étape du jeu.

        Cette méthode gère :
            - Le déplacement du serpent.
            - Les collisions avec les bords et son propre corps.
            - La consommation de nourriture.
            - Les conséquences des pièges.
            - La mise à jour de la taille, de la vitesse et du score.
        """

        # Arrête l'exécution si la partie n'est plus active.
        if not self.__running:
            return None

        # Récupère la position de la tête et la direction actuelle.
        head = self.__snake._Snake__body[0]
        direction = self.__snake.get_direction()

        # Calcule les coordonnées de la prochaine position de la tête.
        new_line = head[0] + direction[0]
        new_col = head[1] + direction[1]

        # Vérifie si le serpent sort des limites du plateau.
        if not (0 <= new_line < self.__lines and 0 <= new_col < self.__cols):
            self.__game_over()
            return None

        # Convertit les coordonnées de la nouvelle position en numéro de cellule.
        new_cell = PlanetAlpha.get_cell_number_from_coordinates(self, new_line, new_col)

        # Vérifie si la nouvelle position est déjà occupée par le serpent.
        if new_cell in self.__snake_to_cells():
            self.__game_over()
            return None

        # Récupère le contenu de la prochaine cellule.
        content = self.get_cell(new_cell)

        # Cas où le serpent mange une nourriture.
        if isinstance(content, Food):
            self.die(new_cell)

            # Prévoit un segment supplémentaire et augmente la vitesse affichée.
            self.__snake._Snake__grow += 1
            self.__snake._Snake__speed += 1

            # Réduit le délai entre les déplacements, avec une limite minimale de 50 ms.
            self.__speed = max(50, self.__speed - 20)

            # Remplace la nourriture consommée et fait apparaître un piège.
            self.spawn_food()
            self.spawn_trap()

        # Cas où le serpent rencontre un piège.
        elif isinstance(content, Trap):
            self.die(new_cell)

            # Si le serpent possède plusieurs segments, il en perd un.
            if len(self.__snake._Snake__body) > 1:
                tail_row, tail_col = self.__snake._Snake__body[-1]

                # Augmente le délai entre les déplacements.
                self.__speed = self.__speed + 10

                # Supprime la dernière partie du corps du serpent.
                self.die(tail_row * self.__cols + tail_col)
                self.__snake._Snake__body.pop()
                self.__snake._Snake__size -= 1

                # Fait apparaître un nouveau piège.
                self.spawn_trap()
            else:
                # La partie se termine si le serpent ne peut plus perdre de segment.
                self.__game_over()
                return None

        # Ajoute la nouvelle position au début du corps : elle devient la tête.
        self.__snake._Snake__body.insert(0, (new_line, new_col))
        self.born(new_cell, self.__snake)

        # Si le serpent doit grandir, on conserve son dernier segment.
        if self.__snake._Snake__grow > 0:
            self.__snake._Snake__grow -= 1
        else:
            # Sinon, on retire le dernier segment pour conserver la même taille.
            tail_line, tail_col = self.__snake._Snake__body[-1]
            self.die(
                PlanetAlpha.get_cell_number_from_coordinates(self, tail_line, tail_col)
            )
            self.__snake._Snake__body.pop()

        # Met à jour la taille réelle du serpent.
        self.__snake._Snake__size = len(self.__snake._Snake__body)

        # Redessine les éléments du plateau et le serpent.
        self.draw_elements()
        self.__snake.draw()

        # Actualise les informations affichées à l'écran.
        self.__score.config(
            text=f"score : {self.__snake.get_size()}  |  Vitesse : {self.__snake.get_speed()}"
        )

        # Programme la prochaine étape après le délai défini.
        self.after(self.__speed, self.__step)

    def __game_over(self):
        """Met fin à la partie et affiche un message de fin."""

        self.__running = False

        # Efface le contenu graphique avant d'afficher le message.
        self.delete("all")

        self.create_text(
            self.__cols * self.__cell_size // 2,
            self.__lines * self.__cell_size // 2,
            text="GAME OVER \n NOOB HAHA",
            fill="red",
            font=("Arial", 36, "bold")
        )

        # Désactive le bouton de démarrage après la fin de la partie.
        self.__b_start.config(state=tk.DISABLED, text="jeu terminé...")

    def clear_all_except_ground(self):
        """
        Supprime tous les éléments du plateau, sauf les éléments de type Ground.
        """

        # Parcourt toutes les cellules du plateau.
        for i in range(self.__lines):
            for j in range(self.__cols):
                cell = PlanetAlpha.get_cell_number_from_coordinates(self, i, j)
                content = self.get_cell(cell)

                # Supprime uniquement les éléments qui ne sont pas du sol.
                if not isinstance(content, Ground):
                    self.die(cell)

    def restart_game(self):
        """Réinitialise les variables et les éléments pour recommencer une partie."""

        # Crée un nouveau serpent avec ses caractéristiques initiales.
        self.__snake = Snake(size=5, speed=3, canvas=self, cell_size=self.__cell_size)

        self.__running = False
        self.__speed = 200

        # Réactive le bouton de démarrage et réinitialise les affichages.
        self.__b_start.config(state=tk.NORMAL, text="Commencer")
        self.__score.config(text="score : 5  |  Vitesse : 3")

        # Efface le dessin et supprime les anciens éléments du plateau.
        self.delete("all")
        self.clear_all_except_ground()

        # Replace les éléments initiaux.
        self.spawn_food()
        self.spawn_food()
        self.spawn_trap()

        # Programme une étape du jeu.
        self.after(self.__speed, self.__step)
