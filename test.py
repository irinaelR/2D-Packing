from objet.rectangle import Rectangle

r1 = Rectangle(1, 150, 150)
r1.x = 0
r1.y = 0

r2 = Rectangle(2, 50, 50)
r2.x = 0
r2.y = 0

list = [r1]

print(r2.intersection_in_list(list))