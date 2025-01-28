from ursina import *

textures = {
  'unknown': 'white_cube',
  'grass': 'textures/grass.png',
  'dirt': 'textures/dirt.png',
  'stone': 'textures/cobblestone.png',
  'planks': 'textures/oak_planks.png',
  'sand': 'textures/sand.png',
  'wood': 'textures/oak_log.png',
  'leaves': 'textures/oak_leaves.png'
    
}

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
