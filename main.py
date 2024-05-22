import random
import pyxel
from effects_particules import Particle, ExplosionParticle
from menu import Menu
from collisions import check_collision

class MainBullet(Particle):
    def __init__(self, x, y):
        super().__init__(x, y, 0, -4, 30, 7, 2)  # Tir principal centré
        self.is_dead = False
       
class SideBullet(Particle):
    def __init__(self, x, y, speed_x, color):
        super().__init__(x, y, speed_x, -4, 30, color, size=1)  # Tirs latéraux avec une couleur différente
        self.is_dead = False

class Player:
    def __init__(self, x, y):        
        self.x = x
        self.y = y
        self.bullets = [] 
        self.score = 0  

    def update(self, enemies):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 2
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= 2
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += 2
        if pyxel.btnp(pyxel.KEY_X):  
            self.shoot_side()
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.shoot_main()

        self.bullets = [bullet for bullet in self.bullets if not bullet.hit]
        self.update_bullets(enemies)

    def update_bullets(self, enemies):
        for bullet in self.bullets:
            bullet.update()
            if bullet.x > pyxel.width or bullet.y < 0:
                bullet.is_dead = True

    def shoot_main(self):
        main_bullet = MainBullet(self.x + 7, self.y)  
        main_bullet.hit = False
        self.bullets.append(main_bullet)

    def shoot_side(self):       
        side_bullet_left = SideBullet(self.x + 1, self.y + 6, -2, 11)              
        side_bullet_right = SideBullet(self.x + 15, self.y + 6, 2, 11)
        side_bullet_left.hit = False
        side_bullet_right.hit = False
        self.bullets.extend([side_bullet_left, side_bullet_right])  

    def draw(self):       
        pyxel.blt(self.x, self.y, 0, 0, 0, 16, 16, 1)
        for bullet in self.bullets:
            bullet.draw()      
        pyxel.text(5, 5, f"Score: {self.score}", pyxel.COLOR_WHITE)        

class Enemy:
    def __init__(self, x, y, speed_x, speed_y, size, color):               
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.size = size
        self.color = color
        self.frame_index = 0
        self.frame_counter = 0  
        self.is_dead = False    

    def update(self):     
        self.x += self.speed_x
        self.y += self.speed_y    
        self.frame_counter += 1
        if self.frame_counter % 8 == 0:
            self.frame_index = (self.frame_index + 1) % 4
            self.frame_counter = 0

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.frame_index * 16, 16, -16, -16, 0) 

class Game:
    def __init__(self):
        pyxel.init(256, 192, title="Simple Shooter", fps=60)
        pyxel.load("SHOOTER.pyxres")       
        self.player = Player(100, 150)
        self.enemies = []
        self.frame_count = 0
        self.game_over = False
        self.state = 'menu'
        self.menu = Menu()  
        self.explosions = [] 
      
    def update(self):
        if self.state == 'menu':
            action = self.menu.update()
            if action == 'play':
                self.state = 'play'               
            elif action == 'scores':
                self.state = 'scores'
            elif action == 'quit':
                self.state = 'quit'
                pyxel.quit()                   

        elif self.state == 'play':
            if not self.game_over:
                self.player.update(self.enemies)

                # Mettre à jour les ennemis
                for enemy in self.enemies:
                    enemy.update()

                self.handle_collisions()
                self.update_explosions()

                self.frame_count += 1
                if self.frame_count % 60 == 0:
                    self.add_enemy()

                if self.check_player_collision():
                    self.game_over = True         
            else:
                if pyxel.btnp(pyxel.KEY_R):
                    self.restart()
                if pyxel.btnp(pyxel.KEY_M):
                    self.state = 'menu'
                    self.restart()

        elif self.state == 'scores':
            pass     

    def handle_collisions(self):
        for bullet in self.player.bullets:
            bullet.update()
            if bullet.x > pyxel.width or bullet.y < 0:
                bullet.is_dead = True
            else:
                for enemy in self.enemies:
                    if check_collision(enemy, bullet):
                        bullet.is_dead = True
                        enemy.is_dead = True
                        explosion = ExplosionParticle(enemy.x, enemy.y, num_particles=20)
                        self.explosions.append(explosion)
                        self.player.score += 1

        self.player.bullets = [bullet for bullet in self.player.bullets if not bullet.is_dead]
        self.enemies = [enemy for enemy in self.enemies if not enemy.is_dead]

    def update_explosions(self):
        for explosion in self.explosions:
            explosion.update()

    def restart(self):
        self.player = Player(100, 150)
        self.enemies = []
        self.explosions = []
        self.frame_count = 0 
        self.game_over = False
        self.score = 0

    def add_enemy(self):
        x = random.randint(0, pyxel.width - 10)
        y = 0
        speed_x = random.choice([-1, 1])
        speed_y = random.uniform(0.5, 1) 
        size = 10
        color = 8
        new_enemy = Enemy(x, y, speed_x, speed_y, size, color)
        self.enemies.append(new_enemy)

    def check_player_collision(self) -> bool:
        for enemy in self.enemies:
            if (
                self.player.x + 16 >= enemy.x
                and self.player.x <= enemy.x + enemy.size
                and self.player.y + 16 >= enemy.y
                and self.player.y <= enemy.y + enemy.size
            ):
                return True
        return False

    def draw(self):
        pyxel.cls(0)
        if self.state == 'menu':           
            self.menu.draw()
        elif self.state == 'play':
            self.player.draw()                
            for enemy in self.enemies:
                enemy.draw() 
            for explosion in self.explosions:
                explosion.draw()
            if self.game_over:
                pyxel.text(100, 86, "Score: " + str(self.player.score), pyxel.COLOR_GREEN)
                pyxel.text(100, 96, "GAME OVER", pyxel.COLOR_RED)
                pyxel.text(80, 106, "Press R to Restart", pyxel.COLOR_WHITE)
                pyxel.text(80, 116, "Press M to Menu", pyxel.COLOR_WHITE)
                
game = Game()
pyxel.run(game.update, game.draw)
