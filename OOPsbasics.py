    
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

# 25/06/2026

# Q1 Create Teacher and Researcher, inherit in Professor.
# class Teacher:
#     def teach (self):
#         print("Teaching student")
# class Research:
#     def research(self):
#         print("Doing Research")
# class Professor(Teacher, Research):
#     def guide(self):
#         print("Guiding students")
# p = Professor()
# p.teach()
# p.research()
# p.guide()


# Q2 Create Fly and Swim, inherit in Duck.
# class Fly:
#     def fly(self):
#         print("Duck can fly")
# class Swim:
#     def swim(self):
#         print("Duck can swim")
# class Duck(Fly, Swim):
#     def sound(self):
#         print("Quack Quack")
# d = Duck()
# d.fly()
# d.swim()
# d.sound()


# # Q3 Create classes GrandFather, Father, and Son to demonstrate Multilevel Inheritance.
# class GrandFather:
#     def House(self):
#         print("Grandfather has a house")
# class Father(GrandFather):
#     def Car(self):
#         print("Father has a Car")
# class Son(Father):
#     def Bike(self):
#         print("Son has a bike")
# s = Son()
# s.House()
# s.Car()
# s.Bike()

# 26/06/2026

# # Q1. Animal → Mammal → Dog (Multilevel Inheritance)
# class Animal:
#     def eat(self):
#         print("Animal eats food")
# class Mammal(Animal):
#     def walk(self):
#         print("Mammal walks on land")
# class Dog(Mammal):
#     def bark(self):
#         print("Dog barks")

# d = Dog()
# d.eat()
# d.walk()
# d.bark()

# # Q2. Person → Employee → Manager (Multilevel Inheritance)
# class Person:
#     def details(self):
#         print("Person has name and age")
# class Employee(Person):
#     def salary(self):
#         print("Employee gets salary")
# class Manager(Employee):
#     def department(self):
#         print("Manager handles a department")
# m = Manager()
# m.details()
# m.salary()
# m.department()

# # Q. Shape → Circle, Rectangle (Hierarchical Inheritance)

# class Shape:
#     def show(self):
#         print("This is Shape")
# class Circle(Shape):
#     def circle(self):
#         print("This is Circle")
# class Rectangle(Shape):
#     def rectangle(self):
#         print("This is Rectangle")
# c = Circle()
# c.show()
# c.circle()
# r = Rectangle()
# r.show()
# r.rectangle()


# # Q. Employee → Developer, Designer (Hierarchical Inheritance)
# class Employee:
#     def work(self):
#         print("Employee works in the company")
# class Developer(Employee):
#     def code(self):
#         print("Developer writes code")
# class Designer(Employee):
#     def design(self):
#         print("Designer creates designs")
# d = Developer()
# d.work()
# d.code()
# de = Designer()
# de.design()

# # Q) Person→ Employee → Manager + Developer (Hybrid Inheritance)
# class Person:
#     def person(self):
#         print("I am a Person")
# class Employee(Person):
#     def employee(self):
#         print("I am an Employee")
# class Manager(Employee):
#     def manager(self):
#         print("I am a Manager")
# class Developer(Employee):
#     def developer(self):
#         print("I am a Developer")
# class TechManager(Manager, Developer):
#     def techmanager(self):
#         print("I am a Tech Manager")
# t = TechManager()
# t.person()
# t.employee()
# t.manager()
# t.developer()
# t.techmanager()

# # Q. Vehicle → Car + ElectricCar → HybridCar (Hybrid Inheritance)
# class Vehicle:
#     def vehicle(self):
#         print("This is a Vehicle")
# class Car(Vehicle):
#     def car(self):
#         print("This is a Car")
# class ElectricCar(Vehicle):
#     def electric(self):
#         print("This is an Electric Car")
# class HybridCar(Car, ElectricCar):
#     def hybrid(self):
#         print("This is a Hybrid Car")
# h = HybridCar()
# h.vehicle()
# h.car()
# h.electric()
# h.hybrid()



# from abc import ABC, abstractmethod
# class RungtaSystem(ABC):
#     @abstractmethod
#     def security(self):
#         pass
# class MobileApp(RungtaSystem):
#     def security(self):
#         print("Good")
#     def mobile_login(self):
#         print("Login into mobile")
# mobile = MobileApp()
# mobile.security()
# mobile.mobile_login()



# from abc import ABC, abstractmethod
# class Vehicle(ABC):
#     @abstractmethod
#     def start(self):
#         pass
#     @abstractmethod
#     def stop(self):
#         pass
# class Car(Vehicle):
#     def start(self):
#         print("Car Started")
#     def stop(self):
#         print("Car Stopped")
# car = Car()
# car.start()
# car.stop()



# from abc import ABC, abstractmethod
# class Teacher(ABC):
#     @abstractmethod
#     def teach(self):
#         pass
# class Researcher(ABC):
#     @abstractmethod
#     def research(self):
#         pass
# class Professor(Teacher, Researcher):
#     def teach(self):
#         print("Teaching Students")
#     def research(self):
#         print("Doing Research")
#     def work(self):
#         print("Doing Research Work")
# p = Professor()
# p.teach()
# p.research()
# p.work()


# from abc import ABC, abstractmethod
# class BankSystem(ABC):
#     @abstractmethod
#     def login(self):
#         pass
#     @abstractmethod
#     def transaction(self):
#         pass
#     @abstractmethod
#     def logout(self):
#         pass
# class SBI(BankSystem):
#     def login(self):
#         print("Login Successful")
#     def transaction(self):
#         print("Transaction Completed")
#     def logout(self):
#         print("Logout Successful")
# user = SBI()
# user.login()
# user.transaction()
# user.logout()