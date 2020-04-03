# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QLineEdit, QFileDialog
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PIL import Image
import sys

# Devices
class Device:
	def __init__(self, x, y, width, height, src, title):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.src = src
		self.title = title

class Mocker:
	def __init__(self):
		self.app = QApplication(sys.argv)
		self.window = QWidget()
		self.window.setMinimumSize(QSize(500, 300))
		self.window.setWindowTitle('Mock Screens.')

		# Main Layout
		self.layout = QVBoxLayout()

		# Devices
		tablet_portrait = Device(96, 113, 681, 911, ":imgs/tablet_portrait.png", "Tablet Portrait")
		tablet_landscape = Device(140, 97, 912, 681, ":imgs/tablet_landscape.png", "Tablet Landscape")
		phone_portrait = Device(83, 101, 482, 858, ":imgs/telefone_portrait.png", "Phone Landscape")
		phone_landscape = Device(103, 80, 859, 483, ":imgs/telefone_landscape.png", "Phone Portrait")

		self.devices = [tablet_portrait, tablet_landscape, phone_portrait, phone_landscape]

		self.labelImgMock = QLabel("Frame")
		self.layout.addWidget(self.labelImgMock)

		self.listDevices = QListWidget()
		self.layout.addWidget(self.listDevices)

		for item in self.devices:
			itemWidget = QListWidgetItem(item.title)
			itemWidget.setIcon(QIcon(item.src))

			self.listDevices.addItem(itemWidget)

		# Images
		self.labelImgs = QLabel('Images to Frame')
		self.layout.addWidget(self.labelImgs)

		self.imageSelectLayout = QHBoxLayout()

		self.inputImgMock = QLineEdit()
		self.imageSelectLayout.addWidget(self.inputImgMock)

		self.btnSelecionarArquivoImport = QPushButton("Search")
		self.btnSelecionarArquivoImport.clicked.connect(self.selectImagesToMock)
		self.imageSelectLayout.addWidget(self.btnSelecionarArquivoImport)

		self.layout.addLayout(self.imageSelectLayout)

		# Folder to Export
		self.labelFolderExport = QLabel('Folder which will receive framed images')
		self.layout.addWidget(self.labelFolderExport)

		self.folderSelectLayout = QHBoxLayout()

		self.inputFolderExport = QLineEdit()
		self.folderSelectLayout.addWidget(self.inputFolderExport)

		self.btnSelecionarArquivoExport = QPushButton("Search")
		self.btnSelecionarArquivoExport.clicked.connect(self.selectFolderToExport)
		self.folderSelectLayout.addWidget(self.btnSelecionarArquivoExport)

		self.layout.addLayout(self.folderSelectLayout)

		# Execution buttons
		self.btnRun = QPushButton("Run")
		self.btnRun.clicked.connect(self.runMocks)

		self.btnCancel = QPushButton('Cancel')
		self.btnCancel.clicked.connect(self.cancel)

		self.btnLayout = QHBoxLayout()
		self.btnLayout.addStretch(1)
		self.btnLayout.addWidget(self.btnRun)
		self.btnLayout.addWidget(self.btnCancel)

		self.layout.addLayout(self.btnLayout)

		# Turn window visible
		self.window.setLayout(self.layout)
		self.window.show()

	def cancel(self):
		self.app.quit()
		sys.exit()

	def selectImagesToMock(self):
		files = QFileDialog.getOpenFileNames(self.window, 'Select the images', '', 'PNG Files (*.png) ;; JPG Files (*.jpg) ;; JPEG Files (*.jpeg)')
		strFiles = ''

		for file in files:
			if(strFiles == ''):
				strFiles += file[0]
			else:
				strFiles += ','
				strFiles += file[0]

		self.inputImgMock.setText(files)

	def selectFolderToExport(self):
		directory = str(QFileDialog.getExistingDirectory(self.window, "Select a directory"))
		self.inputFolderExport.setText(directory)

	def runMocks(self):
		imagens = self.master.tk.splitlist(self.inputImgMock.get())
		index = map(int, self.listDevices.curselection())
		pasta = self.inputFolderExport.get()

		if(len(index) == 0):
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)

			msg.setText("Image Frame not selected")
			msg.setWindowTitle("Oops")
			msg.setStandardButtons(QMessageBox.Ok)

			return

		if(len(imagens) == 0):
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)

			msg.setText("Images not selected")
			msg.setWindowTitle("Oops")
			msg.setStandardButtons(QMessageBox.Ok)

			return

		dispositivo = self.devices[index[0]]
		background = Image.open(dispositivo.src)

		for i in range(len(imagens)):
			img = imagens[i]
			foreground = Image.open(img).resize((dispositivo.width, dispositivo.height), Image.ANTIALIAS) # LANCZOS version 2.7
			final = Image.new("RGBA", background.size)
			final.paste(background, (0, 0), background)
			
			final.paste(foreground, (dispositivo.x, dispositivo.y), foreground)
			final.save(pasta + "/" + str(i + 1) + ".png")
			i += 1

	def run(self):
		# Start the event loop
		sys.exit(self.app.exec_())

# Start Application
app = Mocker()
app.run()
