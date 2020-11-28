class Settings:
    """
    A class to represent the game settings
    ...
    Methods
    -------
    increase_speed() - used to increase difficulty but also points awarded when
        hitting a kitty when leveling up
    """

    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 700
        self.button_width = 200
        self.button_height = 50
        self.button_top_margin = 600
        self.button_left_margin = 400
        self.logo_top_margin = 100
        self.small_margin = 10
        self.medium_margin = 20

        self.buffer_zone = 400
        self.kitty_buffer_factor = 2

        self.font_size = 48
        self.score_font_size = 36

        self.play_button_text = "Play"
        self.caption = "Felicide"

        self.bg_color = (254, 127, 156)
        self.button_color = (108, 70, 117)
        self.text_color = (255, 193, 37)
        self.score_text_color = (46, 139, 87)

        self.bork_image = 'images/bork.png'
        self.corgi_image = 'images/corgibutt.png'
        self.kitty_image = 'images/kitty.png'
        self.logo_image = 'images/logo1.png'

        self.sound_volume = 0.2
        self.bork_sound = 'sounds/bork.wav'

        self.corgi_limit = 3

        self.army_drop_speed = 10
        self.time_interval = 0.25
        self.break_time = 2500

        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.corgi_speed = 1.5
        self.bork_speed = 8
        self.kitty_speed_factor = 0.75
        self.army_direction = 1  # 1 represents right, -1 left
        self.kitty_points = 100

    def increase_speed(self):
        self.corgi_speed *= self.speedup_scale
        self.bork_speed *= self.speedup_scale
        self.kitty_speed_factor *= self.speedup_scale
        self.kitty_points = int(self.kitty_points * self.score_scale)
