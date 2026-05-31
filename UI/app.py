import enaml
from enaml.qt.qt_application import QtApplication

def main():
    app = QtApplication()

    with enaml.imports():
        from app_enaml import NewsWindow

    window = NewsWindow()


    window.show()
    
    app.start()

if __name__ == "__main__":
    main()