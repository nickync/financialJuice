from atom.api import Atom, Str, Int, Enum
class NewsItem(Atom):
    title = Str()
    content = Str()
    time = Str()  # Unix timestampamp 
    category = Str()
    source = Str()
    link = Str()