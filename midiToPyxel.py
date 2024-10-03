from mido import MidiFile, tick2second
from collections import defaultdict
from math import floor

def note_num_to_str(noteNum,octave_shift = 0):
    note_strs = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    octave = floor((noteNum / 12) - 1) + octave_shift
    noteIndex = (noteNum % 12)
    note = note_strs[noteIndex] + str(octave)
    return note


mid = MidiFile('Untitled.mid')

pyxel_ticks_per_beat = 4
print(mid.ticks_per_beat)

note_on_ticks = defaultdict()
start_tick = 0#10*4*mid.ticks_per_beat

for i,track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i,track.name))
    if i == 0:
        dt = -start_tick
        tempo = 500000
        for msg in track:
            if msg.type == 'set_tempo':
                tempo = msg.tempo
            if not msg.is_meta:
                dt += msg.time
                if msg.type == 'note_on':
                    print(msg,dt,tick2second(dt,mid.ticks_per_beat,tempo))
                    beat = (dt/mid.ticks_per_beat)
                    #print(dt,beat,beat % 4)
                    note_on_ticks[round(beat*4)] = msg.note
                

pyxel_max_ticks = 8*6
note_str = ""

for tick in range(pyxel_max_ticks):
    if tick in note_on_ticks.keys():
        note_str += note_num_to_str(note_on_ticks[tick],-1)
    else:
        note_str += "R"

print(note_str)





