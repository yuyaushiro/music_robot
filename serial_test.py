# -*- coding: utf-8 -*-

import sys
import serial
import numpy as np
import time
import pretty_midi


if __name__ == "__main__":
    if len(sys.argv) > 3:
        midi_file = sys.argv[1]
        vel = int(sys.argv[2])
        shift = int(sys.argv[3])
        print(shift)
    else:
        midi_file = ""
        vel = 1000
        shift = 0
    midi_data = pretty_midi.PrettyMIDI(midi_file)

    notes = np.array([[note.start, note.end,
                       pretty_midi.note_number_to_name(note.pitch)]
                      for note in midi_data.instruments[0].notes])

    data = "ss,400\n"
    t1 = float(notes[0, 0])
    for i, note in enumerate(notes):
        if i+1 < len(notes):
            t2 = float(notes[i+1, 0])
        else:
            t2 = t1 + 3
        dt = t2 - t1
        aaa = note[2].replace('#', '')
        aaa = aaa[0] + str(int(aaa[1]) + shift)
        data += aaa + "," + str(int(dt*vel)) + "\n" + "UP,0\n"
        print(aaa, dt)

        t1 = t2
        #time.sleep((t2-t1))
    data += "dd,500\r\n\r\n"

    #print(data)
    with serial.Serial('/dev/ttyUSB0', 115200) as ser:
        #ser.write(bytes(data, 'utf-8'))
        ser.write(data.encode("utf-8"))

        while True:
            c = ser.read()
            string = ser.readline()
            print(string.decode("utf-8"))
            #print(str(string))
        ser.close()

        