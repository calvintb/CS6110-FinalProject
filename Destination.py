from Intersection import Intersection

class Destination(Intersection):
    def __init__(self, label=None):
        super().__init__(label)
        self.is_destination = True


    def __str__(self):
        return f"Destination({self.label})"
