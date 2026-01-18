## Classes and Instances
Class is a blueprint, instance is a real object in memory.   
```python
class Employee:
    def __init__(self, first, last, pay):
        # Instance variables (Each instance has a copy of these)
        self.first = first
        self.last = last
        self.pay = pay
        self.email = f'{first}.{last}@company.com'

    def fullname(self):
        return f'{self.first} {self.last}'
```
We can create objects and initialise variables instead of manual updation.    

* *__self__* keyword is used to refer to the object at hand, so *__ __init__ __* updates the attributes of our object at hand.   
* For methods *__self__* must be passed by default if not a static method.   
* When we call the function using the .fullname() it thinks self is also passed along with other params if any.
```python
emp1 = Employee('Adam', 'Sandler', 10000)
emp2 = Employee('John', 'Boyle', 20000) 

print(emp1.fullname())
print(emp2.fullname())
```

### Class variables vs Instance variables
```python
class Employee:
    def __init__(self, first, last, pay):
        # Instance variables (Each instance has a copy of these)
        self.first = first
        self.last = last
        self.pay = pay
        self.email = f'{first}.{last}@company.com'
    
    def apply_raise(self):
        # 4% raise
        self.pay = int(self.pay*1.04)
```
Instead of having this 4% hardcoded within a function which is a common variable to all the employees, we can make it a class variable
```python
class Employee:

    raise_amount = 1.04
    
    def __init__(self, first, last, pay):
        # Instance variables (Each instance has a copy of these)
        self.first = first
        self.last = last
        self.pay = pay
        self.email = f'{first}.{last}@company.com'
    
    def apply_raise(self):
        # 4% raise
        self.pay = int(self.pay* Employee.raise_amount)
```
We can also use self.raise_amount inplace of Employee.   
Order of checking will be first at instance level, then will check for class level variables. 
```python
emp1 = Employee('Adam', 'Sandler', 10000)
emp2 = Employee('John', 'Boyle', 20000) 

print(emp1.pay)
print(emp2.pay)
emp1.apply_raise()
emp2.apply_raise()

print(Employee.raise_amount)
```
* We can use class. or self. based on our needs. 
* If we want to keep track of number of employees, we want it to be the same for any instance.  
* So, we can then use a class level variable like number_of_employess, which can be updated whenever a new instance is created.

### Methods
1. Class Methods:  
<details>
Class methods take in cls as a parameter, they are used to update classlevel variables.  
    
```python
class Employee:

    raise_amount = 1.04
    
    def __init__(self, first, last, pay):
        # Instance variables (Each instance has a copy of these)
        self.first = first
        self.last = last
        self.pay = pay
        self.email = f'{first}.{last}@company.com'

    def fullname(self):
        return f'{self.first} {self.last}'
    
    def apply_raise(self):
        self.pay = int(self.pay* Employee.raise_amount)
        
    @classmethod
    def set_raise_amnt(cls, amount):
        cls.raise_amount = amount
```
```python
print(emp1.raise_amount) #1.04
print(Employee.raise_amount) #1.04

Employee.set_raise_amnt(1.05)

print(emp1.raise_amount) #1.05
print(Employee.raise_amount) #1.05
```

* Usecase for class methods is an **alternative constructor**.   
* cls() is in turn calling the init function of the class and that in turn constructs the object and returns the object. 
```python
class Employee:
    def __init__(self, first, last, pay):
        # Instance variables (Each instance has a copy of these)
        self.first = first
        self.last = last
        self.pay = pay
        self.email = f'{first}.{last}@company.com'
    
    @classmethod
    def from_string(cls, emp_str):
        first, last, pay = emp_str.split("-")
        return cls(first, last, pay)

new_emp1 = Employee.from_string("Adam-Sandler-100000")
```
</details>

2. Static methods
<details>
Static methods dont take in cls or self as a parameter, they are used as they have some logical connection to a class. Not specifically linked to any instace or class variables.  
    
```python
class Employee:

    raise_amount = 1.04
    
    def __init__(self, first, last, pay):
        # Instance variables (Each instance has a copy of these)
        self.first = first
        self.last = last
        self.pay = pay
        self.email = f'{first}.{last}@company.com'

    def fullname(self):
        return f'{self.first} {self.last}'
    
    def apply_raise(self):
        self.pay = int(self.pay* Employee.raise_amount)
        
    @classmethod
    def set_raise_amnt(cls, amount):
        cls.raise_amount = amount

    @staticmethod
    def is_workday(day):
        # Saturday or sunday, then False.
        return False if day.weekday()==5 or day.weekday()==6 else True
```
```python
import datetime
today = datetime.date(2025, 7, 10)

print(Employee.is_workday(today))
```
</details>

### Inheritence
Python follows a method resolution order. Starts with the child class and keeps going up.  
```python
class Developer(Employee):
    pass

dev1 = Developer("Adam", "Sandler", 10000)
print(dev1.email) # Works Fine
```
We can look at the inherintance here in real time using help method.
```python
print(help(Developer))
"""
Help on class Developer in module __main__:

class Developer(Employee)
 |  Developer(first, last, pay)
 |
 |  Method resolution order:
 |      Developer
 |      Employee
 |      builtins.object
 |
 |  Methods inherited from Employee:
 |
 |  __init__(self, first, last, pay)
 |      Initialize self.  See help(type(self)) for accurate signature.
 |
 |  apply_raise(self)
 |
 |  fullname(self)
 |
 |  ----------------------------------------------------------------------
 |  Class methods inherited from Employee:
 |
 |  set_raise_amnt(amount)
 |
 |  ----------------------------------------------------------------------
 |  Static methods inherited from Employee:
 |
 |  is_workday(day)
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors inherited from Employee:
 |
 |  __dict__
 |      dictionary for instance variables
 |
 |  __weakref__
 |      list of weak references to the object
 |
 |  ----------------------------------------------------------------------
 |  Data and other attributes inherited from Employee:
 |
 |  raise_amount = 1.05
"""
```
Subclasses can be updated without tampering the parent class. Only those not found here are searched upward.  
* We can use constructors of the parent in the child even if we need a different parameter set.
```python
class Developer(Employee):
    raise_amount = 1.10

    def __init__(self, first, last, pay, prog_lang):
        super().__init__(first, last, pay) 
        # also can use: Employee.__init__(self, first, last, pay)
        self.prog_lang = prog_lang
```

```python
class Developer(Employee):
    def __init__(self, first, last, pay, prog_lang):
        super().__init__(first, last, pay)
        self.prog_lang = prog_lang

class Manager(Employee):
    def __init__(self, first, last, pay, employees=None):
        super().__init__(first, last, pay)
        if employees==None:
            self.employees = []
        else:
            self.employees = employees
    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)
    def remove_emp(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)
    def print_emps(self) -> None:
        for emp in self.employees:
            print(f"-->{emp.fullname()}")


dev1 = Developer("A", "B", 10, "python")
dev2 = Developer("C", "D", 20, "C++")

mgr1 = Manager("E", "F", 90, [dev1])
print(dev1.fullname())
mgr1.print_emps()
mgr1.add_emp(dev2)
mgr1.print_emps()
mgr1.remove_emp(dev1)
mgr1.print_emps()
```

Also we can check inheritence using *__isinstance__* and *__issubclass__*
```python
print(isinstance(dev1, Employee)) #True
print(issubclass(Developer, Employee)) #True
print(issubclass(Developer, Manager)) # False
```

### Special Methods (dunder)
```python
class Employee:

    raise_amount = 1.04
    
    def __init__(self, first, last, pay):
        # Instance variables (Each instance has a copy of these)
        self.first = first
        self.last = last
        self.pay = pay
        self.email = f'{first}.{last}@company.com'

    def fullname(self):
        return f'{self.first} {self.last}'
    
    def apply_raise(self):
        self.pay = int(self.pay* Employee.raise_amount)
        
    @classmethod
    def set_raise_amnt(cls, amount):
        cls.raise_amount = amount

    @staticmethod
    def is_workday(day):
        # Saturday or sunday, then False.
        return False if day.weekday()==5 or day.weekday()==6 else True
    
    def __repr__(self):
        # Something that can help us recreate the object or other developers to use
        return f"Employee({self.first}, {self.last}, {self.pay})"
    
    def __str__(self):
        # Suitable print for our end user
        return f"{self.fullname()} - {self.email}"

emp1 = Employee("A", "B", 1000)
print(repr(emp1))
print(str(emp1))
print(emp1.__str__()) # Also works
```
* We can overwrite our own mathematical operator functionalities.  
* A few examples are add, mult, sub, mod, or, xor etc.   
* Every such function would have a signature like (self, other) in general. 
* len() function is also an example
```python
print(int.__add__(1, 2)) # Addition
print(str.__add__("a", "b")) # Concatenation
print("string".__len__()) # Returns 6, same as len(s)

class Employee:
    def __init__(self, first, last, pay):
        # Instance variables (Each instance has a copy of these)
        self.first = first
        self.last = last
        self.pay = pay
        self.email = f'{first}.{last}@company.com'

    def fullname(self):
        return f'{self.first} {self.last}'
    
    def __add__(self, other):
        if isinstance(other, Employee):
            return self.pay + other.pay
        return NotImplemented 

print(emp1 + emp2) # Will give an error without __add__ defind.
```

## Super funtion
It returns a temporary object during runtime. And is used to use the methods of the parent class.  
Can also be used to partly construct children objects.
```python
class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)

    def area(self):
        return self.length*self.width

class Cube(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)  
        self.height = side
    
    def volume(self):
        return self.height * self.width * self.height
    
square = Square(3)
cube = Cube(4)

print(square.area())
print(cube.volume())
```


### Getters, setters, deleter functionalities:
Used to maintian data encapsulation, hiding internal data and uncontrolled modification or access. Switching from simple variables to calculated property with some checks if needed. 
```python
class Employee:

    def __init__(self, first, last):
        self.first = first
        self.last = last
        self.email = f"{first}.{last}@company.com"
    
    def fullname(self):
        return f"{self.first} {self.last}"
    
emp = Employee("John", "Adams")

# Let us change first name 
emp.first = "Jim"

emp.fullname() # Returns updated fullname 
emp.email # Still the old John
```
In this above definition, if we want email field to also be updated when first name was changed:  
* We dont want to define it as a function, as some code that depends on this might break.
* We can define a method and access it like a attribute using the *__property__* decorator.
```python
class Employee:

    def __init__(self, first, last):
        self.first = first
        self.last = last

    @property
    def email(self):
        return self.email = f"{first}.{last}@company.com"

    @property
    def fullname(self):
        return f"{self.first} {self.last}"

emp = Employee("John", "Adams")

# Let us change first name 
emp.first = "Jim"

emp.fullname # Returns updated fullname 
emp.email # Updated email. method is called like an attribute. 
```
If we want the ability to set full name directly, we can use a setter.
```python
class Employee:

    def __init__(self, first, last):
        self.first = first
        self.last = last

    @property
    def email(self):
        return self.email = f"{first}.{last}@company.com"

    @property
    def fullname(self):
        return f"{self.first} {self.last}"
    
    @fullname.setter
    def fullname(self, name):
        self.first, self.last = name.split(" ")

    @fullname.deleter
    def fullname(self):
        self.first = None
        self.last = None
emp = Employee("John", "Adams")

# This updates the first and last attirbutes of the class by invoking the setter.
emp.fullname = "Jim Adams"

# .deleter is invoked when we run del <>
del emp.fullname
``` 

