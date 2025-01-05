from ursina import *
from perlin_noise import PerlinNoise
from ursina.prefabs.first_person_controller import FirstPersonController


print('Enter world seed:')
seed_input = int(input())
world = PerlinNoise(seed=seed_input)
app = Ursina()

class Voxel(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(parent=scene,
                         position=position,
                         model='cube',
                         origin_y=.5,
                         texture='white_cube',
                         color=color.hsv(0, 0, random.uniform(.9, 1.0)),
                         highlight_color=color.lime)

for z in range(-20,20):
    for x in range(-20,20):
        noise_value = world([x / 5, z / 5])
        y = int(noise_value * 10) + 1
        voxel = Voxel(position=(x, y, z))
        for y_fill in range(y - 1, -3, -1):
            Voxel(position=(x, y_fill, z))

def input(key):
    if key == 'left mouse down' and mouse.hovered_entity:
        destroy(mouse.hovered_entity)
    if key == 'right mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
            Voxel(position=hit_info.entity.position + hit_info.normal)

def update():
    if player.y < -50: player.position = (0,25,0)

player = FirstPersonController(y=25)
app.run()
