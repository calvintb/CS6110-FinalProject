from Intersection import Intersection

class Source(Intersection):
    def __init__(self, label=None):
        super().__init__(label)
        self.is_source = True


    def __str__(self):
        return f"Source({self.label})"