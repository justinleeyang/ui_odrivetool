#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import UI_mainwindow2

import odrive
from odrive.enums import *

import fibre

import json
import glob
import datetime

import os

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

from serialThread import odriveWorker

ICON_TRUE_PATH = "Icons/True.jpg"
ICON_FALSE_PATH = "Icons/False.jpg"
ICON_NOSTATE_PATH = "Icons/NoState.jpg"


def find_parents_list(index):
	subwindow_list = []
	cr = index.model().itemFromIndex(index)
	subwindow_list.append(cr.text())
	if index.parent().isValid():
		i1 = index.parent()
		# print(i1.model().itemFromIndex(i1).text())
		subwindow_list.append(i1.model().itemFromIndex(i1).text())
		if i1.parent().isValid():
			i2 = i1.parent()
			# print(i2.model().itemFromIndex(i2).text())
			subwindow_list.append(i2.model().itemFromIndex(i2).text())
			if i2.parent().isValid():
				i3 = i2.parent()
				# print(i3.model().itemFromIndex(i3).text())
				subwindow_list.append(i3.model().itemFromIndex(i3).text())
				if i3.parent().isValid():
					i4 = i3.parent()
					# print(i4.model().itemFromIndex(i4).text())
					subwindow_list.append(i4.model().itemFromIndex(i4).text())
	return subwindow_list


def add_single_layout_line(path_list, my_drive):
	ra_dict = {}

	if len(path_list) == 2:
		if isinstance(my_drive._remote_attributes[path_list[0]], fibre.remote_object.RemoteFunction):
			ra_dict["layout"] = add_pushButton(path_list)
		elif isinstance(my_drive._remote_attributes[path_list[0]], fibre.remote_object.RemoteProperty):
			ra_dict["layout"] = add_label(path_list, my_drive._remote_attributes[path_list[0]])
	elif len(path_list) == 3:
		if isinstance(my_drive._remote_attributes[path_list[1]]._remote_attributes[path_list[0]], fibre.remote_object.RemoteFunction):
			ra_dict["layout"] = add_pushButton(path_list)
		elif isinstance(my_drive._remote_attributes[path_list[1]]._remote_attributes[path_list[0]], fibre.remote_object.RemoteProperty):
			ra_dict["layout"] = add_label(path_list, my_drive._remote_attributes[path_list[1]]._remote_attributes[path_list[0]])
	elif len(path_list) == 4:
		if isinstance(my_drive._remote_attributes[path_list[2]]._remote_attributes[path_list[1]]._remote_attributes[path_list[0]], fibre.remote_object.RemoteFunction):
			ra_dict["layout"] = add_pushButton(path_list)
		elif isinstance(my_drive._remote_attributes[path_list[2]]._remote_attributes[path_list[1]]._remote_attributes[path_list[0]], fibre.remote_object.RemoteProperty):
			ra_dict["layout"] = add_label(path_list, my_drive._remote_attributes[path_list[2]]._remote_attributes[path_list[1]]._remote_attributes[path_list[0]])
	elif len(path_list) == 5:
		if isinstance(my_drive._remote_attributes[path_list[3]]._remote_attributes[path_list[2]]._remote_attributes[path_list[1]]._remote_attributes[path_list[0]], fibre.remote_object.RemoteFunction):
			ra_dict["layout"] = add_pushButton(path_list)
		elif isinstance(my_drive._remote_attributes[path_list[3]]._remote_attributes[path_list[2]]._remote_attributes[path_list[1]]._remote_attributes[path_list[0]], fibre.remote_object.RemoteProperty):
			ra_dict["layout"] = add_label(path_list, my_drive._remote_attributes[path_list[3]]._remote_attributes[path_list[2]]._remote_attributes[path_list[1]]._remote_attributes[path_list[0]])

	return ra_dict

def add_config_float():
	pass

def add_config_int():
	pass

def add_config_bool():
	pass

def add_pushButton(path_list):
	ra_dict = {}
	ra_dict["pushbutton"] = QtWidgets.QPushButton()
	ra_dict["pushbutton"].setObjectName(path_list[0])
	ra_dict["pushbutton"].setText(path_list[0])
	ra_dict["HLayout"] = QtWidgets.QHBoxLayout()
	ra_dict["HLayout"].addWidget(ra_dict["pushbutton"])
	return ra_dict

def add_label(path_list, remote_attribute):
	ra_dict = {}
	ra_dict["label"] = QtWidgets.QLabel()
	ra_dict["label"].setObjectName(path_list[0])
	ra_dict["label"].setText(path_list[0])

	ra_dict["value"] = QtWidgets.QLabel()
	ra_value = remote_attribute.get_value()

	if type(ra_value) == float:
		ra_dict["value"].setText(str(ra_value))
	elif type(ra_value) == int:
		ra_dict["value"].setText(str(ra_value))
	elif type(ra_value) == bool:
		pixmap_false = QtGui.QPixmap("Icons/False.jpg")
		pixmap_true = QtGui.QPixmap("Icons/True.jpg")
		if ra_value:
			ra_dict["value"].setPixmap(pixmap_true)
		else:
			ra_dict["value"].setPixmap(pixmap_false)
	ra_dict["value_path"] = remote_attribute
	ra_dict["HLayout"] = QtWidgets.QHBoxLayout()
	ra_dict["HLayout"].addWidget(ra_dict["label"])
	ra_dict["HLayout"].addWidget(ra_dict["value"])
	return ra_dict

class CustomMDIArea(QtWidgets.QMdiArea):
	odrive_request_sig = QtCore.pyqtSignal()

	def __init__(self,type, parent=None):
		super(self.__class__, self).__init__()
		# self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
		self.setAcceptDrops(True)
		self.my_drive_list = []
		# self.odrive = fibre.remote_object.RemoteObject()

	def dragEnterEvent(self, event):
		print("drag enter event")
		print(event)
		event.accept()

	def dragMoveEnter(self, event):
		print("drag move enter")
		print(event)

	def add_odrive(self, my_drive):
		self.my_drive = my_drive
		self.my_drive_list.append(my_drive)
		# print(self.odrive)

	def dropEvent(self, event):
		print("drop event")

		subwindow_dict = {}

		for index in event.source().selectedIndexes():

			subwindow_list = find_parents_list(index)

			centralWidget = QtWidgets.QWidget(self)
			str1 = '-'.join(subwindow_list)
			centralWidget.setWindowTitle(str1)
			gridLayout = QtWidgets.QGridLayout(centralWidget)

			print(subwindow_list)
			cr = index.model().itemFromIndex(index)
			# subwindow_list.append(cr.text())
			print(cr.hasChildren())
			if cr.hasChildren():
				print(cr.text())
				# print(type(cr))
				label_list = []
				spinBox_list = []
				for row in range(0,cr.rowCount()):
					print("1 - " + cr.child(row,0).text())
					if cr.child(row, 0).hasChildren():
						for sub_child in range(0, cr.child(row,0).rowCount()):
							print("2 - " + cr.child(row,0).child(sub_child,0).text())
							if cr.child(row,0).child(sub_child,0).hasChildren():
								for sub2_child in range(0, cr.child(row,0).child(sub_child,0).rowCount()):
									print("3 - " + cr.child(row,0).child(sub_child,0).child(sub2_child,0).text())
									if cr.child(row,0).child(sub_child,0).child(sub2_child,0).hasChildren():
										for sub3_child in range(0, cr.child(row,0).child(sub_child,0).child(sub2_child,0).rowCount()):
											print("4 - " + cr.child(row,0).child(sub_child,0).child(sub2_child,0).child(sub3_child,0).text())
											if cr.child(row,0).child(sub_child,0).child(sub2_child,0).child(sub3_child,0).hasChildren():
												for sub4_child in range(0, cr.child(row,0).child(sub_child,0).child(sub2_child,0).child(sub3_child,0).rowCount()):
													print("5 - " + cr.child(row,0).child(sub_child,0).child(sub2_child,0).child(sub3_child,0).child(sub4_child,0).text())
					else:
						print("1 no children")
						sub2_window_list = []
						sub2_window_list.clear()
						sub2_window_list = subwindow_list.copy()
						sub2_window_list.insert(0,cr.child(row,0).text())
						print(sub2_window_list)
						subwindow_dict2 = add_single_layout_line(sub2_window_list, self.my_drive)
						# print(subwindow_dict2)
						gridLayout.addLayout(subwindow_dict2["layout"]["HLayout"], row,0,1,1)
			else:
				print("0 no children")
				subwindow_dict = add_single_layout_line(subwindow_list, self.my_drive)


				# for item in range(0, len(label_list)):
				gridLayout.addLayout(subwindow_dict["layout"]["HLayout"], 0,0,1,1)
				# if "pushbutton" in ra_dict:
				# 	gridLayout.addLayout(ra_dict["layout"]["HLayout"], 0,0,1,1)
				# elif "spinbox" in ra_dict:
				# 	gridLayout.addWidget(ra_dict["label"], 0,0,1,1)
				# 	gridLayout.addWidget(ra_dict["spinbox"], 0,2,1,1)
				# 	gridLayout.addWidget(ra_dict["slider"], 0,1,1,1)
				# elif "doublespinbox" in ra_dict:
				# 	gridLayout.addWidget(ra_dict["label"], 0,0,1,1)
				# 	gridLayout.addWidget(ra_dict["doublespinbox"], 0,2,1,1)
				# 	gridLayout.addWidget(ra_dict["slider"], 0,1,1,1)
				# elif "radiobutton_t" in ra_dict:
				# 	gridLayout.addLayout(ra_dict["HLayout"], 0,0,1,1)
			self.addSubWindow(centralWidget).show()

# ra_dict["label"] = QtWidgets.QLabel()
# ra_dict["label"].setObjectName(subwindow_list[0])
# ra_dict["label"].setText(subwindow_list[0])
# if isinstance(self.my_drive._remote_attributes[subwindow_list[0]].get_value(), float):
# 	# ra_dict["doublespinbox"] = QtWidgets.QDoubleSpinBox()
# 	# ra_dict["slider"] = QtWidgets.QSlider()
# 	# ra_dict["slider"].setOrientation(QtCore.Qt.Horizontal)
# # elif isinstance(self.my_drive._remote_attributes[subwindow_list[0]].get_value(), int):
# elif type(self.my_drive._remote_attributes[subwindow_list[0]].get_value()) == type(int):
# 	# print(type(self.my_drive._remote_attributes[subwindow_list[0]].get_value()))
# 	# ra_dict["spinbox"] = QtWidgets.QSpinBox()
# 	# ra_dict["slider"] = QtWidgets.QSlider()
# 	# ra_dict["slider"].setOrientation(QtCore.Qt.Horizontal)
# elif isinstance(self.my_drive._remote_attributes[subwindow_list[0]].get_value(), bool):
	# print(type(self.my_drive._remote_attributes[subwindow_list[0]].get_value()))

	# ra_dict["radiobutton_t"] = QtWidgets.QRadioButton()
	# ra_dict["radiobutton_f"] = QtWidgets.QRadioButton()
	# icon_false = QtGui.QIcon()
	# icon_false.addPixmap(QtGui.QPixmap("Icons/False.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
	# icon_true = QtGui.QIcon()
	# icon_true.addPixmap(QtGui.QPixmap("Icons/True.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
	# ra_dict["radiobutton_t"].setIcon(icon_true)
	# ra_dict["radiobutton_f"].setIcon(icon_false)
	# ra_dict["HLayout"] = QtWidgets.QHBoxLayout()
	# # HLayout = QtWidgets.QHBoxLayout()
	# buttonGroup = QtWidgets.QButtonGroup(centralWidget)
	# buttonGroup.addButton(ra_dict["radiobutton_t"])
	# buttonGroup.addButton(ra_dict["radiobutton_f"])
	# ra_dict["HLayout"].addWidget(ra_dict["label"])
	# ra_dict["HLayout"].addWidget(ra_dict["radiobutton_t"])
	# ra_dict["HLayout"].addWidget(ra_dict["radiobutton_f"])



	# self.HLayout = QtWidgets.QHBoxLayout()
	# self.HLayout.setSpacing(6)
	# self.HLayout.setObjectName("HLayout")
	# self.radioButton_t = QtWidgets.QRadioButton(self.centralWidget)
	# self.radioButton_t.setText("")
	# self.radioButton_t.setIcon(icon)
	# self.radioButton_t.setObjectName("radioButton_t")
	# self.buttonGroup = QtWidgets.QButtonGroup(MainWindow)
	# self.buttonGroup.setObjectName("buttonGroup")
	# self.buttonGroup.addButton(self.radioButton_t)
	# self.HLayout.addWidget(self.radioButton_t)

	# self.buttonGroup = QtWidgets.QButtonGroup(MainWindow)
	# self.buttonGroup.setObjectName("buttonGroup")
	# self.buttonGroup.addButton(self.radioButton_t)
	# # ra_dict["slider"].setOrientation(QtCore.Qt.Horizontal)

					# print(cr.child(row,0).model().itemFromIndex(child_index))
					# print(cr.child(row,0).model().itemFromIndex(child_index).text())
					# subwindow_list.append(i3.model().itemFromIndex(i3).text())
				# 	print(cr.child(row,0).text())
				# 	label_list.append(QtWidgets.QLabel())
				# 	spinBox_list.append(QtWidgets.QDoubleSpinBox())
				# 	# self.axis1Velocity_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.frame_2)
				# 	# spinBox_list[row]
				# 	label_list[row].setObjectName(cr.child(row,0).text())
				# 	label_list[row].setText(cr.child(row,0).text())
				#
				# centralWidget = QtWidgets.QWidget(self)
				# str1 = '-'.join(subwindow_list)
				# centralWidget.setWindowTitle(str1)
				# gridLayout = QtWidgets.QGridLayout(centralWidget)
				# for item in range(0, len(label_list)):
				# 	gridLayout.addWidget(label_list[item], item,0,1,1)
				# 	gridLayout.addWidget(spinBox_list[item], item,1,1,1)
				# self.addSubWindow(centralWidget).show()





			# print(cr.rowCount()) #on model to Model() and get TExt
				# print(cr.model().index(0,0))
				# first_item = cr.model().itemFromIndex(cr.model().index(0,0)).text()
				# print(first_item)
				# # print(cr.index(1))
				# print(cr.index(2))

		# 	print(cr.text())
		# 	if index.parent().isValid():
		# 		i1 = index.parent()
		# 		print(i1.model().itemFromIndex(i1).text())
		# 		subwindow_list.append(i1.model().itemFromIndex(i1).text())
		# 		if i1.parent().isValid():
		# 			i2 = i1.parent()
		# 			print(i2.model().itemFromIndex(i2).text())
		# 			subwindow_list.append(i2.model().itemFromIndex(i2).text())
		# 			if i2.parent().isValid():
		# 				i3 = i2.parent()
		# 				print(i3.model().itemFromIndex(i3).text())
		# 				subwindow_list.append(i3.model().itemFromIndex(i3).text())
		# 				if i3.parent().isValid():
		# 					i4 = i3.parent()
		# 					print(i4.model().itemFromIndex(i4).text())
		# 					subwindow_list.append(i4.model().itemFromIndex(i4).text())
		#
		# print(subwindow_list)
		# #TODO figure out and add all children
		# label_list = []
		# label_list.append(QtWidgets.QLabel())
		# label_list.append(QtWidgets.QLabel())
		# label_list[0].setObjectName("button0")
		# label_list[1].setObjectName("button1")
		# label_list[1].setText("KLOL")
		#
		# centralWidget = QtWidgets.QWidget(self)
		# gridLayout = QtWidgets.QGridLayout(centralWidget)
		# gridLayout.addWidget(label_list[0], 0,0,1,1)
		# gridLayout.addWidget(label_list[1], 1,0,1,1)
		# self.addSubWindow(centralWidget).show()

		# self.pushButton_123 = QtWidgets.QPushButton()
		# self.pushButton_123.setObjectName("pushButton_123")
		# self.pushButton_1223 = QtWidgets.QPushButton()
		# self.pushButton_1223.setObjectName("pushButton_1233")
		# self.pushButton_1233 = QtWidgets.QPushButton()
		# self.pushButton_1233.setObjectName("pushButton_1223")
		# self.pushButton_1233.setText("KLOL")
		# self.centralWidget222 = QtWidgets.QWidget(self)
		# self.gridLayout555 = QtWidgets.QGridLayout(self.centralWidget222)
		# self.gridLayout555.addWidget(self.pushButton_123, 0,0,1,1)
		# self.gridLayout555.addWidget(self.pushButton_1233, 1,0,1,1)
		# self.gridLayout555.addWidget(self.pushButton_1223, 2,0,1,1)
		# self.addSubWindow(self.centralWidget222).show()



class ExampleApp(QtWidgets.QMainWindow, UI_mainwindow2.Ui_MainWindow):

	app_name = "Odrive Tester"
	def __init__(self):
		# Simple reason why we use it here is that it allows us to
		# access variables, methods etc in the design.py file
		super(self.__class__, self).__init__()
		self.setupUi(self)  # This is defined in design.py file automatically
							# It sets up layout and widgets that are defined
		self.quit_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self)
		self.quit_shortcut.activated.connect(self.close_application)

		# self.treeView.setModel(self.odr_model())
		self.treeView.setDragEnabled(True)
		# self.treeView.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
		# self.treeView.setAcceptDrops(True)
		# self.treeView.setDragDropMode(QtGui.QAbstractItemView.DragOnly)

		# self.pushButton_123 = QtWidgets.QPushButton()
		# self.pushButton_123.setObjectName("pushButton_123")
		# self.mdiArea.addSubWindow(self.pushButton_123)
		# self.mdiArea.dropEvent(self.droping)
		# self.mdiArea.setAcceptDrops(True)

		self.testmdi = CustomMDIArea(self)
		self.testmdi.odrive_request_sig.connect(self.odrive_requested)
		self.gridLayout.addWidget(self.testmdi, 0, 2, 1, 1)

		self.odrive_connect()
		# self.mdiArea.dragMoveEvent(QtGui.QDragMoveEvent())

	def odrive_requested(self):
		self.testmdi.add_odrive(self.my_drive)

	def droping(self):
		print("drop")

	def odr_model(self):
		model = QtGui.QStandardItemModel(0, 1, self)
		model.setHeaderData(0, QtCore.Qt.Horizontal, "Odrive")
		# model.setHeaderData(1, QtCore.Qt.Horizontal, "Graph enable")
		item = QtGui.QStandardItem("axis0")
		child = QtGui.QStandardItem("controller")  # Apple
		childbanana = QtGui.QStandardItem("config")  # Apple
		childApple = QtGui.QStandardItem("vel_limit")  # Apple
		child.appendRow(childbanana)
		child.appendRow(childApple)

		item.appendRow(child)
		child2 = QtGui.QStandardItem("objects4")  # Banana
		item.appendRow(child2)
		model.setItem(0, 0, item)
		item2 = QtGui.QStandardItem("type222")
		model.setItem(1, 0, item2)
		return model


	def load_config_template(self):
		config_template = {}
		with open("config_template.json") as f:
			config_template = json.load(f)
		return config_template

	def close_application(self):
		print("whooaaaa so custom!!!")
		# try:
		# 	self.odrive_worker.stop()
		# except:
		# 	pass
		sys.exit()

	def odrive_connect(self):
		self.odrive_worker = odriveWorker()
		self.odrive_worker.odrive_found_sig.connect(self.odrive_connected)
		self.odrive_worker.start()

	def odrive_connected(self, my_drive):
		self.my_drive = my_drive
		self.testmdi.add_odrive(self.my_drive)
		self.treeView.setModel(self.setup_odrive_model(my_drive))

	def setup_odrive_model(self, my_drive):
		print("Odrive found. Setting up model.")
		# ignore_list = ["test_property", "test_function", "fw_version_revision", "fw_version_major", "fw_version_minor", "enter_dfu_mode",
		# 				"save_configuration", "erase_configuration", "get_oscilloscope_val", "hw_version_major", "hw_version_minor", "fw_version_unreleased",
		# 				"hw_version_variant", "reboot", "get_adc_voltage"]
		ignore_list = ["test_property", "test_function", "fw_version_revision", "fw_version_major", "fw_version_minor", "enter_dfu_mode",
						"get_oscilloscope_val", "hw_version_major", "hw_version_minor", "fw_version_unreleased",
						"hw_version_variant", "get_adc_voltage"]
		# axis_attribute_list = []
		model = QtGui.QStandardItemModel(0, 1, self)
		model.setHeaderData(0, QtCore.Qt.Horizontal, "Odrive")
		# model.setHeaderData(1, QtCore.Qt.Horizontal, "Type")
		 # isinstance(odrv0._remote_attributes["reboot"], fibre.remote_object.RemoteFunction)
		item = QtGui.QStandardItem("odrv0")
		for key in my_drive._remote_attributes.keys():
			# if key not in ignore_list:
			if isinstance(my_drive._remote_attributes[key], fibre.remote_object.RemoteObject):
				child = QtGui.QStandardItem(key)
				for child_key in my_drive._remote_attributes[key]._remote_attributes.keys():
					if isinstance(my_drive._remote_attributes[key]._remote_attributes[child_key], fibre.remote_object.RemoteObject):
						sub1_child = QtGui.QStandardItem(child_key)
						for sub1_child_key in my_drive._remote_attributes[key]._remote_attributes[child_key]._remote_attributes.keys():
							if isinstance(my_drive._remote_attributes[key]._remote_attributes[child_key]._remote_attributes[sub1_child_key], fibre.remote_object.RemoteObject):
								sub2_child = QtGui.QStandardItem(sub1_child_key)
								for sub2_child_key in my_drive._remote_attributes[key]._remote_attributes[child_key]._remote_attributes[sub1_child_key]._remote_attributes.keys():
									if isinstance(my_drive._remote_attributes[key]._remote_attributes[child_key]._remote_attributes[sub1_child_key]._remote_attributes[sub2_child_key], fibre.remote_object.RemoteObject):
										sub3_child = QtGui.QStandardItem(sub2_child_key)
										sub2_child.appendRow(sub3_child)
									else:
										sub3_child = QtGui.QStandardItem(sub2_child_key)
										sub2_child.appendRow(sub3_child)
								sub1_child.appendRow(sub2_child)
							else:
								sub2_child = QtGui.QStandardItem(sub1_child_key)
								sub1_child.appendRow(sub2_child)
						child.appendRow(sub1_child)
					else:
						sub1_child = QtGui.QStandardItem(child_key)
						child.appendRow(sub1_child)
					# elif
				item.appendRow(child)
			else:
				if key not in ignore_list:
					child = QtGui.QStandardItem(key)
					item.appendRow(child)

		child = QtGui.QStandardItem("fw_version")
		item.appendRow(child)
		child = QtGui.QStandardItem("hw_version")
		item.appendRow(child)

		model.setItem(0,0,item)
		# self.testmdi.show()
		return model



def main():
	app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
	form = ExampleApp()                 # We set the form to be our (design)
	form.show()                         # Show the form
	app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
	main()                              # run the main function
