from atom.api import Atom, Str, Int, Enum
class NewsItem(Atom):
    title = Str()
    content = Str()
    time = Str()  # Unix timestampamp 
    category = Str()
    source = Str()
    link = Str()


    def to_text(self):
        """Convert the news item to a formatted text string."""
        if self.title and self.content:
            return f"{self.title}\n{self.content} - {self.time}\n{self.source} ** {self.category} **\n{self.link}"
        return f"{self.title} - {self.time}\n{self.source} ** {self.category} **\n{self.link}"
