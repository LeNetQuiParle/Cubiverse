from ursina import *
from random import randint
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from perlin_noise import PerlinNoise
import trees

seed_input = randint(1,1000)
world = PerlinNoise(seed=seed_input)

app = Ursina(title='Cubiverse',
  icon='icon.ico',
  fullscreen=True,
  editor_ui_enabled=False,
  development_mode=False,
  show_ursina_splash=True,)

textures = {
  'unknown': 'white_cube',
  'grass': 'textures/grass.png',
  'dirt': 'textures/dirt.png',
  'stone': 'textures/cobblestone.png',
  'planks': 'textures/oak_planks.png',
  'sand': 'textures/sand.png',
  'wood': 'textures/oak_log.png',
  'cursor': 'textures/cursor.png',
  'player': 'textures/player.png',
  'leaves': 'textures/oak_leaves.png'
    
}



step_timer = 0.0
step_interval = 0.5

class Actionbar(Entity):
    def __init__(self, width=10, height=1, **kwargs):
        super().__init__(
            parent = camera.ui,
            model = Quad(radius=.015),
            texture = 'white_cube',
            texture_scale = (width, height),
            scale = (width*.1, height*.1),
            origin = (0,0),
            position = (0,-.4),
            color = color.hsv(0, 0, .1, .9),
            )

        self.width = width
        self.height = height

        for key, value in kwargs.items():
            setattr(self, key, value)


    def find_free_spot(self):
        for y in range(self.height):
            for x in range(self.width):
                grid_positions = [(int(e.x*self.texture_scale[0]), int(e.y*self.texture_scale[1])) for e in self.children]


                if not (x, -y) in grid_positions:
                    return x, y


    def append(self, item, x=0, y=0):


        x, y = self.find_free_spot()

        icon = Draggable(
            parent = self,
            model = 'quad',
            texture = textures[item].replace('.png', '_item.png'),
            color = color.white,
            scale_x = 1/self.texture_scale[0],
            scale_y = 1/self.texture_scale[1],
            origin = (4.5,0),
            x = x * 1/self.texture_scale[0],
            y = -y * 1/self.texture_scale[1],
            z = -.5,
            )
        name = item.replace('_', ' ').title()

        icon.tooltip = Tooltip(name)
        icon.tooltip.background.color = color.hsv(0,0,0,.8)


        def drag():
            icon.org_pos = (icon.x, icon.y)
            icon.z -= .01

        def drop():
            icon.x = int((icon.x + (icon.scale_x/2)) * self.width) / self.width
            icon.y = int((icon.y - (icon.scale_y/2)) * self.height) / self.height
            icon.z += .01

            if icon.x < 0 or icon.x >= 1 or icon.y > 0 or icon.y <= -1:
                icon.position = (icon.org_pos)
                return

            for c in self.children:
                if c == icon:
                    continue

                if c.x == icon.x and c.y == icon.y:
                    c.position = icon.org_pos

        icon.drag = drag
        icon.drop = drop

class Voxel(Button):
  def __init__(self, position=(0,0,0), texture='unknown'):
    super().__init__(
      parent=scene,
      position=position,
      model='cube',
      origin_y=.5,
      texture=textures[texture],
      color='#ffffff',
      highlight_color=color.green,
      shader=lit_with_shadows_shader,
    )


for z in range(-10, 10):
  for x in range(-10, 10):
    noise_value = world([x / 20, z / 20])
    y = int(noise_value * 10) + 1
    voxel = Voxel(position=(x, y, z), texture='grass')
    if randint(1,300) == 1:
      trees.oak_tree(x,y,z)
    for y_fill in range(y - 1, y - 3, -1):
      if y_fill > -3:
        Voxel(position=(x, y_fill, z), texture='dirt')
    for y_fill in range(y - 3, -3, -1):
      Voxel(position=(x, y_fill, z), texture='stone')


def input(key): 
  global actual_block, view, player, player_graphics
  if key == 'right mouse down':
    hit_info = raycast(camera.world_position, camera.forward, ignore=[player, player_graphics], debug=True)
    if hit_info.hit:
      Voxel(position=hit_info.entity.position + hit_info.normal, texture=actual_block)
      textur=textures[actual_block]
      textur=str(textur)
      textur=textur.replace('textures/','')
      textur=textur.replace('.png','')
      Audio(f'sounds/blocks/{textur}{randint(1,4)}.ogg')
  if key == 'left mouse down' and mouse.hovered_entity:
    if not mouse.hovered_entity == player:
      textur=mouse.hovered_entity.texture
      textur=str(textur)
      textur=textur.replace('.png', '')
      Audio(f'sounds/blocks/{textur}{randint(1,4)}.ogg')
      destroy(mouse.hovered_entity)

  match key:
    case '0': actual_block = 'grass'
    case '1': actual_block = 'dirt'
    case '2': actual_block = 'stone'
    case '3': actual_block = 'planks'
    case '4': actual_block = 'wood'
    case '5': actual_block = 'leaves'
    case '6': actual_block = 'sand'

  if key == 'tab':
    if view == 1:
      camera.z = -5
      view = 3
      player_graphics.visible_self = True
    elif view == 3:
      camera.z = 0
      view = 1
      player_graphics.visible_self = False

  if key == 'escape':
    mouse.locked = not mouse.locked


def update():
  global step_timer, step_interval
  if player.y < -50: player.position = (0,11,0)
  
  if (held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']) and player.grounded:
    step_timer -= time.dt
    if step_timer <= 0:
      Audio(f'sounds/step/grass{randint(1,6)}.ogg')
      step_timer = step_interval

player = FirstPersonController(
  speed=6,
  y=11,
  model='cube',
  collider='box',
  origin_y=-.5,
)
destroy(player.cursor)
player.cursor = Entity(parent=camera.ui, model='cube', color=color.white, texture=textures['cursor'], scale=.05,)
player.visible_self = False
player_graphics = Entity(
  parent=player,
  model='cube',
  scale_y=1.85,
  origin_y=-.5,
  texture=textures['player'],
  shader=lit_with_shadows_shader,
)

player_graphics.visible_self=False

actionbar = Actionbar()
actionbar.append('grass')
actionbar.append('dirt')
actionbar.append('stone')
actionbar.append('planks')
actionbar.append('wood')
actionbar.append('leaves')
actionbar.append('sand')

actual_block = 'grass'

view = 1

sun = DirectionalLight(shadows=False)
sun.look_at(Vec3(1,-1,-1))
Sky()



app.run()
