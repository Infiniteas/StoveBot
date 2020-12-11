"""
stoveBot.py
Author: Bernard Chen
Main stoveBot GUI application. Utilizes stoveBotMQTT.py and stoveBotCV.py
"""

import sys
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from stoveBotMQTT import *

DIAL_SIZE = 350
DIAL_DIAG = (DIAL_SIZE**2 + DIAL_SIZE**2)**0.5
DIAL_IMG_PATH = "../dial.png"

class StoveBotWindow(QMainWindow):
	updateLeftDial = pyqtSignal(int)
	updateRightDial = pyqtSignal(int)

	currLeftAngle = 0
	currRightAngle = 0

	def __init__(self, *args, **kwargs):
		super(StoveBotWindow, self).__init__(*args, **kwargs)

		self.setWindowTitle("StoveBot")

		self.layout = QGridLayout()

		# Title
		titleLabel = QLabel("StoveBot Monitor")
		titleLabel.setFont(QFont('Helvetica', 30, QFont.Bold))

		# Dial descriptions
		self.leftStatus = QLabel("OFF")
		self.rightStatus = QLabel("OFF")
		self.leftStatus.setFont(QFont('Helvetica', 20))
		self.rightStatus.setFont(QFont('Helvetica', 20))

		# Dial off buttons
		self.leftButton = QPushButton()
		self.leftButton.setText("Turn Off")
		self.leftButton.clicked.connect(lambda : publishLeftAngle(self))
		self.leftButton.clicked.connect(lambda : self.rotateLeftDial(0))
		self.leftButton.hide()

		self.rightButton = QPushButton()
		self.rightButton.setText("Turn Off")
		self.rightButton.clicked.connect(lambda : publishRightAngle(self))
		self.rightButton.clicked.connect(lambda : self.rotateRightDial(0))
		self.rightButton.hide()

		# Dials
		self.dialImage = QPixmap(DIAL_IMG_PATH)

		self.leftDial = QLabel()
		self.leftDial.setMinimumSize(DIAL_DIAG, DIAL_DIAG)
		self.leftDial.setAlignment(Qt.AlignCenter)
		self.leftDial.setPixmap(self.dialImage.scaledToHeight(DIAL_SIZE))

		self.rightDial = QLabel()
		self.rightDial.setMinimumSize(DIAL_DIAG, DIAL_DIAG)
		self.rightDial.setAlignment(Qt.AlignCenter)
		self.rightDial.setPixmap(self.dialImage.scaledToHeight(DIAL_SIZE))

		# Add all to layout
		self.layout.addWidget(titleLabel, 0, 0, 1, 0, Qt.AlignCenter)
		self.layout.addWidget(self.leftStatus, 1, 0, Qt.AlignCenter)
		self.layout.addWidget(self.rightStatus, 1, 1, Qt.AlignCenter)
		self.layout.addWidget(self.leftButton, 2, 0, Qt.AlignCenter)
		self.layout.addWidget(self.rightButton, 2, 1, Qt.AlignCenter)
		self.layout.addWidget(self.leftDial, 3, 0, Qt.AlignCenter)
		self.layout.addWidget(self.rightDial, 3, 1, Qt.AlignCenter)

		# Connect custom signals
		self.updateLeftDial.connect(self.rotateLeftDial)
		self.updateRightDial.connect(self.rotateRightDial)

		widget = QWidget()
		widget.setLayout(self.layout)

		self.setCentralWidget(widget)

	def __rotateDial(self, dial, angle):
		t = QTransform()
		t.rotate(angle)
		dial.setPixmap(self.dialImage.scaledToHeight(DIAL_SIZE).transformed(t))

	def rotateLeftDial(self, angle):
		self.__rotateDial(self.leftDial, angle)
		self.currLeftAngle = angle
		if (angle == 0):
			self.leftButton.hide()
			self.leftStatus.setText("OFF")
		else:
			self.leftButton.show()
			self.leftStatus.setText("ON")

	def rotateRightDial(self, angle):
		self.__rotateDial(self.rightDial, angle)
		self.currRightAngle = angle
		if (angle == 0):
			self.rightButton.hide()
			self.rightStatus.setText("OFF")
		else:
			self.rightButton.show()
			self.rightStatus.setText("ON")

	def getLeftAngle(self):
		return self.currLeftAngle

	def getRightAngle(self):
		return self.currRightAngle

def main():
	app = QApplication(sys.argv)

	window = StoveBotWindow()
	window.show()

	client = startCVSubscriber(window)

	app.exec_()

	stopCVSubscriber(client)

if __name__ == "__main__":
	main()
