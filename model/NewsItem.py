from atom.api import Atom, Str, List, Bool
class NewsItem(Atom):
    title = Str()
    content = Str()
    time = Str()  # Unix timestampamp 
    category = List()
    source = Str()
    link = Str()
    critical = Bool(default=False)

    def to_text(self):
        """Convert the news item to a formatted text string."""

        parts = []
        if self.content:
            if '**break**' in self.content:
                for part in self.content.split("**break**"):
                    parts.append(f"{part}")
            else:
                parts.append(f"{self.content}")

        return "\n".join([p for p in parts if p.strip()])     