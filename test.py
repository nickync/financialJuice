# test_main.py
from enaml.qt.qt_application import QtApplication
import enaml

def main():
    with enaml.imports():
        from testw import TestWindow
    
    app = QtApplication()
    view = TestWindow()
    view.show()
    app.start()

if __name__ == '__main__':
    main()