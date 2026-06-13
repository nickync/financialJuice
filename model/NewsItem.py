from atom.api import Atom, Str
class NewsItem(Atom):
    title = Str()
    content = Str()
    time = Str()  # Unix timestampamp 
    category = Str()
    source = Str()
    link = Str()

    def to_text(self):
        """Convert the news item to a formatted text string."""
        #if self.title and self.content:
        #return f"Title: {self.title}\nContent: {self.content} - {self.time}\n{self.source} ** {self.category} **\n{self.link}"
        #return f"Title: {self.title}\n - {self.time}\n{self.source} ** {self.category} **\n{self.link}"
        parts = []
        # if self.title:
        #     parts.append(f"{self.title}")
        if self.content:
            #print(self.content)
            if '**break**' in self.content:
                for part in self.content.split("**break**"):
                    parts.append(f"{part}")
            else:
                parts.append(f"{self.content}")

        #tsc = f"{self.time} - {self.source} ** {self.category} **\n{self.link}"
        #parts.append(tsc)

        return "\n".join([p for p in parts if p.strip()])     