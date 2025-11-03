import cv2
import numpy as np
import time
from collections import deque
import os

HSV_PRESETS = {
    "Red":    ([0,120,70], [10,255,255], [170,120,70], [179,255,255]), 
    "Green":  ([36,50,70], [89,255,255]),
    "Blue":   ([90,60,50], [128,255,255]),
    "Yellow": ([20,100,100], [35,255,255]),
    "Orange": ([5,100,100], [20,255,255]),
    "Violet": ([130,50,70], [160,255,255])
}

DRAW_COLORS = {
    "Red": (0,0,255), "Green": (0,255,0), "Blue": (255,0,0),
    "Yellow": (0,255,255), "Orange": (0,165,255), "Violet": (238,130,238)
}

SHAPE_NAMES = ["Triangle", "Square", "Rectangle", "Circle"]

COLOR_KEYS = {'1':"Red",'2':"Green",'3':"Blue",'4':"Yellow",'5':"Orange",'6':"Violet"}
SHAPE_KEYS = {'q':"Triangle",'w':"Square",'e':"Rectangle",'r':"Circle"}


def get_next_filename(prefix="session", ext=".avi"):
    i = 1
    while True:
        name = f"{prefix}_{i}{ext}"
        if not os.path.exists(name):
            return name
        i += 1

def get_contour_center(contour):
    M = cv2.moments(contour)
    if M["m00"] == 0:
        return None
    return (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))

def detect_shape(contour):
    area = cv2.contourArea(contour)
    if area < 800:
        return None

    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
    sides = len(approx)

    if sides == 3:
        return "Triangle"
    elif sides == 4:
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = w / float(h)
        if 0.95 <= aspect_ratio <= 1.05:
            return "Square"
        else:
            return "Rectangle"
    elif sides > 6:
        if perimeter == 0:
            return None
        circularity = 4 * np.pi * area / (perimeter * perimeter)
        if circularity > 0.7:
            return "Circle"
    return None

#video capture

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Could not access the camera.")
    exit()


tracked_combos = []    
trails = []            
previous_centers = []  
trail_overlay = None
recording_writer = None
recording_filename = None

# initial parameters
selected_color = None
selected_shape = None
min_area = 800
trail_length = 10

#controls
print("||| CONTROLS |||")
print("Colors: 1-Red 2-Green 3-Blue 4-Yellow 5-Orange 6-Violet")
print("Shapes: q-Triangle w-Square e-Rectangle r-Circle")
print("a = Add combo | z = Remove last combo | x = Reset")
print("+/- = Adjust minimum area | ESC/q = Quit")

#main program

last_time = time.time()
fps_smooth = 0.0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)

    height, width = frame.shape[:2]   
    if trail_overlay is None:
        trail_overlay = np.zeros_like(frame)
    else:
        trail_overlay = (trail_overlay * 0.9).astype(np.uint8)

    # key actions
    key = cv2.waitKey(1) & 0xFF
    if key != 255:
        key_char = chr(key) if key < 256 else ''

        if key_char in COLOR_KEYS:
            selected_color = COLOR_KEYS[key_char]
            print("Selected color:", selected_color)
        elif key_char in SHAPE_KEYS:
            selected_shape = SHAPE_KEYS[key_char]
            print("Selected shape:", selected_shape)

        elif key_char == 'a': 
            if not selected_color or not selected_shape:
                print("Pick color and shape first!")
            else:
                preset = HSV_PRESETS[selected_color]
                hsv_ranges = [(np.array(preset[0]), np.array(preset[1]))] \
                    if selected_color != "Red" else \
                    [(np.array(preset[0]), np.array(preset[1])), (np.array(preset[2]), np.array(preset[3]))]

                tracked_combos.append({"color": selected_color, "shape": selected_shape, "hsv_ranges": hsv_ranges})
                trails.append([deque(maxlen=trail_length), deque(maxlen=trail_length)])
                previous_centers.append([None, None])
                print(f"Added {selected_color} {selected_shape}")

                if recording_writer is None:
                    recording_filename = get_next_filename()
                    fourcc = cv2.VideoWriter_fourcc(*"XVID")#type:ignore
                    recording_writer = cv2.VideoWriter(recording_filename, fourcc, 20.0, (width, height))
                    print("Recording started:", recording_filename)

        elif key_char == 'z':  
            if tracked_combos:
                tracked_combos.pop()
                trails.pop()
                previous_centers.pop()
                print("Removed last combo")

        elif key_char == 'x':  
            tracked_combos.clear()
            trails.clear()
            previous_centers.clear()
            trail_overlay = np.zeros_like(frame)
            if recording_writer:
                recording_writer.release()
                recording_writer = None
            print("Reset complete")

        elif key_char == '+':
            min_area += 100
            print("Minimum area:", min_area)
        elif key_char == '-':
            min_area = max(100, min_area - 100)
            print("Minimum area:", min_area)
        elif key == 27 or key_char == 'q':  
            break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    display = frame.copy()

    #all combos detection
    for idx, combo in enumerate(tracked_combos):
        mask = None
        for (low, high) in combo["hsv_ranges"]:
            current_mask = cv2.inRange(hsv, np.array(low), np.array(high))
            mask = current_mask if mask is None else cv2.bitwise_or(mask, current_mask)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
        mask = cv2.medianBlur(mask, 5)#type:ignore
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        valid_shapes = [(cnt, cv2.contourArea(cnt)) for cnt in contours if cv2.contourArea(cnt) >= min_area and detect_shape(cnt) == combo["shape"]]
        valid_shapes.sort(key=lambda x: x[1], reverse=True)

        top_contours = [v[0] for v in valid_shapes[:2]]
        centers = [get_contour_center(c) for c in top_contours]
        prev = previous_centers[idx]
        current_positions = [None, None]

        if len(top_contours) == 0:
            for t in trails[idx]:
                t.clear()
            continue

        for cent in centers:
            if cent is None:
                continue
            distances = [np.hypot(cent[0]-p[0], cent[1]-p[1]) if p is not None else 1e6 for p in prev]
            best = int(np.argmin(distances))
            if distances[best] < 80 and current_positions[best] is None:
                current_positions[best] = cent#type:ignore
                prev[best] = cent
            else:
                if None in prev:
                    empty_slot = prev.index(None)
                    current_positions[empty_slot] = cent#type:ignore
                    prev[empty_slot] = cent
                else:
                    farthest = int(np.argmax(distances))
                    current_positions[farthest] = cent#type:ignore
                    prev[farthest] = cent

        # update trail points
        for i in range(2):
            if current_positions[i] is not None:
                trails[idx][i].appendleft(current_positions[i])

        draw_color = DRAW_COLORS.get(combo["color"], (255,255,255))
        for i, contour in enumerate(top_contours):
            cv2.drawContours(display, [contour], -1, (0,0,0), 9)
            cent = get_contour_center(contour)
            if cent:
                cv2.putText(display, f"{combo['color']} {combo['shape']} {i+1}", (cent[0]+10, cent[1]),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)

        #fading effect
        for trail_pair in trails:
            for trail in trail_pair:
                for j in range(1, len(trail)):
                    if trail[j-1] is None or trail[j] is None:
                        continue
                    fade = int(255 * ((len(trail) - j) / len(trail)))
                    cv2.line(trail_overlay, trail[j-1], trail[j], (fade, fade, fade), 8, cv2.LINE_AA)

    final_output = cv2.addWeighted(display, 1, trail_overlay, 0.7, 0)

    # Text overlays
    cv2.putText(final_output, f"Combos: {len(tracked_combos)} (press a to add)", (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.putText(final_output, f"Min Area: {min_area}", (10,80), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 1)
    cv2.putText(final_output, f"Selected: {selected_color or '-'} {selected_shape or '-'}", (10,120), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 1)

    # FPS
    now = time.time()
    dt = now - last_time if now != last_time else 1.0
    last_time = now
    fps = 1.0 / dt
    fps_smooth = fps_smooth * 0.9 + fps * 0.1
    cv2.putText(final_output, f"FPS: {fps_smooth:.1f}", (width-120, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    # Show frames
    cv2.imshow("Object Tracker", final_output)
    if 'mask' in locals():
        cv2.imshow("Mask", mask)#type:ignore

    if recording_writer:
        recording_writer.write(final_output)

if recording_writer:
    recording_writer.release()
cap.release()
# cv2.destroyAllWindows()