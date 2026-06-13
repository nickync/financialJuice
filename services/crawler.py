import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from typing import List
from model.NewsItem import NewsItem
import time
import logging as log
import os
import tempfile
import platform


class Crawler:
    def __init__(self, url: str = "https://financialjuice.com"):
        self.base_url = url
        self.driver = None

    def _get_driver(self):
        if self.driver is None:
            options = Options()
            
            #options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-dev-shm-usage")
            #options.add_argument("--disable-blink-features=AutomationControlled")
            #options.add_argument("--disable-extensions")
            #options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')

            #options.add_experimental_option("excludeSwitches", ["enable-automation"])
            #options.add_experimental_option('useAutomationExtension', False)


            profile_path = os.path.join(os.getcwd(), "chrome_profile")

            os.makedirs(profile_path, exist_ok=True)

            options.add_argument(f"--user-data-dir={profile_path}")

            service = Service(ChromeDriverManager().install())

            log.info("Initializing Selenium WebDriver with ChromeDriverManager.")
            self.driver = webdriver.Chrome(service=service, options=options)

            log.info("Selenium WebDriver initialized successfully before execute script.")

            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            log.info("Initialized Selenium WebDriver with anti-detection measures.")
            # self.driver.execute_script("""
            #                            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            #                            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            #                            """)

            self.driver.minimize_window()

        return self.driver
    
    def _scroll_and_load(self, driver, scroll_pause: float = 2):
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def fetch_news(self, max_scrolls: int = 2, initial_load = False) -> List[NewsItem]:
        log.info(f"Starting news fetch from {self.base_url}")
        driver = self._get_driver()
        news_items = []

        try:
            log.info(f"Navigating to {self.base_url}")
            driver.get(self.base_url)
            time.sleep(3)
            if initial_load:
                for _ in range(max_scrolls):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(5)

            log.info("Finished scrolling to load dynamic content.")

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            html = driver.page_source
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")

            articles = self._find_articles(soup)

            for article in articles:
                title = self._extract_title(article)
                content = self._extract_content(article)
                source = self._extract_source(article)
                category = self._extract_category(article)
                timestamp = self._extract_timestamp(article)
                link = self._extract_link(article)
                critical = self._is_critical(article)
                if title:
                    news_items.append(NewsItem(
                        title=title,
                        content=content,
                        source=source,
                        category=category,
                        time=timestamp,
                        link=link,
                        critical=critical
                    ))

        except Exception as e:
            print(f"An error occurred: {e}")

        return news_items
    
    def _find_articles(self, soup):
        return soup.find_all("div", class_="headline-item")
    
    def _extract_title(self, article):
        title_tag = article.find("p", class_="headline-title")
        if title_tag:
            title_text = title_tag.get_text(strip=True)
            return title_text if title_text != 'Join us and Go Real-time' else ""
        return ""
    
    def _extract_content(self, article):
        #content = article.find("div", class_="summary-item")
        content_tag = article.find("div", class_="headline-content") if article else None

        if content_tag:
            # replace br with newlines
            for br in content_tag.find_all("br"):
                br.replace_with("**break**")

            # replace li with newlines
            for li in content_tag.find_all("li"):
                li.replace_with("**break** -  " +li.get_text(strip=True))

            return content_tag.get_text(strip=True)
        return ""
    
    def  _extract_source(self, article):
        source_tag = article.find("span", class_="news-source")
        return source_tag.get_text(strip=True) if source_tag else ""
    
    def _extract_category(self, article):
        categories = article.find_all("span", class_="news-label")

        return [c.get_text(strip=True) for c in categories] if categories else []
    
    def _extract_timestamp(self, article):
        time_tag = article.find("p", class_="time")
        if time_tag:
            time_str = time_tag.get_text(strip=True)
            return time_str
        
        return int(time.time())
    
    def _extract_link(self, article):
        link_tag = article.find("a", class_="news-link")
        return link_tag["href"] if link_tag and "href" in link_tag.attrs else ""

    def _is_critical(self, article):
        critical_tag = article.find("div", class_="active-critical")
        return critical_tag is not None
    
    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None