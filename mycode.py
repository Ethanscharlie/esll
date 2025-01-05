
def append(list, item):
    list.append(item)
def listget(list, index):
    return list[index]
    
def main():
    myList = []
    myList = range(111)
    i = 0
    while (i<len(myList)):
        print(listget(myList, i))
        i = i+1
main()
