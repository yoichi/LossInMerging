class String:
    def __init__(self, data):
        self.__data = data.replace(" ", "")
    def get(self):
        return self.__data

if __name__ == '__main__':
    a = String("Example String")
    assert a.get() == "ExampleString"
