from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

app = Ursina()

# textures path setting
textures = {
    'unknown': 'white_cube',
    'grass': 'textures/grass.png',
    'dirt': 'textures/dirt.png',
    'stone': 'textures/cobblestone.png',
    'endstone': 'textures/end_stone_bricks.png',
    'planks': 'textures/oak_planks.png',
    'sand': 'textures/sand.png',
#    'bedrock': 'textures/bedrock.png',
    'command_block': 'textures/command_block_back.png',
    'wood': 'textures/oak_log.png',
    
}


#voxel class
class Voxel(Button):
    def __init__(self, position=(0,0,0), texture=textures['unknown']):
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture=texture,
            color='#ffffff',
            highlight_color=color.green,
            shader=lit_with_shadows_shader,
        )


# starting platform
for z in range(-10,10):
    for x in range(-10,10):
        voxel = Voxel(position=(x,0,z), texture=textures['grass'])

# keys input
def input(key): 
    # blocks placing and destroying
    global actual_block
    if key == 'right mouse down':
        hit_info = raycast(camera.world_position, camera.forward)
        if hit_info.hit:
            try:
                Voxel(position=hit_info.entity.position + hit_info.normal, texture=textures[actual_block])
            except Exception:
                Voxel(position=hit_info.entity.position + hit_info.normal, texture=textures['grass'])
    if key == 'left mouse down' and mouse.hovered_entity:
        b = mouse.hovered_entity
        destroy(mouse.hovered_entity)

        
    '''# block types switching
    match key:
        case '1': actual_block = 'grass'
        case '2': actual_block = 'dirt'
        case '3': actual_block = 'stone'
        case '4': actual_block = 'planks'
        case '5': actual_block = 'sand'
        case '5': actual_block = 'endstone'
        case '6': actual_block = 'wood'
        case '9': actual_block = 'command_block'''

# game loop
def update():
    if player.y < -50: player.position = (0,5,0) #player respawns when falling

player = FirstPersonController() # adding player
#actual_block = 'grass'

sun = DirectionalLight(shadows=True) # adding sun
sun.look_at(Vec3(1,-1,-1)) # sun direction
Sky() # adding sky



app.run()
