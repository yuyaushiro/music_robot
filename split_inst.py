import numpy as np
import pretty_midi
import sys
import os


if __name__ == "__main__":
    if len(sys.argv) > 1:
        midi_file = sys.argv[1]
    else:
        midi_file = ""
    midi_data = pretty_midi.PrettyMIDI(midi_file)

    instruments = np.array(midi_data.instruments)
    print(instruments)
    os.makedirs(midi_file[0:-4])
    for i, instrument in enumerate(instruments):
        data = pretty_midi.PrettyMIDI()
        data.instruments.append(instrument)
        #data.write(midi_file[0:-5] + "/" + instrument.name + '_' + str(i) + '.mid')
        data.write(midi_file[0:-5] + "/" + str(i) + '.mid')
