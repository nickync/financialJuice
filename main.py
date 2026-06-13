import enaml
from enaml.qt.qt_application import QtApplication
from model.NewsItem import NewsItem
from controller.news_controller import NewsController
import logging as log


def main():
    log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    app = QtApplication()

    with enaml.imports():
        from ui.app_enaml import NewsWindow

    window = NewsWindow()

    news_controller = NewsController(window)
    
    def on_close():
        news_controller.crawler.close()
        news_controller.stop()

    window.show()
    
    app._qapp.aboutToQuit.connect(on_close)
    
    app.start()

if __name__ == "__main__":
    main()
