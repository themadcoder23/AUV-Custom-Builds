# 🍊 Path Marker: Orange Object Alignment System

This project implements a real-time object detection and alignment system using **OpenCV** and **Python**. It is designed to identify a dominant orange object in the camera feed, calculate its angle and position relative to the frame center, and generate navigational commands to move towards and align with the target.

This system is ideal for autonomous vehicles (like ROVs or drones) or robotics projects requiring visual tracking and alignment.

## ✨ Features

* **Real-Time Processing:** Processes video frames from a camera stream (`cv2.VideoCapture(0)`).
* **HSV Color Filtering:** Uses a defined **orange color range** to isolate the target object.
* **Morphological Operations:** Applies **opening and closing** to reduce noise and close gaps in the mask.
* **Contour Analysis:** Finds the largest contour and uses `cv2.minAreaRect` to calculate the object's **orientation (angle)** and **center point (offset)**.
* **Navigational Command Generation:** Generates the following commands based on calculated error thresholds:
    * `Yaw left`/`Yaw right`: To correct angular misalignment.
    * `Left`/`Right`: To correct horizontal position offset.
    * `Forward`: When both angular and positional errors are within acceptable thresholds for a sustained period.
* **Alignment Logic:** Uses a frame counter (`frame_aligned` and `min_frames`) to ensure **stable alignment** before issuing the final `Forward` command and entering the fully `aligned` state.

---

## ⚙️ Requirements

To run this code, you need Python and the following libraries:

| Library | Command to Install |
| :--- | :--- |
| **OpenCV** (cv2) | `pip install opencv-python` |
| **NumPy** (np) | `pip install numpy` |

---

## 🚀 Getting Started

### 1. Installation

Clone the repository and install the dependencies:

```bash
git clone [https://github.com/themadcoder23/AUV-Custom-Builds.git](https://github.com/themadcoder23/AUV-Custom-Builds.git)
cd AUV-Custom-Builds
pip install opencv-python numpy
