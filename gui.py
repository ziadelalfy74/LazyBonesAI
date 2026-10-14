import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from controller import GestureController

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('LazyBones AI - Gesture Controller')
        self.setGeometry(50, 50, 1100, 650)
        self.setStyleSheet("background-color: #161b22; color: #c9d1d9; font-family: 'Segoe UI', Arial;")

        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, 'ICON.ico')
        else:
            icon_path = os.path.join(os.path.dirname(__file__), 'ICON.ico')

        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        
        left_widget = QWidget()
        left_widget.setStyleSheet("background-color: #0d1117; border: 1px solid #30363d; border-radius: 10px;")
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(15, 15, 15, 15)

        title_doc = QLabel("LAZYBONES - GESTURE MAP")
        title_doc.setStyleSheet("font-size: 16px; font-weight: bold; color: #58a6ff; margin-bottom: 10px;")
        left_layout.addWidget(title_doc)

        instructions_text = """
        <b>[ ↗ ] VOLUME UP (Thumb Up):</b><br>
        Extend Thumb upwards to increase system media volume.<br><br>
        
        <b>[ ↘ ] VOLUME DOWN (Thumb Down):</b><br>
        Point Thumb downwards to decrease system media volume.<br><br>
        
        <b>[ ◼ ] PLAY / PAUSE (Closed Fist):</b><br>
        Make a full closed fist to toggle media playback.<br><br>
        
        <b>[ ⏩ ] FORWARD 10s (Victory Up):</b><br>
        Show Victory sign pointing UP to skip forward 10 seconds.<br><br>
        
        <b>[ ⏪ ] REWIND 10s (OK Gesture):</b><br>
        Make an OK sign (Thumb & Index closed, others up) to rewind 10 seconds.
        """
        
        doc_label = QLabel(instructions_text)
        doc_label.setWordWrap(True)
        doc_label.setStyleSheet("font-size: 13px; color: #8b949e; line-height: 1.4;")
        left_layout.addWidget(doc_label)
        left_layout.addStretch()

        main_layout.addWidget(left_widget, 1)

        
        right_widget = QWidget()
        right_widget.setStyleSheet("background-color: #0d1117; border: 1px solid #30363d; border-radius: 10px;")
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(15, 15, 15, 15)

        self.video_label = QLabel('CAMERA OFFLINE\nClick START to initialize')
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("border: 2px dashed #30363d; background-color: #010409; color: #484f58; border-radius: 8px; font-weight: bold;")
        self.video_label.setFixedSize(640, 360)
        right_layout.addWidget(self.video_label, alignment=Qt.AlignCenter)

        btn_layout = QHBoxLayout()
        
        self.start_btn = QPushButton('START ENGINE')
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #238636; color: white; font-weight: bold; padding: 12px; border-radius: 6px; font-size: 14px;
            }
            QPushButton:hover { background-color: #2ea043; }
            QPushButton:pressed { background-color: #196c2e; padding-top: 14px; }
        """)
        self.start_btn.clicked.connect(self.start_camera)
        
        self.stop_btn = QPushButton('STOP ENGINE')
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #da3633; color: white; font-weight: bold; padding: 12px; border-radius: 6px; font-size: 14px;
            }
            QPushButton:hover { background-color: #f85149; }
            QPushButton:pressed { background-color: #b62324; padding-top: 14px; }
        """)
        self.stop_btn.clicked.connect(self.stop_camera)

        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        right_layout.addLayout(btn_layout)

        main_layout.addWidget(right_widget, 1)

        self.setLayout(main_layout)

    def start_camera(self, _=None, explicit_start=True):
        if self.controller is None or not self.controller.isRunning():
            self.controller = GestureController()
            self.controller.frame_signal.connect(self.update_gui_feed)
            self.controller.start()

    def stop_camera(self):
        if self.controller and self.controller.isRunning():
            self.controller.stop()
            self.controller = None
        self.video_label.clear()
        self.video_label.setText('CAMERA OFFLINE\nClick START to initialize')

    def update_gui_feed(self, qt_image, action_text, color_tuple):
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        self.stop_camera()
        event.accept()

import traceback
import sys

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        with open("crash_log.txt", "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
        raise e