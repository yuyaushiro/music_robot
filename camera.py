import cv2
import numpy as np

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FPS, 30)
width = 1920
height = 1080
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)   # カメラ画像の横幅を1280に設定
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)  # カメラ画像の縦幅を720に設定
mtx = np.array([[1451.104955, 0.000000, 975.838026],
                [0.000000, 1449.488655, 554.863412],
                [0.000000, 0.000000, 1.000000]])
dist =  np.array([0.048423, -0.127427, 0.002862, 0.000782, 0.000000])

rad_thresh = 2

i = 0
while True:
    ret, frame = cap.read()
    if ret:
        h,  w = frame.shape[:2]
        newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
        frame = cv2.undistort(frame, mtx, dist, None, newcameramtx)
        #frame = cv2.undistort(frame, mtx, dist)
        frame = frame[20:-20,20:-20]
        print('---')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, ksize=(7, 7), sigmaX=1.0, sigmaY=1.0)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        lines = cv2.HoughLines(edges, 1, np.pi/180, 300)
        h_lines = []
        if lines is not None:
            for line in lines:
                rho, theta = line[0]
                if theta < np.deg2rad(90+rad_thresh) and\
                   theta > np.deg2rad(90-rad_thresh):
                    a = np.cos(theta)
                    b = np.sin(theta)
                    x0 = a * rho
                    y0 = b * rho
                    x1 = int(x0 + width*(-b))
                    y1 = int(y0 + width*(a))
                    x2 = int(x0 - width*(-b))
                    y2 = int(y0 - width*(a))
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    h_lines.append(rho)
            h_lines = np.sort(h_lines)
            if len(h_lines) > 2 and len(h_lines) % 2 == 0:
                staff_notation = np.array([np.mean([h_lines[i], h_lines[i+1]])
                                           for i in range(0, len(h_lines), 2)])
                top_sf, bottom_sf = np.array_split(staff_notation, 2)

                # 音階リスト
                top_scale = []
                for i in range(len(top_sf)-1):
                    top_scale.append(top_sf[i])
                    top_scale.append(np.mean([top_sf[i], top_sf[i+1]]))
                top_scale.append(top_sf[-1])

        frame = cv2.resize(frame, None, fx=0.7, fy=0.7)
        cv2.imshow('Raw Frame', frame)

    # キー入力を1ms待って、k が27（ESC）だったらBreakする
    k = cv2.waitKey(1)
    if k == 27:
        break
    if k == ord('s'):
        file_name = "image" + str(i).zfill(2)
        cv2.imwrite(file_name + '.png', frame)
        # file = open(file_name + '.txt', 'w')
        # file.write('hogehoge')
        # file.close()
        i += 1

# キャプチャをリリースして、ウィンドウをすべて閉じる
cap.release()
cv2.destroyAllWindows()
