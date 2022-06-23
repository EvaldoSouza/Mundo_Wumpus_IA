from random import randrange


for i in range(200000):
    flag = randrange(5)
    if flag >= 5:
        print("falso")