class Andy:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print("hi", self.name)

    def __str__(self):
        return f"Andy = {self.name}"

andy = Andy("xxx")
print(andy.name)
andy.say_hello()
print(andy)