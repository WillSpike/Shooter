# collisions.py
def check_collision(enemy, bullet):
    hit = (
        bullet.x + bullet.size >= enemy.x
        and bullet.x <= enemy.x + enemy.size
        and bullet.y + bullet.size >= enemy.y
        and bullet.y <= enemy.y + enemy.size
    )
    if hit:
        bullet.hit = True
    return hit
