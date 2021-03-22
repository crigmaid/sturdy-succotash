"""
Platformer Game
"""
import arcade
import math

# Constants
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 200
RIGHT_VIEWPORT_MARGIN = 500
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 200

PLAYER_START_X = 350
PLAYER_START_Y = 500


class Game(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.level = 1
        self.sprite_lists_map = {}
        self.player_sprite = None
        self.player_sprite_list = arcade.SpriteList()
        self.player_physics_engine = None
        self.is_on_a_platform = False
        self.enemy_sprite = None
        self.enemy_sprite_list =  arcade.SpriteList()
        self.enemy_physics_engine = None
        self.current_time = 0
        self.is_jumping = False # TODO REFACTOR
        #self.view_x = 0
        #self.view_y = 0


    def setup(self, level):
        """ Set up the game here. Call this function to restart the game. """
        self.sprite_lists_map = self.read_map("Maps/Level" + str(level) + ".tmx")
        self.player_sprite = arcade.Sprite("images/player_2/player_stand.png")
        self.player_sprite.center_x = 250
        self.player_sprite.center_y = 500
        self.player_sprite_list.append(self.player_sprite)
        self.player_physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.sprite_lists_map["Platforms"], gravity_constant=GRAVITY)
        self.enemy_sprite = arcade.Sprite("images/player_1/player_stand.png")
        self.enemy_sprite.center_x = 400
        self.enemy_sprite.center_y = 750
        self.enemy_sprite_list.append(self.enemy_sprite)
        self.enemy_physics_engine = arcade.PhysicsEnginePlatformer(self.enemy_sprite,
                                                                    self.sprite_lists_map["Platforms"],
                                                                    gravity_constant=GRAVITY)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        for layer_name in self.sprite_lists_map:
            self.sprite_lists_map[layer_name].draw()

        self.player_sprite_list.draw()
        self.enemy_sprite_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.SPACE:
            self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.LCTRL:
            self.player_sprite.change_y = PLAYER_JUMP_SPEED * -1
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED * -1
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP or key == arcade.key.SPACE:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.LCTRL:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def update(self, delta_time):
        """ Movement and game logic """
        self.current_time = self.current_time + delta_time
        if math.floor(self.current_time) % 2 == 0 and self.is_jumping == False:
            self.is_jumping = True
            self.enemy_sprite.change_y = PLAYER_JUMP_SPEED
        self.is_jumping = False

        self.player_physics_engine.update()
        self.enemy_physics_engine.update()
        """        if self.player_sprite.collides_with_list(self.sprite_lists_map["Platforms"]):
            self.is_on_a_platform = True
            print("I am inside of the if statement")
        else:
            self.is_on_a_platform = False"""


    def read_map(self, map_location:str):
        tiled_map = arcade.read_tmx(map_location)
        r_map = {}
        for layer in tiled_map.layers:
            sprite_list = arcade.tilemap.process_layer(tiled_map, layer.name, scaling=.5)
            r_map[layer.name] = sprite_list
        return r_map

def main():
    """ Main method """
    window = Game()
    window.setup(window.level)
    arcade.run()

if __name__ == "__main__":
    main()