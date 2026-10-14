# 🛋️🤖 LazyBones AI

**LazyBones AI** is an open-source, AI-powered computer vision application that lets you control your laptop media playback (YouTube, media players, web browsers, system volume) using intuitive **hand gestures** via your webcam, without ever needing to touch your keyboard or mouse!

---

## 🚀 Gestures & Controls

* <b>[ ↗ ] VOLUME UP (Thumb Up):</b> Extend Thumb upwards to increase system media volume.
* <b>[ ↘ ] VOLUME DOWN (Thumb Down):</b> Point Thumb downwards to decrease system media volume.
* <b>[ ◼ ] PLAY / PAUSE (Closed Fist):</b> Make a full closed fist to toggle media playback.
* <b>[ ⏩ ] FORWARD 10s (Victory Up):</b> Show Victory sign (✌️) pointing UP to skip forward 10 seconds.
* <b>[ ⏪ ] REWIND 10s (OK Gesture):</b> Make an OK sign 👌 (Thumb & Index closed, others up) to rewind 10 seconds.

---

## 🛠️ Tech Stack
* **Python** (Core Logic)
* **MediaPipe** (Hand Tracking & Gesture Recognition)
* **OpenCV** (Video Stream Processing)
* **PyAutoGUI / Keyboard** (System Media Controls Injection)

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/ziadelalfy74/LazyBonesAI.git](https://github.com/ziadelalfy74/LazyBonesAI.git)
cd LazyBonesAI

2. Install Dependencies
pip install -r requirements.txt

3. Run the Application
python gui.py