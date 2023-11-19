from PyQt5.QtWidgets import *
import os
from PIL import Image, ImageFilter
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
unSharpnessButton = QPushButton("Нерізкість")
BWbutton = QPushButton("Ч/Б")
erosionButton = QPushButton("Розмивання")

listFileButton = QListWidget()

mainLine = QHBoxLayout()
extraLine1 = QVBoxLayout()
extraLine2 = QVBoxLayout()
extraLine3 = QHBoxLayout()
extraLine4 = QHBoxLayout()

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
extraLine3.addWidget(unSharpnessButton)
extraLine3.addWidget(BWbutton)
extraLine2.addLayout(extraLine3)

extraLine4.addWidget(erosionButton)
extraLine2.addLayout(extraLine4)

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

    def mirrorEffect(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.showImage()

    def sharpnessEffect(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.showImage()

    def unSharpnessEffect(self):
        self.image = self.image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
        self.showImage()

    def BWeffect(self):
        self.image = self.image.convert("L")
        self.showImage()

    def erosionEffect(self):
        self.image = self.image.filter(ImageFilter.BLUR)
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
mirrorButton.clicked.connect(photoWork.mirrorEffect)
sharpnessButton.clicked.connect(photoWork.sharpnessEffect)
unSharpnessButton.clicked.connect(photoWork.unSharpnessEffect)
BWbutton.clicked.connect(photoWork.BWeffect)
erosionButton.clicked.connect(photoWork.erosionEffect)


window.setLayout(mainLine)
window.show()
app.exec()