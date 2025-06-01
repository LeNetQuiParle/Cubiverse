from ursina import *
from ursina.shaders import lit_with_shadows_shader

class Voxel(Button):
  def __init__(self, position=(0,0,0), texture='wood'):
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

textures = {
  'wood': 'textures/oak_log.png',
  'leaves': 'textures/oak_leaves.png'
}

tree_wood = [(0,0,0),(0,1,0),(0,2,0),(0,3,0),(0,4,0)]
tree_leaves = [
  (-2,2,-2),(-1,2,-2),(0,2,-2),(1,2,-2),(2,2,-2),
  (-2,2,-1),(-1,2,-1),(0,2,-1),(1,2,-1),(2,2,-1),
  (-2,2,0),(-1,2,0),(1,2,0),(2,2,0),
  (-2,2,1),(-1,2,1),(0,2,1),(1,2,1),(2,2,1),
  (-2,2,2),(-1,2,2),(0,2,2),(1,2,2),(2,2,2),
  (-2,3,-2),(-1,3,-2),(0,3,-2),(1,3,-2),(2,3,-2),
  (-2,3,-1),(-1,3,-1),(0,3,-1),(1,3,-1),(2,3,-1),
  (-2,3,0),(-1,3,0),(1,3,0),(2,3,0),
  (-2,3,1),(-1,3,1),(0,3,1),(1,3,1),(2,3,2),
  (-2,3,2),(-1,3,2),(0,3,2),(1,3,2),(2,2,2),

  (-1,4,-1),(0,4,-1),(1,4,-1),(-1,4,0),
  (1,4,0),(-1,4,1),(0,4,1),(1,4,1),
  
  (0,5,1),(-1,5,0),(0,5,0),(1,5,0),(0,5,-1)
]

def oak_tree(x, y, z):
  for block in tree_wood:
    Voxel(position=(block[0] + x,block[1] + (y + 1),block[2] + z), texture='wood')
  for block in tree_leaves:
    Voxel(position=(block[0] + x,block[1] + (y + 1),block[2] + z), texture='leaves')

