import time
import numpy as np
import pretty_midi
import sys


if __name__ == "__main__":
    if len(sys.argv) > 1:
        midi_file = sys.argv[1]
    else:
        midi_file = ""
    #midi_data = pretty_midi.PrettyMIDI("midi/dq_inst/inst_Horn 1.mid")
    #midi_data = pretty_midi.PrettyMIDI("midi/arupusu_inst/inst_ Accordion Fr *merged.mid")
    #midi_data = pretty_midi.PrettyMIDI("midi/aogeba_inst/inst_sc88  2_2.mid")
    midi_data = pretty_midi.PrettyMIDI(midi_file)

    notes = np.array([[note.start, note.end,
                       pretty_midi.note_number_to_name(note.pitch)]
                      for note in midi_data.instruments[0].notes])
    print(notes)
    print('start')
    t1 = float(notes[0, 0])
    for i, note in enumerate(notes):
        if i+1 < len(notes):
            t2 = float(notes[i+1, 0])
        else:
            t2 = t1 + 3
        print(note[2])
        print(t2-t1)
        time.sleep((t2-t1))
        t1 = t2
