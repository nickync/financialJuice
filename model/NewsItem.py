from atom.api import Atom, Str, Int, Enum
class NewsItem(Atom):
    title = Str()
    content = Str()
    time = Int()  # Unix timestamp
    importance = Int()  # Scale of 1 to 5
    category = Enum("Equities", "Bonds", "Crypto", "Forex", "Indexes")
    source = Str()