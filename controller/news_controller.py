import threading
import time
from typing import List
from model.NewsItem import NewsItem
from services.crawler import Crawler
import logging as log
import enaml.application


class NewsController:
    def __init__(self, window, fetch_interval: int = 10):
        self.crawler = Crawler()
        self.window = window
        self.fetch_interval = fetch_interval
        self.running = True
        self.thread = None
        self.news_items = []
        self.titles = set()

        self.start_fetching()

        #load from db?

    def start_fetching(self):
        self.thread = threading.Thread(target=self._fetch_loop, daemon=True)
        self.thread.start()

    def _fetch_loop(self):
        while self.running:
            try:
                log.info("Starting news fetch loop.")
                INITIAL_LOAD = not self.news_items
                if not self.window.news_items:
                    new_articles = self.crawler.fetch_news(2, initial_load=INITIAL_LOAD)
                else:
                    new_articles = self.crawler.fetch_news(0)

                new_count = 0

                for article in new_articles:
                    if INITIAL_LOAD:
                        self.news_items.append(article)
                        self.titles.add(article.title)
                        new_count += 1
                    elif article.title not in self.titles:
                        self.news_items.insert(0, article)
                        self.titles.add(article.title)
                        new_count += 1
                
                if new_count > 0:
                    print(f"Fetched {new_count} new articles")
                    self.update_ui()
            
                time.sleep(self.fetch_interval)

            except Exception as e:
                print(f"Error in fetch loop: {e}")
                time.sleep(self.fetch_interval)

    def update_ui(self):
        from enaml.qt.qt_application import QtApplication

        def update(items):
            self.window.news_items = [article for article in items]
        
        enaml.application.deferred_call(update, self.news_items)

    def filter(self, keyword: str):
        if keyword:
            filtered = [item for item in self.news_items if not 'truth social posts' in item.time.lower()]
            self.news_items = filtered
        else:
            self.news_items = [article for article in self.news_items]
        
        self.update_ui()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)