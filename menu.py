# Menu.py
import pyxel
class Menu:
    def __init__(self):
        self.option = 0  # Option actuel

    def update(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.option = max(0, self.option - 1)  # Déplacer l'option vers le haut
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.option = min(2, self.option + 1)  # Déplacer l'option vers le bas
        elif pyxel.btnp(pyxel.KEY_RETURN )or pyxel.btnp(pyxel.KEY_KP_ENTER): 
            if self.option == 0:  # Jouer
                return 'play'
            elif self.option == 1:  # Scores
                return 'scores'
            elif self.option == 2:  # Quitter
                return 'quit'

    def draw(self):
        pyxel.cls(0)
        pyxel.text(100, 45, "Jouer", pyxel.COLOR_WHITE if self.option != 0 else pyxel.COLOR_YELLOW)
        pyxel.text(100, 55, "Scores", pyxel.COLOR_WHITE if self.option != 1 else pyxel.COLOR_YELLOW)
        pyxel.text(100, 65, "Quitter", pyxel.COLOR_WHITE if self.option != 2 else pyxel.COLOR_YELLOW)
