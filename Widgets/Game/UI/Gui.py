from Widgets.Base import Widget
class Gui(Widget):
    def __init__(self):
        super().__init__()
        self.uiElements = []
    def update(self,game):
        for e in self.uiElements:
            e.update(game)
    def render(self,game):
        for e in self.uiElements:
            e.render(game)