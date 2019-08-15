

from PyQt5 import QtCore, QtGui, QtWidgets
import odrive
import time

class odriveWorker(QtCore.QThread):
	# add some signals here
	odrive_found_sig = QtCore.pyqtSignal('PyQt_PyObject')
	def __init__(self):
		QtCore.QThread.__init__(self)
		self._isRunning = True

	def stop(self):
		self._isRunning = False

	def run(self):
		self.my_drive = odrive.find_any()
		self.odrive_found_sig.emit(self.my_drive)

		# while self._isRunning is True:
			# time.sleep(.01)
			# QtWidgets.QApplication.processEvents()
