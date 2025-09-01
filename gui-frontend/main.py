from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QProgressBar


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.setWindowTitle("Progress Tracker App")
        self.setMinimumSize(QSize(500, 500))

        main_page = QWidget()
        main_page_layout = QVBoxLayout()

        # Replace with request to backend server
        trackers = {
            "tracker1": ["1", "The Oxford History of Britain", 582, 751],
            "tracker2": ["2", "Churchill: Walking with Destiny", 0, 982]
        }


        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(200, 80, 250, 20)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border-radius: 10px;
                background-color: #6197cf;
                text-align: center;
                height: 5px;
                color: #FFFFFF;
                font-size: 16px;
                font-weight: bold;
            }

            QProgressBar::chunk {
                background-color: #0c6bab;
                border-radius: 10px
            }
                                        """)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(trackers["tracker1"][3])
        self.progress_bar.setValue(trackers["tracker1"][2])
        main_page_layout.addWidget(self.progress_bar)
        main_page.setLayout(main_page_layout)
        self.setCentralWidget(main_page)

app = QApplication([])
main = Main()
main.show()
app.exec()
