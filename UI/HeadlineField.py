from enaml.widgets.api import MultilineField

class HeadlineField(MultilineField):
    def __init__(self, read_only=False, auto_sync_text=True, hug_width='ignore', hug_height='ignore'):
        super().__init__(read_only=read_only, auto_sync_text=auto_sync_text, hug_width=hug_width, hug_height=hug_height)
        self.read_only = read_only
        self.auto_sync_text = auto_sync_text



    