# Ethan's Silly Little Language

## Basic Syntax
### Hello World
```
" Runs at the start of the program "
Void start()
    print("Hello World")
end

" Runs every frame "
Void draw()

end
```

### Variables
```
Decimal myDec 100.0
Integer myInt 3
Boolean myBool false
String myStr "Hello World"

" Increment by one "
myInt myInt + 1 

" Reassign String "
myStr "New String"
```

### Loop
```
Integer i 0
while i < 10
    print("Looped")
    i i + 1
end
```

### Functions
```
Decimal getFunnyNumber(String text)
    if text = "first"
        return 0.0
    elif text = "second"
        return 1.0
    end
end
```

### Ifs
```
if num < 100
    print("A")
elif num > -100
    print("B")
else
    print("C")
end

if num = 5 
    print("It's Five")
end

if num > 0 and num < 5
    print("It's between 0 and 5")
end
```

