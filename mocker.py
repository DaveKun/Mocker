# -*- coding: utf-8 -*-

from Tkinter import Tk, Label, Entry, Button, Listbox, END
from PIL import Image
import sys
import tkFileDialog as filedialog
import tkMessageBox as MessageBox

# Devices
class Dispositivos:
	def __init__(self, x, y, width, height, src, titulo):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.src = src
		self.titulo = titulo

class Mocker:
	def __init__(self):
		self.master = Tk()
		self.master.geometry("500x250")
		self.master.title('Mock Screens.')

		# Devices
		tablet_portrait = Dispositivos(96, 113, 681, 911, "tablet_portrait.png", "Tablet Portrait")
		tablet_landscape = Dispositivos(140, 97, 912, 681, "tablet_landscape.png", "Tablet Landscape")
		phone_portrait = Dispositivos(83, 101, 482, 858, "telefone_portrait.png", "Phone Landscape")
		phone_landscape = Dispositivos(103, 80, 859, 483, "telefone_landscape.png", "Phone Portrait")

		self.dispositivos = [tablet_portrait, tablet_landscape, phone_portrait, phone_landscape]

		self.labelImgMock = Label(self.master, text="Frame")
		self.labelImgMock.place( x=10, y=5 )

		self.listDispositivos = Listbox(self.master)
		self.listDispositivos.place( x=10, y=30, width=480, height=36 )

		for item in self.dispositivos:
			self.listDispositivos.insert(END, item.titulo)

		# Images
		self.labelImgMock = Label(self.master, text="Images to Frame")
		self.labelImgMock.place( x=10, y=70 )

		self.inputImgMock = Entry(self.master, width=43)
		self.inputImgMock.place( x=10, y=100 )

		self.btnSelecionarArquivoImport = Button(self.master, text="Search", command=self.selecionaMock)
		self.btnSelecionarArquivoImport.place( x=410, y=100 )

		# Folder to Export
		self.labelFolderExport = Label(self.master, text="Folder which will receive framed images")
		self.labelFolderExport.place( x=10, y=130 )

		self.inputFolderExport = Entry(self.master, width=43)
		self.inputFolderExport.place( x=10, y=160 )

		self.btnSelecionarArquivoExport = Button(self.master, text="Search", command=self.selecionaPastaExport)
		self.btnSelecionarArquivoExport.place( x=410, y=160 )

		# Execution buttons
		self.btnExecutar = Button(self.master, text="Run", command=self.executaMocks)
		self.btnExecutar.place( x=410, y=200 )

		self.btnCancelar = Button(self.master, text="Cancel", command=self.cancelar)
		self.btnCancelar.place( x=325, y=200 )

	def cancelar(self):
		self.master.destroy()

	def selecionaMock(self):
		tiposArquivos = [('PNG Images', '.png'),('JPG Images', '.jpg'), ('JPEG Images', '.jpeg')]
		fl = filedialog.askopenfilenames(parent=self.master, filetypes=tiposArquivos, title="Selecione os arquivos")
		self.inputImgMock.insert(0, fl)

	def selecionaPastaExport(self):
		folder = filedialog.askdirectory(parent=self.master)
		self.inputFolderExport.insert(0, folder)

	def executaMocks(self):
		imagens = self.master.tk.splitlist(self.inputImgMock.get())
		index = map(int, self.listDispositivos.curselection())
		pasta = self.inputFolderExport.get()

		if(len(index) == 0):
			MessageBox.showwarning("Oops","Image Frame not selected")
			return

		if(len(imagens) == 0):
			MessageBox.showwarning("Oops","Images not selected")
			return

		dispositivo = self.dispositivos[index[0]]
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
		self.master.mainloop()

# Start
app = Mocker()
app.run()
