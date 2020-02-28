class student(object):
    def __init__(self):
        self.score = 0

    # @property
    # def score(self):
    #     return self.__score


    # @score.setter
    # def setScore(self, s):
    #     if 0 <= s <= 100:
    #         self.__score = s
    def hello(self):
        print("hello")

    def __getattr__(self, name):
        print("In __getattr__: " + name)
        if name == "score":
            return self.score

    def __setattr__(self, name, value):
        print("In __setattr__: " + name)
        if name == "score":
            self.__dict__[name] = value
            
class xiaoming(student):
    def __init__(self):
        

if __name__ == "__main__":
    shit = student()
    shit.score = 20
    print(shit.score)
    shit.hello()

    # print(shit.score)

    # shit.setScore = 20

    # print(shit.score)


        