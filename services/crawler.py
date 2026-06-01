import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List
from model.NewsItem import NewsItem

class Crawler:
    def __init__(self, url: str = "https://financialjuice.com"):
        self.base_url = url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def fetch_news(self) -> List[NewsItem]:
        try:
            response = self.session.get(self.base_url, timeout=10)
            response.raise_for_status()
            return self.parse_news(response.text)
        except requests.RequestException as e:
            print(f"Error fetching news: {e}")
            return []
        
    def parse_news(self, html: str) -> List[NewsItem]:
        soup = BeautifulSoup(html, 'html.parser')
        news_items = []
        
        articles = soup.select('div.news-item')
        for article in articles[:20]:
            try:
                title = self.extract_title(article)
                content = self.extract_content(article)
                time = self.extract_time(article)
                importance = self.extract_importance(article)
                category = self.extract_category(article)
                source = self.extract_source(article)
                news_item = NewsItem(title=title, content=content, time=time, importance=importance, category=category, source=source)
                news_items.append(news_item)
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue
        return news_items
    
    def _extract_title(self, article) -> str:
        title_elem = article.select_one('h1, h2, h3, .title, .headline')
        return title_elem.text.strip() if title_elem else ""
    
    def _extract_content(self, article) -> str:
        content_elem = article.select_one('p, .content, .description, .summary')
        return content_elem.text.strip()[:200] if content_elem else ""
    
    def _extract_time(self, article) -> int:
        time_elem = article.select_one('time, .date, .timestamp')
        if time_elem and time_elem.has_attr('datetime'):
            dt = datetime.fromisoformat(time_elem['datetime'])
            return int(dt.timestamp())
        elif time_elem:
            try:
                dt = datetime.strptime(time_elem.text.strip(), "%Y-%m-%d %H:%M:%S")
                return int(dt.timestamp())
            except ValueError:
                pass
        return int(datetime.now().timestamp())
    
    def _extract_importance(self, article) -> int:
        importance_elem = article.select_one('.importance, .priority')
        if importance_elem:
            try:
                return int(importance_elem.text.strip())
            except ValueError:
                pass
        return 3
    
    def _extract_category(self, article) -> str:
        category_elem = article.select_one('.category, .tag')
        return category_elem.text.strip() if category_elem else "General"
    
    def _extract_source(self, article) -> str:
        source_elem = article.select_one('.source, .author')
        return source_elem.text.strip() if source_elem else "Unknown"

