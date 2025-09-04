import os
import requests
from dotenv import load_dotenv
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QProgressBar, QSizePolicy, QSpacerItem


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.setWindowTitle("Progress Tracker App")
        self.setMinimumSize(QSize(500, 500))

        main_page = QWidget()
        main_page_layout = QVBoxLayout()
        main_page_layout.setContentsMargins(0, 0, 0, 0)
        main_page_layout.setSpacing(0)

        # Retrieve Trackers From Server
        trackers = self.get_trackers()

        # Heading Label
        label = QLabel("Progress Tracker App")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        main_page_layout.addWidget(label)

        # Store progress bars by tracker_name/key for individual retrieval
        trackers_container = QWidget()
        trackers_layout = QVBoxLayout()
        trackers_layout.setContentsMargins(40, 40, 40, 40)
        trackers_layout.setSpacing(20)

        self.progress_bars = {}
        for tracker_name, tracker_data in trackers.items():
            tracker_container = QWidget()
            tracker_layout = QVBoxLayout()
            tracker_layout.setContentsMargins(0, 0, 0, 0)
            tracker_layout.setSpacing(15)

            tracker_label = QLabel(f"{tracker_data[1]} - {tracker_data[2]}/{tracker_data[3]}")
            tracker_label.setObjectName("tracker-label")
            tracker_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            tracker_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            tracker_layout.addWidget(tracker_label)

            progress_bar = QProgressBar(self)
            progress_bar.setMinimum(0)
            progress_bar.setMaximum(tracker_data[3])
            progress_bar.setValue(tracker_data[2])
            progress_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            tracker_layout.addWidget(progress_bar)

            tracker_container.setLayout(tracker_layout)
            trackers_layout.addWidget(tracker_container)
            trackers_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
            self.progress_bars[tracker_name] = progress_bar

        trackers_container.setLayout(trackers_layout)
        main_page_layout.addWidget(trackers_container)

        main_page.setLayout(main_page_layout)
        self.setCentralWidget(main_page)

    def get_trackers(self):
        backend_ip = os.getenv("BACKEND_IP")
        url = f"http://{backend_ip}:8000/trackers"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()


def load_stylesheet(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, filename)
    with open(path) as f:
        return f.read()


load_dotenv()  # Load environmental variables
app = QApplication([])
app.setStyleSheet(load_stylesheet("style.qss"))
main = Main()
main.show()
app.exec()
