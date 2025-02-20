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

## Simple platforming engine example
```
" --------------- Constants --------------- "
Decimal SCREEN_WIDTH 800
Decimal SCREEN_HEIGHT 800
Decimal SPEED 10
Decimal GRAVITY 0.35
Decimal JUMP_POWER 70

" --------------- box variables --------------- "
Decimal boxX 100
Decimal boxY 100
Decimal boxW 100
Decimal boxH 100
Decimal boxVelocityY 0

Void start()

end

Void draw()
  setBackground(100, 200, 100)

  " --------------- Update Box Phyics --------------- "
  boxVelocityY boxVelocityY + GRAVITY * deltatime

  if pressingKey(">")
    boxX boxX + SPEED * deltatime
  end
  if pressingKey("<")
    boxX boxX - SPEED * deltatime
  end
  if pressingKey(" ")
    boxVelocityY -JUMP_POWER * deltatime
  end

  boxY boxY + boxVelocityY * deltatime

  if boxY + boxH > SCREEN_HEIGHT
    boxY SCREEN_HEIGHT - boxH
    boxVelocityY 0
  end

  " --------------- Draw Box --------------- "
  fill(255, 0, 0)
  drawRectangle(boxX, boxY, boxW, boxH)
end
```
