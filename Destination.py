from Intersection import Intersection

class Destination(Intersection):
    def __init__(self, label=None):
        super().__init__(label)


    def __str__(self):
        return f"Destination({self.label})"
