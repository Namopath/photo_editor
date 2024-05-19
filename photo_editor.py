from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QFileDialog
import os
from PyQt5.QtCore import Qt
from PIL import Image, ImageFilter
from PyQt5.QtGui import *

app = QApplication([])
win = QWidget()
win.setWindowTitle('Easy editor application')
win.resize(700,400)


folder = QPushButton('Folder')
list1 = QListWidget()

b1 = QPushButton('Left')
b2 = QPushButton('Right')
b3 = QPushButton('Mirror')
b4 = QPushButton('Sharpness')
b5 = QPushButton('B/W')
label2 = QLabel('Image')

mainh = QHBoxLayout(win)
v1 = QVBoxLayout()
mainh.addLayout(v1, 25)
#h1 = QHBoxLayout()
#v1.addLayout(h1)
v1.addWidget(folder)
v1.addWidget(list1)
v2 = QVBoxLayout()
#h1.addLayout(v2)
#h2 = QHBoxLayout()
#v1.addLayout(h2)
h3 = QHBoxLayout()
v2.addWidget(label2)
v2.addLayout(h3)
h3.addWidget(b1)
h3.addWidget(b2)
h3.addWidget(b3)
h3.addWidget(b4)
h3.addWidget(b5)
mainh.addLayout(v2, 75)
win.setLayout(mainh)

workdir = ''
def chooseworkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
    


def filter(filenames, extensions):
    results = []
    for name in filenames:
        for extension in extensions:
            if name.endswith(extension):
                results.append(name)
    return results

def showFileNameList():
    chooseworkdir()
    filenames = os.listdir(workdir)
    extensions = ['.jpg','.png','.bmp','.jpeg']
    result = filter(filenames, extensions)
    list1.clear()
    list1.addItems(result)
    

class ImageProcessor():
    
    def __init__(self):
        self.filename = None
        self.original = None
        self.foldername = 'modified/'
    
    def openimage(self,dir ,filename):
        self.dir = dir
        self.filename = filename
        file_path = os.path.join(dir, filename)
        self.original = Image.open(file_path)
        
    def ShowImage(self, file_path):
        label2.hide()
        pixmapimage = QPixmap(file_path)
        w, h = label2.width(), label2.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        label2.setPixmap(pixmapimage)
        label2.show()
        
    def saveImage(self):
        path = os.path.join(workdir, self.foldername)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)    
        self.original.save(image_path)
    
    def do_bw(self):
        self.original = self.original.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.foldername, self.filename)
        self.ShowImage(image_path)
        
    def flip_left(self):
        self.original = self.original.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.foldername, self.filename)
        self.ShowImage(image_path)
    
    def flip_right(self):
        self.original= self.original.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.foldername, self.filename)
        self.ShowImage(image_path)
        
    def mirror(self):
        self.original = self.original.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.foldername, self.filename)
        self.ShowImage(image_path)
        
    def sharpen(self):
        self.original = self.original.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.foldername, self.filename)
        self.ShowImage(image_path)
        
        
workimage = ImageProcessor()
    
def ShowChosenImage():
    if list1.currentRow() >= 0:
        filename = list1.currentItem().text()
        workimage.openimage(workdir, filename)
        path = os.path.join(workdir, workimage.filename)
        workimage.ShowImage(path)


    
b5.clicked.connect(workimage.do_bw)
list1.currentRowChanged.connect(ShowChosenImage)        
folder.clicked.connect(showFileNameList)
b1.clicked.connect(workimage.flip_left)
b2.clicked.connect(workimage.flip_right)
b3.clicked.connect(workimage.mirror)
b4.clicked.connect(workimage.sharpen)

win.show()
app.exec_()

