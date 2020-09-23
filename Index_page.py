# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QPushButton,QLineEdit,QMessageBox, QVBoxLayout,QRadioButton,QListWidget,QListWidgetItem ,QHBoxLayout,QFormLayout,QGroupBox,QScrollArea
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QScrollArea Test')
        self.setGeometry(400, 400, 400, 800)

        formLayout = QFormLayout()
        groupBox = QGroupBox()

        for n in range(10):
            label1 = QLabel('Slime_%2d' % n)
            label2 = QLabel()
            label2.setPixmap(QPixmap('./C.png'))
            label = QLabel(self)
            pixmap = QPixmap(str('%s.jpg'%str(n)))
            label.setFixedSize(200,300)
    #         self.label.setGeometry(40,20,200,300)
            label.setPixmap(pixmap)
            formLayout.addRow(label1, label2)

        groupBox.setLayout(formLayout)

        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
