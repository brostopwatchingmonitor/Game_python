import arcade
from views.game_view import GameView

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.title_text = None
        self.subtitle_text = None
        self.start_text = None
        self.controls_text = None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
        
        # Inisialisasi objek teks sekali saja agar performa cepat
        self.title_text = arcade.Text("DUNGEON SWORDMAN", self.window.width / 2, self.window.height / 2 + 50,
                                      arcade.color.CRIMSON, font_size=40, anchor_x="center", bold=True)
        self.subtitle_text = arcade.Text("Misi: Kalahkan Queen Tesa", self.window.width / 2, self.window.height / 2 - 10,
                                         arcade.color.WHITE, font_size=18, anchor_x="center")
        self.start_text = arcade.Text("Tekan ENTER untuk Memulai Petualangan", self.window.width / 2, self.window.height / 2 - 80,
                                      arcade.color.GOLDENROD, font_size=14, anchor_x="center")
        self.controls_text = arcade.Text("Kontrol: W/A/S/D (Gerak) | J (Interaksi) | Shift (Dash)", 
                                         self.window.width / 2, 40,
                                         arcade.color.LIGHT_GRAY, font_size=12, anchor_x="center")

    def on_draw(self):
        self.clear()
        self.title_text.draw()
        self.subtitle_text.draw()
        self.start_text.draw()
        self.controls_text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)
