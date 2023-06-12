from PyQt6.QtWidgets import QTabWidget

class TabWidgetManager(QTabWidget):
    def __init__(self, parent=None):
        super(TabWidgetManager, self).__init__(parent)
        self._tabs_count = None

    @property
    def tabs_count(self):
        if self._tabs_count is None:
            self._tabs_count = self.count()
        return self._tabs_count

    def previous(self):
        current = self.currentIndex()
        if current == 0:
            print(f'You are at index {current}, There is no previous')
            return
        else:
            self.setCurrentIndex(current - 1)

    def next(self):

        current = self.currentIndex()
        print(self.tabs_count)
        print(current)
        print('***')
        if current == self.tabs_count - 1:
            print(f'You are at the  {current} index. There is no next')
            return
        else:
            self.setCurrentIndex(current + 1)

