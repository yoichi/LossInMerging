class String:
    def __init__(self, data):
        self.__data = data.replace(" ", "")
    def get(self):
        return self.__data
    def equals(self, other):
        return self.__data == other.replace(" ", "")
