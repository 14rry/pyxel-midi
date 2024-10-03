"""
Rhythm game helper for pyxel

Check if user input matches rhythm of song

Create music where one of the channels should 
be matched by the user input.

In game code, load pyxres file with music defined

Initialize PyxelBeats and provide the music number and 
channel that should be matched. Optionally define the
grace_frames, or how early/late the input can be.

TODO: support note hold/release

"""

import pyxel

class PyxelBeats:

    def __init__(self,music_num,ch,grace_frames = 4):
        self.current_note = None
        self.note_change_frame = 0
        self.press_frame = 0
        self.frames_per_note = 30
        self.padding = grace_frames
        self.need_check_early = False
        self.success_note = True
        self.missed_note = False
        self.num_misses = 0
        self.mplaying = False
        self.music_num = music_num

        self.ch = ch # the channel with beats that have to be tested
        self.set_music(music_num)

    def set_music(self,music_num):
        self.snd_idx = -1

        snds = pyxel.musics[music_num].seqs.to_list()
        self.snds = snds[self.ch]

    def toggle_music(self):
            if self.mplaying:
                pyxel.stop()
                self.current_note = None
                self.mplaying = False
            else:
                pyxel.playm(self.music_num,loop=True)
                self.mplaying = True
                self.call = False
                self.snd_idx = -1      

    def judge_timing(self):    
        self.press_frame = pyxel.frame_count
        dist = abs(self.note_change_frame - pyxel.frame_count)
        if dist < self.padding: #(dist > self.frames_per_note - self.padding and dist < self.frames_per_note + self.padding):
            print('good')
            self.success_note = True
        else:
            # maybe slightly early press, see if note comes on soon
            self.need_check_early = True

    def check_miss_early(self):
        # no note happened after player pressed button early.. too early!!
        if self.need_check_early:
            if abs(self.press_frame - pyxel.frame_count) >= self.padding:
                self.need_check_early = False
                print('bad early')

    def check_miss(self):
        if not self.missed_note:
            if not self.success_note:
                if abs(pyxel.frame_count - self.note_change_frame) >= self.padding:
                    self.num_misses += 1
                    print('missed note',self.num_misses,self.current_note)
                    self.missed_note = True

    # returns true if start of measure
    def update_note_frames(self):
        start_of_sound = False
        if not self.mplaying:
            return start_of_sound

        cn = pyxel.play_pos(0) # get current position in sound (channel doesn't matter - all have same num of notes)
        if cn[1] != self.current_note: # next beat in measure
            self.current_note = cn[1]

            # start of measure
            if cn[1] == 0:
                start_of_sound = True
                self.snd_idx += 1
                if self.snd_idx > len(self.snds)-1:
                    self.snd_idx = 0

            note_num = pyxel.sounds[self.snds[self.snd_idx]].notes[cn[1]] # note pitch value
            if note_num != -1: # not a rest
                self.missed_note = False
                self.success_note = False
                self.note_change_frame = pyxel.frame_count

                if self.need_check_early: # when button is pressed slightly before note on, still give credit
                    self.need_check_early = False
                    if abs(self.press_frame - pyxel.frame_count) < self.padding:
                        self.success_note = True
                        print('good early')

        return start_of_sound


    def update(self):
        self.check_miss_early()
        sound_started = self.update_note_frames()
        self.check_miss()
        return sound_started