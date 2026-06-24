    
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

# # Q.4)Create a class Animal and inherit it to create a Dog class.
# class Animal:
#     def eat(self):
#         print("Animal is eating.")
# class Dog(Animal):
#     def bark(self):
#         print("Dog is barking.")       
# d=Dog()
# d.eat()
# d.bark()

# # Q.5 Create a class Person and inherit it in students
# class Person:
#     def display(self):
#         print("This is a person.")
# class Student(Person):
#     def study(self):
#         print("This is a student.")
# s = Student()
# s.display()
# s.study()