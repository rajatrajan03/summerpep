# a = "Rakesh"
# for i in range(0,6):
#     print(a[i],"", end="")
    
# for i in range(0,5):
#     for j in range(0,i+1):
#         print("*", end="")
#     print()

# for i in range(1,6):
#     for j in range(0,i+1):
#         print(j, end="")
#     print()

# for i in range(1,6):
#     for j in range(1,i+1):
#         print(i, end="")
#     print()
    
    
# for i in range(0,5):
#     for j in range(0,i+1):
#         print(j+1, end="")
#     print()
    
# for i in range(0,5):
#     for j in range(0,i+1):
#         print(i+1, end="")
#     print()

# for i in range(0,5):
#     for j in range(0,5-i):
#         print("j", end="")
#     print()

# a = "Rakesh"
# b = "Rahul"
# for i in range(0,6):
#     print (a[i])
#     for j in range(0,5):
#         print(b[j])

# # wrong code range never goes backwards in python, so the below code will not work
# for i in range(7,1):
#     for j in range(1,7-i):
#         print(i, end="")
#     print()


# for i in range(7,1,-1):
#     for j in range(1,7-i):
#         print(i, end="")
#     print()
    
# for i in range(5, 0, -1):
#     for j in range(i):
#         print("*", end="")
#     print()
    
# for i in range(5):
#     for j in range(i):
#         print(" ", end="")
#     for j in range(5 - i):
#         print("*", end="")
#     print()

# for i in range(5, 0, -1):
#     print(" " * (5 - i), end="")
#     for j in range(1, i + 1):
#         print(j, end="")
#     print()
    
 
# for i in range(5, 0, -1):
#     for j in range(5 - i):
#         print(" ", end="")
#     for j in range(i):
#         print(i, end="")
#     print()

# # pyramid pattern
# n = 5
# for i in range(1, n + 1):
#     for j in range(n - i):
#         print(" ", end="")
#     for j in range(2 * i - 1):
#         print("*", end="")
#     print()
    
# # reverse pyramid pattern
# n= 5 
# for i in range(n, 0, -1):
#     for j in range(n - i):
#         print(" ", end="")
#     for j in range(2 * i - 1):
#         print("*", end="")
#     print()
    
# # diamond pattern  
# n = 5
# for i in range(1, n + 1):
#     for j in range(n - i):
#         print(" ", end="")
#     for j in range(2 * i - 1):
#         print("*", end="")
#     print()
# for i in range(n - 1, 0, -1):
#     for j in range(n - i):
#         print(" ", end="")
#     for j in range(2 * i - 1):
#         print("*", end="")
#     print()
    
# output
#    *
#    ***
#   *****
#  *******
# *********
#  *******
#   *****
#    ***
#     *


# x=5
# for i in range(1,6):
#     for k in range(1,x+1):
#         print(" ", end="")
#     for j in range(1,i+1):
#         print("*", end="")
#     print()
#     x=x-1
    
# output
#      *
#     **
#    ***
#   ****
#  *****

# x=5
# for i in range(5,0,-1):
#     for k in range(1,x+1):
#         print(" ", end="")
#     for j in range(1,i+1):
#         print("*", end="")
#     print()
#     x=x-1
    
# class - a class is a blueprint for creating objects. 
# It defines a set of attributes and methods that the created objects will have. 
# In Python, classes are defined using the `class` keyword, followed by the class name 
# and a colon. Inside the class, you can define attributes (variables) and 
# methods (functions) that belong to the class.

# class Car:
#     company = "BMW24"
#     year = 2026

# print(Car.company)
# print(Car.year)

# class Car:
#     company = "BMW24"
#     year = 2026

# c = Car()

# print(c.company)
# print(c.year)

# class Car:
#     def __init__(self):
#         self.company = "BMW24"
#         self.year = 2026

#     def display(self):
#         print("Company:", self.company)
#         print("Year:", self.year)

# c = Car()
# c.display()

# class Car:
#     def __init__(self, make, model, year):
#         self.make = make
#         self.model = model
#         self.year = year



# # Q1) Create a Student class with name, roll_no, marks and display details.
# class student:
#     def __init__(self, name, roll_no, marks):
#         self.name = name
#         self.roll_no = roll_no
#         self.marks = marks
#     def increase_marks(self, increase):
#         self.marks = self.marks + increase
#         return self.marks
#     def decrease_marks(self, decrease):
#         self.marks = self.marks - decrease
#         return self.marks
#     def display_info(self):
#         return f"{self.name}, {self.roll_no}, {self.marks}"
# stud = student("Rahul", 35, 90)
# print(stud.increase_marks(10))
# print(stud.decrease_marks(10))
# print(stud.display_info())

# # Q.2) Create a BankAccount class with deposit and withdrwal methods.
# class BankAccount:
#     def __init__(self,name,balance):
#         self.name = name
#         self.balance = balance

#     def deposit(self, amount):
#         self.balance += amount
#         return self.balance

#     def withdraw(self, amount):
#         self.balance -= amount
#         return self.balance
# acc = BankAccount("Alice", 1000)
# print("After deposit:", acc.deposit(500))
# print("After withdrawal:", acc.withdraw(200))

# q.3)Calculate salary of an employee after bonus
# class Employee:
#     def __init__(self, salary):
#         self.salary = salary
#     def bonus(self, bonus):
#         self.salary += bonus
#         return self.salary
# emp = Employee(50000)
# print("After bonus:", emp.bonus(5000))