



import pyxel


pyxel.init(160, 120)
pyxel.sounds[0].speed = 30
pyxel.sounds[0].set_notes("C3D3E3F3G3RRRG3RRRG3RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")

play_frame = 0

fps = 30

def update():
    global play_frame
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

    if pyxel.btnp(pyxel.KEY_SPACE):
        pyxel.play(0,0)
        play_frame = pyxel.frame_count

    play_time = (pyxel.frame_count - play_frame) / fps
    play_time *= 30
    print(pyxel.play_pos(0),play_time)

    

def draw():
    pyxel.cls(0)
    pyxel.rect(10, 10, 20, 20, 11)

pyxel.run(update, draw)