# SOLID Principles
### Single Responsibility
Single Responsibility Principle (SRP) states a class should have only one reason to change, meaning it handles just one job or responsibility.

Before (violates SRP - mixes data and persistence):
```python
class Person:
    def __init__(self, name):
        self.name = name
    def save(self):
        print(f'Save {self.name} to database')
```
After (split responsibilities):
```python
class Person:
    def __init__(self, name): self.name = name
class PersonDB:
    def save(self, person): print(f'Save {person.name} to database')
```
### Open/Closed
Open/Closed Principle (OCP) states classes should be open for extension but closed for modification.
​
Before (violates OCP - modify for new shapes):
```python
class Shape:
    def __init__(self, type_, **kwargs):
        self.type_ = type_
        if self.type_ == "circle": self.radius = kwargs["radius"]
        elif self.type_ == "rectangle": self.width, self.height = kwargs["width"], kwargs["height"]
    def area(self):
        if self.type_ == "circle": return 3.14 * self.radius**2
        elif self.type_ == "rectangle": return self.width * self.height
```
After (extend via subclasses):
```python
from abc import ABC, abstractmethod
class Shape(ABC):
    @abstractmethod
    def area(self): pass
class Circle(Shape):
    def __init__(self, r): self.radius = r
    def area(self): return 3.14 * self.radius**2
class Rectangle(Shape):
    def __init__(self, w, h): self.width, self.height = w, h
    def area(self): return self.width * self.height
```
### Liskov Substitution
Liskov Substitution Principle (LSP) states that objects of a superclass should be replaceable with objects of a subclass without breaking the application.

Before (violates LSP - Square breaks Rectangle expectations):
```python
class Rectangle:
    def __init__(self, w, h): self.width, self.height = w, h
    def set_width(self, w): self.width = w
    def set_height(self, h): self.height = h
    def area(self): return self.width * self.height
class Square(Rectangle):
    def __init__(self, s): super().__init__(s, s)
    def set_width(self, w): self.width = self.height = w
    def set_height(self, h): self.width = self.height = h
```
After (siblings sharing abstract base):

```python
from abc import ABC, abstractmethod
class Shape(ABC):
    @abstractmethod
    def area(self): pass
class Rectangle(Shape):
    def __init__(self, w, h): self.width, self.height = w, h
    def area(self): return self.width * self.height
class Square(Shape):
    def __init__(self, s): self.side = s
    def area(self): return self.side**2
```
### Interface Segregation
Interface Segregation Principle (ISP) states that clients should not be forced to depend on interfaces they do not use.

Before (violates ISP - forces unused methods):
```python
from abc import ABC, abstractmethod
class Printer(ABC):
    @abstractmethod
    def print(self, doc): pass
    @abstractmethod
    def fax(self, doc): pass
    @abstractmethod
    def scan(self, doc): pass
class OldPrinter(Printer):
    def print(self, doc): print(f"Print {doc}")
    def fax(self, doc): raise NotImplementedError()
    def scan(self, doc): raise NotImplementedError()
```
After (small, specific interfaces):
```python
class Printer(ABC):
    @abstractmethod
    def print(self, doc): pass
class Faxer(ABC):
    @abstractmethod
    def fax(self, doc): pass
class Scanner(ABC):
    @abstractmethod
    def scan(self, doc): pass
class OldPrinter(Printer):
    def print(self, doc): print(f"Print {doc}")
class ModernPrinter(Printer, Faxer, Scanner):
    def print(self, doc): print(f"Color print {doc}")
    def fax(self, doc): print(f"Fax {doc}")
    def scan(self, doc): print(f"Scan {doc}")
```
### Dependency Inversion
Dependency Inversion Principle (DIP) states that high-level modules should not depend on low-level modules; both should depend on abstractions.  
​
Before (violates DIP - concrete dependency):
```python
class FrontEnd:
    def __init__(self): self.backend = BackEnd()
    def show(self): print(self.backend.get_data())
class BackEnd:
    def get_data(self): return "DB data"
```
After (abstract dependency):
```python
from abc import ABC, abstractmethod
class DataSource(ABC):
    @abstractmethod
    def get_data(self): pass
class DB(DataSource):
    def get_data(self): return "DB data"
class API(DataSource):
    def get_data(self): return "API data"
class FrontEnd:
    def __init__(self, source: DataSource):
        self.source = source
    def show(self): print(self.source.get_data())
```