import socket
import xml.etree.ElementTree as ET
import os
import subprocess
import time
import sys
import serial
import numpy as np
import pretty_midi


host = '127.0.0.1' #localhost
port = 10500   #julisuサーバーモードのポート

def check_word(word):
    if word == "ファンファーレ":
        midi_to_serial("../midi/KantohG/0.mid", 1000, -1)
        killword = ("ファンファーレ")
    elif word == "マリオ":
        midi_to_serial("../midi/mario/_0.mid", 1000, 0)
        killword = ("マリオ")
    elif word == "カービィ":
        midi_to_serial("../midi/harukaz/_2.mid", 1300, -2)
        killword = ("カービィ")
    elif word == "エムステ":
        midi_to_serial("../midi/shiba_mu/1090.mid", 1000, 0)
        killword = ("エムステ")
    elif word == "ドラゴンクエスト":
        midi_to_serial("../midi/shiba_mu/dragonquest.mid", 1000, -2)
        killword = ("ドラゴンクエスト")
    elif word == "ゲットワイルド":
        midi_to_serial("../midi/shiba_mu/getwild.mid", 1000, 0)
        killword = ("ゲットワイルド")
    elif word == "ホットリミット":
        midi_to_serial("../midi/shiba_mu/hotlimit.mid", 1000, -1)
        killword = ("ホットリミット")
    elif word == "恋":
        midi_to_serial("../midi/shiba_mu/koi.mid", 1000, -1)
        killword = ("恋")
    elif word == "紅":
        midi_to_serial("../midi/shiba_mu/kurenai.mid", 1000, -1)
        killword = ("紅")
    elif word == "ポルカ":
        midi_to_serial("../midi/shiba_mu/livinpolka.mid", 1000, -1)
        killword = ("ポルカ")
    elif word == "め組":
        midi_to_serial("../midi/shiba_mu/megumi.mid", 1000, -1)
        killword = ("め組")
    elif word == "夏祭り":
        midi_to_serial("../midi/shiba_mu/natumaturi.mid", 1000, 0)
        killword = ("夏祭り")
    elif word == "ニコニコ動画":
        midi_to_serial("../midi/shiba_mu/nikoniko.mid", 1000, -1)
        killword = ("ニコニコ動画")
    elif word == "サザエさん":
        midi_to_serial("../midi/shiba_mu/sazae.mid", 1000, -1)
        killword = ("サザエさん")
    elif word == "てってってー":
        midi_to_serial("../midi/shiba_mu/tettete.mid", 1000, 0)
        killword = ("てってってー")
    elif word == "USA":
        midi_to_serial("../midi/shiba_mu/USA.mid", 1000, 0)
        killword = ("USA")
    elif word == "打ち上げ花火":
        midi_to_serial("../midi/shiba_mu/utiage.mid", 1000, -1)
        killword = ("打ち上げ花火")
    elif word == "君が代":
        midi_to_serial("../midi/shiba_mu/kokka.mid", 1000, 0)
        killword = ("君が代")
    elif word == "ダースベイダー":
        midi_to_serial("../midi/shiba_mu/bayder.mid", 1000, -1)
        killword = ("ダースベイダー")
    elif word == "テーゼ":
        midi_to_serial("../midi/shiba_mu/eva.mid", 1000, 0)
        killword = ("テーゼ")
    elif word == "キューピー":
        midi_to_serial("../midi/shiba_mu/qp.mid", 1000, -1)
        killword = ("キューピー")
    elif word == "千本桜":
        midi_to_serial("../midi/shiba_mu/thousand.mid", 1000, 0)
        killword = ("千本桜")
    elif word == "ジングルベル":
        midi_to_serial("../midi/shiba_mu/bell.mid", 1000, 0)
        killword = ("ジングルベル")
    elif word == "全然前世":
        midi_to_serial("../midi/shiba_mu/zense.mid", 1000, 0)
        killword = ("全然前世")
    elif word == "背景":
        midi_to_serial("../midi/shiba_mu/haikei.mid", 1000, 0)
        killword = ("背景")
    else:
        print("else")
        killword = ('name')

    print (killword) # wordを表示

def midi_to_serial(midi_file, vel, shift):
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
    data += "dd,100\r\n\r\n"

    with serial.Serial('/dev/ttyUSB0', 115200) as ser:
        ser.write(data.encode("utf-8"))
        #string = ""
        #while (string != "100,4444,0\r\n"):
        #    print(string)
        #    c = ser.read()
        #    string = ser.readline()
        #    string = string.decode("utf-8")
        #print(string != "100,4444,0")
        ser.close()

def main():

    p = subprocess.Popen(["./julius-start.sh"], stdout=subprocess.PIPE, shell=True) # julius起動スクリプトを実行
    pid = str(p.stdout.read().decode('utf-8')) # juliusのプロセスIDを取得
    time.sleep(3) # 3秒間スリープ
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port)) #サーバーモードで起動したjuliusに接続

    try:
        data = '' # dataの初期化
        killword ='' # 前回認識した言葉を記憶するための変数
        while 1:
            #print(data) # 認識した言葉を表示して確認
            if '</RECOGOUT>\n.' in data: 

                root = ET.fromstring('<?xml version="1.0"?>\n' + data[data.find('<RECOGOUT>'):].replace('\n.', ''))
                for whypo in root.findall('./SHYPO/WHYPO'):
                    word = whypo.get('WORD')# juliusで認識したWORDをwordに入れる
                    check_word(word)
                    data = '' # dataの初期化

            else:
                data += str(client.recv(1024).decode('utf-8')) #dataが空のときjuliusからdataに入れる
                print('NotFound')# juliusに認識する言葉がない。認識していない。


    except KeyboardInterrupt:
        p.kill()
        subprocess.call(["kill " + pid], shell=True)# juliusのプロセスを終了する。
        client.close()

if __name__ == "__main__":
    main()
