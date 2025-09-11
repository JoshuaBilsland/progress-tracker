import os
import requests
from dotenv import load_dotenv
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QProgressBar, QSizePolicy, QSpacerItem, QPushButton


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.setWindowTitle("Progress Tracker App")
        self.setMinimumSize(QSize(500, 500))

        self.main_page = QWidget()
        self.main_page_layout = QVBoxLayout()
        self.main_page_layout.setContentsMargins(0, 0, 0, 0)
        self.main_page_layout.setSpacing(0)

        # Heading Label
        self.heading_label = QLabel("Progress Tracker App")
        self.heading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.heading_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.main_page_layout.addWidget(self.heading_label)

        # Store progress bars by tracker_name/key for individual retrieval
        self.trackers_container = QWidget()
        self.create_trackers_layout()

        self.trackers_container.setLayout(self.trackers_layout)
        self.main_page_layout.addWidget(self.trackers_container)

        self.main_page.setLayout(self.main_page_layout)
        self.setCentralWidget(self.main_page)

    def refresh_trackers(self):
        container_index = self.delete_trackers_structure()
        self.create_trackers_layout()
        self.trackers_container.deleteLater()
        self.trackers_container = QWidget()
        self.trackers_container.setLayout(self.trackers_layout)
        self.main_page_layout.insertWidget(container_index, self.trackers_container)
        self.centralWidget().update()

    def create_trackers_layout(self):
        trackers = self.get_trackers()
        self.trackers_layout = QVBoxLayout()
        self.trackers_layout.setContentsMargins(40, 40, 40, 40)
        self.trackers_layout.setSpacing(20)

        self.progress_bars = {}
        for tracker_name, tracker_data in trackers.items():
            tracker_container = QWidget()
            tracker_layout = QVBoxLayout()
            tracker_layout.setContentsMargins(0, 0, 0, 0)
            tracker_layout.setSpacing(15)

            # Tracker Label
            tracker_label = QLabel(f"{tracker_data[1]} - {tracker_data[2]}/{tracker_data[3]}")
            tracker_label.setObjectName("tracker-label")
            tracker_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            tracker_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            tracker_layout.addWidget(tracker_label)

            # Tracker Bar
            progress_bar = QProgressBar(self)
            progress_bar.setMinimum(0)
            progress_bar.setMaximum(tracker_data[3])
            progress_bar.setValue(tracker_data[2])
            progress_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            tracker_layout.addWidget(progress_bar)

            # Tracker Delete Button
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda checked, tn=tracker_name: self.delete_tracker(tn))
            delete_button.clicked.connect(lambda checked: self.refresh_trackers())
            tracker_layout.addWidget(delete_button)

            tracker_container.setLayout(tracker_layout)
            self.trackers_layout.addWidget(tracker_container)
            self.trackers_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
            self.progress_bars[tracker_name] = progress_bar

    def get_trackers(self):
        backend_ip = os.getenv("BACKEND_IP")
        url = f"http://{backend_ip}:8000/trackers"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def delete_trackers_structure(self):
        # Delete existing trackers layout and widgets
        while self.trackers_layout.count():  # Keeps going until no more widgets in layout
            child = self.trackers_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Find the index of the previous container within the main page layout
        for i in range(self.main_page_layout.count()):
            item = self.main_page_layout.itemAt(i)
            widget = item.widget()
            if widget == self.trackers_container:
                index = i
        return index

    def delete_tracker(self, trackername):
        backend_ip = os.getenv("BACKEND_IP")
        url = f"http://{backend_ip}:8000/delete"
        response = requests.delete(url, params={"trackername": trackername})
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
