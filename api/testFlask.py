import random

class testFlask:
    def __init__(self) -> None:
        self.switch1 = False
        self.handle = random.random()
        self.num = 0
        self.val = 0
        print("init")

    def open(self) -> None:
        self.switch1 = True
        print("open")

    def set(self, num, val) -> None:
        self.num = num
        self.val = val

    def read(self) -> dict:
        d = {'given':0, 'observed':0}

        if (self.switch1 == True) :
            d['given'] = self.val + random.random()

            self.val1 = self.val
            if self.num == 0: 
                self.val1 = self.val / 3
            elif self.num == 1:
                self.val1 = self.val / -1.004
            elif self.num == 2:
                self.val1 = self.val * 2.564
            elif self.num == 3:
                self.val1 = self.val / -2.294
            else:
                self.val1 = 0

            d['observed'] = self.val1 + random.random()

        return d

    def close(self) -> None:
        self.switch1 = False
        print("close")

if __name__ == '__main__':
    a = testFlask()
    print(a.handle)