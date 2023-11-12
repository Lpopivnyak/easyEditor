from PyQt5.QtWidgets import *
import os
from PIL import Image
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

app = QApplication([])
window = QWidget()

photoCell = QLabel()

fileButton = QPushButton("Папка")
steerLeftButton = QPushButton("Вліво")
steerRightButton = QPushButton("Вправо")
mirrorButton = QPushButton("Дзеркало")
sharpnessButton = QPushButton("Різкість")
BWButton = QPushButton("Ч/Б")

listFileButton = QListWidget()

mainLine = QHBoxLayout()
extraLine1 = QVBoxLayout()
extraLine2 = QVBoxLayout()
extraLine3 = QHBoxLayout()

def pil2pixmap(im):
    if im.mode == "RGB":
        r, g, b = im.split()
        im = Image.merge("RGB", (b, g, r))
    elif im.mode == "RGBA":
        r, g, b, a = im.split()
        im = Image.merge("RGBA", (b, g, r, a))
    elif im.mode == "L":
        im = im.convert("RGBA")
    im2 = im.convert("RGBA")
    data = im2.tobytes("raw", "RGBA")
    qim = QImage(data, im.size[0], im.size[1], QImage.Format_ARGB32)
    pixmap = QPixmap.fromImage(qim)
    return pixmap

extraLine1.addWidget(fileButton)
extraLine1.addWidget(listFileButton)
mainLine.addLayout(extraLine1)

extraLine2.addWidget(photoCell)
mainLine.addLayout(extraLine2)

extraLine3.addWidget(steerLeftButton)
extraLine3.addWidget(steerRightButton)
extraLine3.addWidget(mirrorButton)
extraLine3.addWidget(sharpnessButton)
extraLine3.addWidget(BWButton)
extraLine2.addLayout(extraLine3)

class WorkPhoto:
    def __init__(self):
        self.image = None
        self.folder = None
        self.filename = None

    def load(self):
        imagePath = os.path.join(self.folder, self.filename)
        self.image = Image.open(imagePath)

    def showImage(self):
        pixel = pil2pixmap(self.image)
        pixel = pixel.scaled(800, 600, Qt.KeepAspectRatio)
        photoCell.setPixmap(pixel)

    def leftRotate(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.showImage()

    def rightRotate(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.showImage()

photoWork = WorkPhoto()

def openFile():
    photoWork.folder = QFileDialog.getExistingDirectory()
    files = os.listdir(photoWork.folder)
    listFileButton.clear()
    listFileButton.addItems(files)

def showImage():
    photoWork.filename = listFileButton.currentItem().text()
    photoWork.load()
    photoWork.showImage()


listFileButton.currentRowChanged.connect(showImage)
fileButton.clicked.connect(openFile)
steerLeftButton.clicked.connect(photoWork.leftRotate)
steerRightButton.clicked.connect(photoWork.rightRotate)
window.setLayout(mainLine)
window.show()
app.exec()