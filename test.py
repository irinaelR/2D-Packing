from objet.rectangle import Rectangle

r1 = Rectangle(1, 150, 150)
r1.x = 0
r1.y = 0

r2 = Rectangle(2, 50, 80)
r2.x = 120
r2.y = 50

list = [r1]

print(r2.rotate())
