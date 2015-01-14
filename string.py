class String:
    def __init__(self, data):
        self.__data = data.replace(" ", "")
    def get(self):
        return self.__data
    def equals(self, other):
        return self.__data == other.replace(" ", "")

if __name__ == '__main__':
    a = String("Example String")
    assert a.get() == "ExampleString"
    assert a.equals("Example String") == True
    assert a.equals("ExampleString") == True
    assert a.equals("Different String") == False
