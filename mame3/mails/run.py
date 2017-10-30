import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from app2 import Ui_Dialog

class MyApp(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # EVENTS
        self.ui.pushAll.clicked.connect(self.fillAll)

    def fillAll(self):
        self.ui.id1.setText('1234567890')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())
