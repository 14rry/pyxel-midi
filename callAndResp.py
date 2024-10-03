import pyxel
import pyxelBeats

class App:
    def __init__(self):
        pyxel.init(160, 120,fps=60)
        pyxel.load('my_resource.pyxres')
        self.x = 0
        self.call = False # response = False
        self.beats = pyxelBeats.PyxelBeats(1,2)

        #self.music_tick = 0
        # self.music_tick_inc = 4*120
        
        pyxel.run(self.update, self.draw)

    def toggle_call_response(self):
        if self.call:
            self.call = False
            #self.music_tick += self.music_tick_inc
        else:
            self.call = True   

    def update(self):

        if pyxel.btnp(pyxel.KEY_UP):
            #pyxel.play(3,10)
            self.beats.judge_timing()

        if pyxel.btnp(pyxel.KEY_P):
            self.beats.toggle_music()
            self.call = False

        start_of_sound = self.beats.update()

        if start_of_sound:
            self.toggle_call_response()

        # if not self.call:
        #     self.beats.check_miss()

        self.x = (self.x + 1) % pyxel.width

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.x, 0, 8, 8, 9)

App()