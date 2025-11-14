import cv2
import numpy as np

cap = cv2.VideoCapture(0)

frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

lower_orange = np.array([5, 120, 120])
upper_orange = np.array([20, 255, 255])

thresh_angle = 8
thresh_x = 40
area_thresh = 3000

aligned = False
frame_aligned = 0
min_frames = 30

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    cmd = None

    if aligned:
        cmd = "Forward"
    else:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_orange, upper_orange)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            c = max(contours, key=cv2.contourArea)
            rect = cv2.minAreaRect(c)
            (x, y), (w, h), angle = rect

            if w * h > area_thresh:
                box = cv2.boxPoints(rect)
                box = np.intp(box)
                cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)#type: ignore

                center_point = (int(x), int(y))
                frame_center = (frame.shape[1] // 2, frame.shape[0] // 2)
                cv2.circle(frame, center_point, 6, (0, 0, 255), -1)
                cv2.line(frame,(frame_center[0], 0),(frame_center[0], frame.shape[0]),(255, 0, 0), 1)

                offset_x = center_point[0] - frame_center[0]

                if w > h:
                    angle += 90
                if angle > 90:
                    angle -= 180
                elif angle < -90:
                    angle += 180
                angle_error = -angle

                if abs(angle_error) > thresh_angle:
                    frame_aligned = 0
                    if angle_error > 0:
                        cmd = "Yaw left"
                    else:
                        cmd = "Yaw right"
                elif abs(offset_x) > thresh_x:
                    frame_aligned = 0
                    if offset_x < 0:
                        cmd = "Left"
                    else:
                        cmd = "Right"
                else:
                    frame_aligned += 1
                    if frame_aligned >= min_frames:
                        cmd = "Forward"
                        aligned = True

    if cmd:
        cv2.putText(frame, cmd, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Path Marker Final", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()