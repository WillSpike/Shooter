import pyxel 
import math
import random
# Effect_particules.py 
class Particle:
    def __init__(self, x, y, speed_x, speed_y, lifetime, color=7, size=1, gravity=0):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.lifetime = lifetime
        self.color = color 
        self.size = size
        self.gravity = gravity

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y + self.gravity
        self.lifetime -= 0.5

        # Diminuer progressivement la taille de la particule
        self.size = max(self.size - 0.4, 1)      

    def draw(self):
        if self.lifetime > 0:
            pyxel.rect(self.x, self.y, self.size, self.size, self.color)

class ExplosionParticle:
    def __init__(self, x, y, num_particles=10):
        self.particles = []        
        for _ in range(num_particles):
            angle = random.uniform(0, 2*math.pi)    # Angle aléatoire en radians
            speed = random.uniform(1, 3)            # Vitesse aléatoire
            speed_x = speed * math.cos(angle)
            speed_y = speed * math.sin(angle)            
            particle = Particle(x, y, speed_x, speed_y, lifetime=30, color=random.randint(0, 15), size=2, gravity=0.1)
            self.particles.append(particle)

    def update(self):
        for particle in self.particles:
            particle.update()

    def draw(self):
        for particle in self.particles:
            particle.draw()

class ParticleLogarithmic(Particle):
    def __init__(self, x, y, theta, a=1, b=0.1, color=8, size=2):
        super().__init__(x, y, 0, 0, 100, color, size)  
        self.theta = theta
        self.a = a
        self.b = b
        self.center_x = x
        self.center_y = y

    def update(self):
        self.theta += 0.5  # Augmenter l'angle pour faire tourner la spirale
        self.x = self.center_x + self.a * math.cos(self.theta) * math.exp(self.b * self.theta)
        self.y = self.center_y + self.a * math.sin(self.theta) * math.exp(self.b * self.theta)
        self.lifetime -= 0.5
