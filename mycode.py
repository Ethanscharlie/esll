
def append(list, item):
    list.append(item)
def listget(list, index):
    return list[index]
    
def checkNumber(number):
    if number%3==0:
        return "fizz"
    elif number%5==0:
        return "buzz"
    elif number%5==0 and number%3==0:
        return "fizzbuzz"
    return str(number)
def doFizzbuzz(number):
    print(number)
    print(checkNumber)
    print("")
def main():
    doFizzbuzz(5)
    doFizzbuzz(3)
    doFizzbuzz(15)
    doFizzbuzz(2)
main()
