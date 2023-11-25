import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from Widgets.Window import Base 


app = QApplication(sys.argv)
B = Base()
B.show()
app.exec()