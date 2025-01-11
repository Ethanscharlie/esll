
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
    _ = print(number)
    _ = print(checkNumber)
    _ = print("")
def main():
    _ = doFizzbuzz(5)
    _ = doFizzbuzz(3)
    _ = doFizzbuzz(15)
    _ = doFizzbuzz(2)
main()
