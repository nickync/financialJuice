from atom.api import Str, Bool
from enaml.widgets.api import RawWidget
from enaml.core.declarative import d_

# Import the appropriate Qt binding
try:
    from enaml.qt.QtCore import Qt
    from enaml.qt.QtWidgets import QLabel
except ImportError:
    from PyQt6.QtCore import Qt
    from PyQt6.QtWidgets import QLabel


class WrappingLabel(RawWidget):
    """
    A read-only label that supports automatic text wrapping.
    
    Usage in .enaml:
        WrappingLabel:
            text = "Long text that will wrap to fit the available width"
            word_wrap = True
            maximum_width = 300
    """
    
    __slots__ = ('__weakref__',)

    # Public attributes
    text = d_(Str())
    word_wrap = d_(Bool(True))
    
    def create_widget(self, parent):
        """Create the toolkit widget for the control.
        
        This method is called by Enaml's proxy system when the widget
        needs to be created [citation:1][citation:2].
        
        Parameters
        ----------
        parent : toolkit widget or None
            The parent toolkit widget for the control.
        
        Returns
        -------
        result : toolkit widget
            The toolkit specific widget for the control.
        """
        label = QLabel(parent)
        label.setWordWrap(self.word_wrap)  # Enable text wrapping [citation:3]
        label.setText(self.text)
        label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        return label
    
    def _update_text(self, change):
        """Sync text changes to the underlying Qt widget."""
        widget = self.get_widget()
        if widget:
            widget.setText(change['value'])
    
    def _update_word_wrap(self, change):
        """Sync word_wrap changes to the underlying Qt widget."""
        widget = self.get_widget()
        if widget:
            widget.setWordWrap(change['value'])
    
    def _observe_text(self, change):
        """Atom observer for text attribute."""
        self._update_text(change)
    
    def _observe_word_wrap(self, change):
        """Atom observer for word_wrap attribute."""
        self._update_word_wrap(change)