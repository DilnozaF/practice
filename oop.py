class Vehicle:
    color = "white"
    def __init__(self,name,max_speed, mileage):
        self.name = name
        self.max_speed = max_speed
        self.mileage = mileage
    def seating_capacity(self,capacity):
        return f"The seating capacity of a {self.name} is {capacity} passengers"
class Bus(Vehicle):
    pass
    # def seating_capacity(self,capacity=50):
    #      return super().seating_capacity(capacity)
class Car(Vehicle):
    pass
n=Car("Audi Q5",240,12)
i=Bus("School Volvo",180,12)
print(f"color: {i.color}")
# print(i.seating_capacity())
print(f"Vehicle Name: {i.name}")
print(f"Speed: {i.max_speed}")
print(f"Mileage: {i.mileage}")

print(f"color: {n.color}")
print(f"Vehicle Name: {n.name}")
print(f"Speed: {n.max_speed}")
print(f"Mileage: {n.mileage}")


class Vehicle:
    def __init__(self, name, mileage, capacity):
        self.name = name
        self.mileage = mileage
        self.capacity = capacity

    def fare(self):
        return self.capacity * 100

class Bus(Vehicle):
    def fare(self):
        total=self.capacity*100
        return total+0.1*total

School_bus = Bus("School Volvo", 12, 50)
print("Total Bus fare is:", School_bus.fare())


class Vehicle:
    def __init__(self, name, mileage, capacity):
        self.name = name
        self.mileage = mileage
        self.capacity = capacity

class Bus(Vehicle):
    pass

School_bus = Bus("School Volvo", 12, 50)
print(type(School_bus))
print(isinstance(School_bus, Vehicle))