import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QApplication
from PyQt5 import uic

from OpenGL.GL import *
from OpenGL.GLU import *

SPHERE_RADIUS_1 = 0.9
SPHERE_RADIUS_2 = 0.6
CYLINDER_RADIUS = 0.2
GREEN = [0.0, 1.0, 0.0, 1.0]
YELLOW = [1.0, 1.0, 0.0, 1.0]


class MainForm(QtWidgets.QMainWindow):
    def __init__(self, *args):
        super(MainForm, self).__init__(*args)
        self.resetScene()
        self.lastPos = None
        uic.loadUi("ui/MainForm.ui", self)
        self.setupUi()

    def setupUi(self):
        self.windowHeight = self.openGLWidget.height()
        self.windowWidth = self.openGLWidget.width()
        self.openGLWidget.initializeGL()
        self.openGLWidget.resizeGL(self.windowWidth, self.windowHeight)
        self.openGLWidget.paintGL = self.paintGL
        self.openGLWidget.initializeGL = self.initializeGL

        self.pB_xUp.clicked.connect(self.xUp)
        self.pB_xDown.clicked.connect(self.xDown)
        self.pB_yUp.clicked.connect(self.yUp)
        self.pB_yDown.clicked.connect(self.yDown)
        self.pB_zUp.clicked.connect(self.zUp)
        self.pB_zDown.clicked.connect(self.zDown)
        self.pB_reset.clicked.connect(self.resetScene)
        self.pB_perUp.clicked.connect(self.perUp)
        self.pB_perDown.clicked.connect(self.perDown)

    def resizeEvent(self, event):
        size = event.size()
        self.openGLWidget.resize(size.width() - 130, size.height() - 21)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            dx = event.x() - self.lastPos.x()
            dy = event.y() - self.lastPos.y()
            self.xRot += dy
            self.yRot += dx
            self.lastPos = event.pos()
            self.update()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.perDown()
        else:
            self.perUp()
        self.update()

    def initializeGL(self):
        glClearColor(0.5, 0.5, 0.5, 1.0)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)

        lightPosition = [10.0, -30.0, 10.0, 1.0]
        lightColor = [0.9, 0.9, 0.9, 1.0]
        glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
        glEnable(GL_LIGHT0)

    def loadScene(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(
            self.perspective,
            self.windowWidth / float(self.windowHeight or 1),
            0.1,
            100
        )

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(
            10, -30, 15,
            0, 0, 1,
            0, 0, 1
        )

    def paintGL(self):
        self.loadScene()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()

        glRotate(self.xRot, 1.0, 0.0, 0.0)
        glRotate(self.yRot, 0.0, 1.0, 0.0)
        glRotate(self.zRot, 0.0, 0.0, 1.0)
        glScalef(self.zoom, self.zoom, self.zoom)
        # glTranslatef(0.0, 0.0, self.zoom)

        glPushMatrix()
        glTranslate(-4.0, 4.0, -4.0)
        glRotate(90, 1.0, 0.0, 0.0)
        self.Na_Cl()
        glPopMatrix()

        glPopMatrix()

        self.openGLWidget.update()

    def firts_layer(self, object):
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, GREEN)
        gluSphere(object, SPHERE_RADIUS_1, 100, 100)

        glPushMatrix()
        glTranslate(0.0, 0.0, 8.0)
        gluSphere(object, SPHERE_RADIUS_1, 100, 100)
        glPopMatrix()

        glPushMatrix()
        glTranslate(8.0, 0.0, 0.0)
        gluSphere(object, SPHERE_RADIUS_1, 100, 100)
        glPopMatrix()

        glPushMatrix()
        glTranslate(8.0, 0.0, 8.0)
        gluSphere(object, SPHERE_RADIUS_1, 100, 100)
        glPopMatrix()

        glPushMatrix()
        glTranslate(4.0, 0.0, 4.0)
        gluSphere(object, SPHERE_RADIUS_1, 100, 100)
        glPopMatrix()

        glPushMatrix()
        glTranslate(4.0, 0.0, 4.0)
        gluSphere(object, SPHERE_RADIUS_1, 100, 100)
        glPopMatrix()

        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, YELLOW)
        glPushMatrix()
        glTranslate(4.0, 0.0, 0.0)
        gluSphere(object, SPHERE_RADIUS_2, 100, 100)
        glPopMatrix()

        glPushMatrix()
        glTranslate(0.0, 0.0, 4.0)
        gluSphere(object, SPHERE_RADIUS_2, 100, 100)
        glPopMatrix()

        glPushMatrix()
        glTranslate(4.0, 0.0, 8.0)
        gluSphere(object, SPHERE_RADIUS_2, 100, 100)
        glPopMatrix()

        glPushMatrix()
        glTranslate(8.0, 0.0, 4.0)
        gluSphere(object, SPHERE_RADIUS_2, 100, 100)
        glPopMatrix()

    def secondLayer(self, object):

        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, YELLOW)
        gluSphere(object, SPHERE_RADIUS_2, 100, 100)

        glPushMatrix()
        glTranslate(0.0, 0.0, 8.0)
        gluSphere(object, SPHERE_RADIUS_2, 100, 100)
        glPopMatrix()

        glPushMatrix()
        glTranslate(8.0, 0.0, 0.0)
        gluSphere(object, SPHERE_RADIUS_2, 100, 100)
        glPopMatrix()

        glPushMatrix()
        glTranslate(8.0, 0.0, 8.0)
        gluSphere(object, SPHERE_RADIUS_2, 100, 100)
        glPopMatrix()

        glPushMatrix()
        glTranslate(4.0, 0.0, 4.0)
        gluSphere(object, SPHERE_RADIUS_2, 100, 100)
        glPopMatrix()

        glPushMatrix()
        glTranslate(4.0, 0.0, 4.0)
        gluSphere(object, SPHERE_RADIUS_2, 100, 100)
        glPopMatrix()

        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, GREEN)
        glPushMatrix()
        glTranslate(4.0, 0.0, 0.0)
        gluSphere(object, SPHERE_RADIUS_1, 100, 100)
        glPopMatrix()

        glPushMatrix()
        glTranslate(0.0, 0.0, 4.0)
        gluSphere(object, SPHERE_RADIUS_1, 100, 100)
        glPopMatrix()

        glPushMatrix()
        glTranslate(4.0, 0.0, 8.0)
        gluSphere(object, SPHERE_RADIUS_1, 100, 100)
        glPopMatrix()

        glPushMatrix()
        glTranslate(8.0, 0.0, 4.0)
        gluSphere(object, SPHERE_RADIUS_1, 100, 100)
        glPopMatrix()

    def cell(self, object):
        glPushMatrix()
        gluCylinder(object, CYLINDER_RADIUS, CYLINDER_RADIUS, 8, 100, 100)
        glPopMatrix()

        glPushMatrix()
        glTranslate(8.0, 0.0, 0.0)
        gluCylinder(object, CYLINDER_RADIUS, CYLINDER_RADIUS, 8, 100, 100)
        glPopMatrix()

        glPushMatrix()
        glTranslate(4.0, 0.0, 0.0)
        gluCylinder(object, CYLINDER_RADIUS, CYLINDER_RADIUS, 8, 100, 100)
        glPopMatrix()

        glPushMatrix()
        glRotate(90, 0.0, 1.0, 0.0)
        gluCylinder(object, CYLINDER_RADIUS, CYLINDER_RADIUS, 8, 100, 100)
        glPopMatrix()

        glPushMatrix()
        glTranslate(0.0, 0.0, 4.0)
        glRotate(90, 0.0, 1.0, 0.0)
        gluCylinder(object, CYLINDER_RADIUS, CYLINDER_RADIUS, 8, 100, 100)
        glPopMatrix()

        glPushMatrix()
        glTranslate(0.0, 0.0, 8.0)
        glRotate(90, 0.0, 1.0, 0.0)
        gluCylinder(object, CYLINDER_RADIUS, CYLINDER_RADIUS, 8, 100, 100)
        glPopMatrix()

    def Na_Cl(self):
        # Рисуем сферы

        object = gluNewQuadric()
        # Первый слой
        self.firts_layer(object)

        # Второй слой
        glPushMatrix()
        glTranslate(0.0, 8.0, 0.0)
        self.firts_layer(object)
        glPopMatrix()

        # Третий слой
        glPushMatrix()
        glTranslate(0.0, 4.0, 0.0)
        self.secondLayer(object)
        glPopMatrix()

        # Рисуем связи между сферами
        color = [1.0, 1.0, 1.0, 1.0]
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, color)

        self.cell(object)

        glPushMatrix()
        glTranslate(0.0, 8.0, 0.0)
        self.cell(object)
        glPopMatrix()

        glPushMatrix()
        glTranslate(0.0, 4.0, 0.0)
        self.cell(object)
        glPopMatrix()

        glPushMatrix()
        glRotate(-90, 1.0, 0.0, 0.0)
        self.cell(object)
        glPopMatrix()

        glPushMatrix()
        glRotate(-90, 1.0, 0.0, 0.0)
        glTranslate(0.0, -4.0, 0.0)
        self.cell(object)
        glPopMatrix()

        glPushMatrix()
        glRotate(-90, 1.0, 0.0, 0.0)
        glTranslate(0.0, -8.0, 0.0)
        self.cell(object)
        glPopMatrix()

    def resetScene(self):
        self.perspective = 30
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.zoom = 1

    def xUp(self):
        self.xRot += 10
        self.paintGL()

    def xDown(self):
        self.xRot -= 10
        self.paintGL()

    def yUp(self):
        self.yRot += 10
        self.paintGL()

    def yDown(self):
        self.yRot -= 10
        self.paintGL()

    def zUp(self):
        self.zRot += 10
        self.paintGL()

    def zDown(self):
        self.zRot -= 10
        self.paintGL()

    def perUp(self):
        if self.perspective < 90:
            self.perspective += 5

    def perDown(self):
        if self.perspective > 5:
            self.perspective -= 5


def main():
    app = QApplication(sys.argv)
    window = MainForm()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
