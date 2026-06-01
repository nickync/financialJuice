import enaml
from enaml.qt.qt_application import QtApplication
from model.NewsItem import NewsItem
from controller.news_controller import NewsController


def main():
    app = QtApplication()

    with enaml.imports():
        from ui.app_enaml import NewsWindow

    window = NewsWindow()

    news_controller = NewsController(window)
    
    # window.news_items = [NewsItem(title="Sample News 1", content="This is the first sample news item.", time=1234567890, importance=5, category="Equities", source="Sample Source"),
    #                      NewsItem(title="Sample News 2", content="This is the second sample news item.", time=1234567891, importance=5, category="Bonds", source="Sample Source"),
    #                      NewsItem(title="Sample News 3", content="This is the third sample news item.", time=1234567892, importance=5, category="Crypto", source="Sample Source"),
    #                         NewsItem(title="Sample News 4", content="This is the fourth sample news item.", time=1234567893, importance=5, category="Forex", source="Sample Source"),
    #                         NewsItem(title="Sample News 5", content="This is the fifth sample news item.", time=1234567894, importance=5, category="Indexes", source="Sample Source"),]

    def on_close():
        news_controller.stop()

    window.news_items = news_controller.news_items

    window.show()
    
    app.start()

if __name__ == "__main__":
    main()
