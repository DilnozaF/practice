import math
class Circle:
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return math.pi * self.radius ** 2
    def perimeter(self):
        return 2 * math.pi * self.radius


import datetime
class Person:
    def __init__(self, name, country, dob):
        self.name = name
        self.country = country
        self.dob = dob
    def age(self):
        today=datetime.date.today()
        age = today.year - self.dob.year
        if (today.month, today.day)<(self.dob.month, self.dob.day):
            age-=1
        return age


class calculator:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def addition(self):
        return self.a + self.b
    def subtraction(self):
        return self.a - self.b
    def multiplication(self):
        return self.a * self.b
    def division(self):
        if self.b!=0:
             return self.a / self.b
        else:
            print("cannot divide by zero")


class shape:
    def calculateArea(self):
        pass
    def calculatePerimeter(self):
        pass
class circle(shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return math.pi * self.radius ** 2
    def perimeter(self):
        return 2 * math.pi * self.radius
class triangle(shape):
    def __init__(self, a, b, c,h,base):
        self.a = a
        self.b = b
        self.c = c
        self.h = h
        self.base = base
    def area(self):
        return self.h*self.base/2
    def perimeter(self):
        return self.a+self.b+self.c
class square(shape):
    def __init__(self, a):
        self.a = a
    def area(self):
        return self.a*self.a
    def perimeter(self):
        return 4*self.a


def binarySearch( arr, low, high,x):
        mid = (low+high)//2
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            return binarySearch(arr, low, mid-1, x)
        else:
            return binarySearch(arr, mid+1, high, x)
arr = [ 2, 3, 4, 10, 40 ]
x = 10
result = binarySearch(arr, 0, len(arr)-1, x)

if result != -1:
    print("Element is present at index", str(result))
else:
    print("Element is not present in array")

class Node:
    def __init__(self, data):
        self.data = data
        self.right = None
        self.next = None
class BinarySearchTree:
    def __init__(self):
        self.root = None
    def insert(self, data):
        if self.root == None:
            self.root = Node(data)
        else:
            self.insert_recursive(self.root, data)
    def insert_recursive(self, node, data):
        if data < node.data:
            if node.left is None:
                node.left = Node(data)
            else:
                self.insert(node.left, data)
        else:
            if node.right is None:
                node.right = Node(data)
            else:
                self.insert_recursive(node.right, data)
    def search(self, data):
        return self.search_recursively(self.root, data)
    def search_recursive(self, node, data):
        if node is None or node.data == data:
            return node
        if data < node.data:
            return self.search_recursive(node.left, data)
        else:
            return self.search_recursive(node.right, data)
