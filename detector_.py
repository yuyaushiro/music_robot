# -*- coding: utf-8 -*-
import cv2
import numpy as np
import dlib

width = 1920
height = 1080
rad_thresh = 2
scale = {13: "C3", 12: "D3", 11: "E3", 10: "F3", 9: "G3", 8: "A3", 7: "B3",
         6: "C4", 5: "D4", 4: "E4", 3: "F4", 2: "G4", 1: "A4", 0: "B4"}


def detect_staff_notation(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, ksize=(7, 7), sigmaX=1.0, sigmaY=1.0)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLines(edges, 1, np.pi/180, 300)
    h_lines = []
    staff_notation = np.array([0])
    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            if theta < np.deg2rad(90+rad_thresh) and\
               theta > np.deg2rad(90-rad_thresh):
                h_lines.append(rho)
        h_lines = np.sort(h_lines)
        if len(h_lines) > 2 and len(h_lines) % 2 == 0:
            staff_notation = np.array([np.mean([h_lines[i], h_lines[i+1]])
                                       for i in range(0, len(h_lines), 2)])
            for sf in staff_notation:
                cv2.line(img, (0, int(sf)), (width, int(sf)),
                         (0, 0, 255), 1)
    return staff_notation


def calc_scale_height(staff_notation, scale_height0=[]):
    if len(staff_notation) is not 5:
        return None

    scale_height = []
    for i in range(4):
        scale_height.append(staff_notation[i])
        scale_height.append(np.mean([staff_notation[i], staff_notation[i+1]]))
    scale_height.append(staff_notation[4])
    dist = scale_height[1]-scale_height[0]
    scale_height.insert(0, scale_height[0] - dist)
    scale_height.insert(0, scale_height[0] - dist)
    scale_height.insert(0, scale_height[0] - dist)
    dist = scale_height[-1]-scale_height[-2]
    scale_height.append(scale_height[-1] + dist)
    scale_height.append(scale_height[-1] + dist)
    scale_height = scale_height0 + scale_height

    return scale_height


def detect_notes(img, scale_height):
    notes_pos = [[] for i in range(int(len(scale_height)/14))]

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    dets = detector(rgb)
    for i, det in enumerate(dets):
        note_x = np.mean([det.left(), det.right()])
        note_y = np.mean([det.top(), det.bottom()])
        idx = np.abs(np.asarray(scale_height) - note_y).argmin()
        if (idx % 14) != 0:
            line_num = int(idx / 14)

            notes_pos[line_num].append([scale[idx % 14], note_x, note_y])
            # cv2.putText(img, str(i), (det.right(), det.bottom()),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0),
            #             thickness=2)
            cv2.putText(img, scale[idx % 14], (det.right(), det.bottom()),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0),
                        thickness=2)
            cv2.rectangle(img,
                          (det.left(), det.top()),
                          (det.right(), det.bottom()), (0, 0, 255), 2)

    notes_array = []
    for n in notes_pos:
        n.sort(key=lambda x: float(x[1]))
        notes_array.extend(n)
    return notes_array


if __name__ == "__main__":
    svm_file = "onpu/detector.svm"
    detector = dlib.simple_object_detector(svm_file)
    cap = cv2.VideoCapture(0)
    if cap.isOpened() is not True:
        raise("IO Error")
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    win_name = "Capture"
    cv2.namedWindow(win_name, cv2.WINDOW_AUTOSIZE)
    # win_det = dlib.image_window()
    # win_det.set_image(detector)

    while True:
        ret, img = cap.read()
        img = cv2.imread('チューリップ.png')
        img = cv2.resize(img, None, fx=0.6, fy=0.6)

        if ret:
            # 五線検出
            staff_notation = detect_staff_notation(img)
            scale_height = []
            for i in range(5, len(staff_notation)+1, 5):
                scale_height = calc_scale_height(staff_notation[i-5:i],
                                                 scale_height0=scale_height)
            if len(scale_height) is not 0:
                # 音符検出
                notes_array = detect_notes(img, scale_height)
                print(np.array(notes_array))

            cv2.imshow(win_name, img)

        key = cv2.waitKey(1)
        if key == ord('s'):
            file_name = "ScreenShot"
            cv2.imwrite(file_name + '.png', img)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
