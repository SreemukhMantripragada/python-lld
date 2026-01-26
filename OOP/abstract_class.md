## Abstract classes

In python, we use abc library to create abstract classes or methods.   
These are meant to be sub-classed and the children define the functionalities, we just give the blue print.  
These are used in common interview settings to implement *Interfaces* acting as blueprints for relevant classes to ensure consistent implementation and preventing direct instantiation of the parent.  

*TypeError* will be raised for those that don't implement all abstract methods of parent.   
```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod # Child must implement this for sure.
    def start_engine(self): ...

    def honk(self): # Concrete method, can be implemented, overridden or inherited
        print("Beep, Beep")

class Car(Vehicle):
    def start_engine(self):
        print("Car started")
class Motorcycle(Vehicle):
    def start_engine(self):
        print("Motorcycle started")
```
Use in interviews:
1. Abstraction: We are effectively hiding implementation details and only exposing essential features like a Vehicle interface
2. Polymorphism: We can consider every child to be a Vehicle, so we can consider all of them alike with respect to the common functionalities. 
Examples: PaymentProcesser, Shape, Logger etc. 