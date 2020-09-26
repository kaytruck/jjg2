from pygame import Rect


class Floor:
    def __init__(self, x1, y1, x2, y2):
        self.__floor = Rect(x1, y1, x2, y2)

    def get_left(self):
        return self.__floor.left

    def set_left(self, left):
        self.__floor.left = left

    def get_right(self):
        return self.__floor.right

    def get_top(self):
        return self.__floor.top

    def get_bottom(self):
        return self.__floor.bottom

    def get_rect(self):
        return self.__floor

    left = property(get_left, set_left)
    right = property(get_right)
    top = property(get_top)
    bottom = property(get_bottom)
    rect = property(get_rect)
