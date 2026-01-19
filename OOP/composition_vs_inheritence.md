# Composition vs Inheritence
Both help us seperate responsibilities and let us reuse code, but we need to be careful when to use which.
### **Inheritence**  (IS A relationship)   
Break down classes into a hierarchical class-subclass setup.    
Example: Base class **Animal**, Derived class **Horse**     
This is an example of *__Liskov Substitution principle__*, which states that if child is a subtype of parent, replacing objects of parent with child should not change the programs behaviour.    
![alt text](https://files.realpython.com/media/ic-basic-inheritance.f8dc9ffee4d7.jpg)   

Inheritence is used every where in python, everything in Python is an object, class definitions and functions are objects too. All of them are inherited from thebase class named **object**.     
To accomodate a new type of class which is not exactly a natural child to a parent class, we will face an issue with just inheritence. So if we must force this to happen, we must update other children or the parent itself.  
### **Composition**(HAS A relationship)    
Uses separate classes to have different responsibilites that are linked in some meaningful way.   
In the UML we can show the cardinality of the relationship. Here we show 1 **Composite** class has one **Component** class contained within.   
![alt text](https://files.realpython.com/media/ic-basic-composition.8a15876f7db2.jpg)  
Different options for cardinality:
* *Number*: Showing the number of **Component** class instances that **Composite** contains.  
* **symbol*: Can contain any number of instances.  
* *Range*: We can show ranges with minimum and maximum number of instances like *1..4* or only minimum *1..**       

Example: Composite class **Horse**, componet class **Tail**, so now a **Dog** class can also contain a component class **Tail** thus increasing code reusability.     
* So with composition, we can use an abstract class that forms a contract and use those that we need and call them all alike, instead of a full parent class. 
* Composite will have different components that can share a common interface, keeping it from a need only basis.    
* We can have an **ImageHandler** class that has an object of a class implementing a **Image** interface, which is implemented as **JPGImage** or **PNGImage** etc.  


## Interview setting
#### Inheritence=One dimension, Composition=Multiple axes
In an LLD question, we always have many different roles, that need independent changes, we cannot start with a big generic class and keep inheriting and specialising in something.      
For example we can have many things come up, like   
    * Policies(Salary vs Hourly vs Commision, pricing rules, discount rules).  
    * Roles(Manager, Driver, developer).  
    * States(Paid, created, cancelled).  
    * Behaviour(Push notifications sms vs email)     

Our response: *As there are multiple ways these actors/behaviours/policies can change, we can keep the core entities stable and then plug-in different behaviours using Composition*

#### When to choose inheritnce(Only in IS-A setup)
Our response: *As the card payment is a type of payment method we can have a interface that a child implements. But if the child cannot fulfill what the parent promises, we must not use it. Ex: Reactange and Square parent and child classes. resize(width, height) would not go well with the child, so not a good option. We can make sure we are not violating LSP*
Example:
```python
class PaymentMethod:
    def pay(self, amount: int) -> None:
        raise NotImplementedError

class CardPayment(PaymentMethod):
    def pay(self, amount: int) -> None:
        pass
```
#### LSP must be thoroughly followed
When a child is called, it must not surprise the caller, it must keep the parents behaviour intact.   
Otherwise we may need to update all the code where the parent was earlier used, which breaks everything.  
If code expects Base, passing Derived shouldn’t change correctness.
```python
class Rectangle:
    def resize(self, w, h):
        self.w, self.h = w, h

class Square(Rectangle):
    pass  # inherits resize(w,h) -> breaks square constraint
```

#### Use ABC(abstract base classes): Conrtact-like boundaries are set 
Common errors are making a base class instantiable but not used anywhere.   
In this example just having a PayrollPolicy object would violate our code as it is nothing without a proper implementation, so make it an Interface. 
```python
from abc import ABC, abstractmethod

class PayrollPolicy(ABC):
    @abstractmethod
    def calculate(self) -> int: ...

class SalaryPolicy(PayrollPolicy):
    def __init__(self, weekly: int):
        self.weekly = weekly

    def calculate(self) -> int:
        return self.weekly
```
#### Duck-typing
So our main idea is to prioritise *behaviour* over *ancestory*.   
If the code somewhere calls .calculate(), any object fulfilling .calculate() and returning something as expected must be allowed.   
So contracts like interfaces solve this issue. We dont have to worry about the internal implementation, continuing on the above example, any implemented policy object can be used to .calculate().  
This is another way to achieve *polymorphism* besides *inheritence*.    
Idea: If it looks like a duck and quacks like a duck, it must be a duck.
```python
def run_payroll(policy) -> int:
    return policy.calculate()  # duck-typed contract
```

#### Composition: "HAS A"+ methods are delegated
*Delegation* is passing on a task to another object rather than handling the request itself or inheriting from parent.   
This keeps policies or strategies out of the responsibility of the class they are given to.   
For example, an employee need not handle his own policy to get paid. There can be different policies which all satisfy a policy interface and the empolyee can *have* a policy object and its functionality is delegated away from the class.   
This avoids creating a whole variety of subclasses, and code reuse is easier.

#### mixins in python:
Mixins are additional functionalities added to similar classes that help us add them like a feature using multiple inheritance rather than creating a big hierarchy.  
For example:
```python
class Shape:
    def __init__(self, x, y):
        # X and Y coordinates
        self.x, self.y = x, y
    def serialize(self):
        print(",".join([f"{k}-{v}" for k,v in self.__dict__.items()]))

class Rectangle(Shape):
    def __init__(self, x, y, height, width):
        super().__init__(x, y)
        self.height = height
        self.width = width

class Circle(Shape):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

c = Circle(0, 0, 10)
r = Rectangle(1, 3, 4, 5)
c.serialize() # x-0,y-0,radius-10
r.serialize() # x-1,y-3,height-4,width-5
```
Here the base class is having shared responsibilities, so if we must use inheritance, we must create a separate *Serializable* class and make *Shape* inherit from that.   
If we have another class and subclass setup for which we need serialisation of objects, we must define the base class to extend form *Serializable* which leads to long chains of inheritence.  
For small feature additions *mixins* are great, we cab create another class and use *multiple inheritence* which gives the *serialize()* method when inherited.
```python
class Shape:
    def __init__(self, x, y):
        # X and Y coordinates
        self.x, self.y = x, y

class Serializer:    
    def serialize(self):
        print(",".join([f"{k}-{v}" for k,v in self.__dict__.items()]))

class Rectangle(Shape, Serializer):
    def __init__(self, x, y, height, width):
        super().__init__(x, y)
        self.height = height
        self.width = width

class Circle(Shape, Serializer):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

c = Circle(0, 0, 10)
r = Rectangle(1, 3, 4, 5)
c.serialize()
r.serialize()
```
This is a better implementation. A mixin is a class with a single purpose to add functionality to other classes.   
Uses: Loggers, Serializers, Comparators

#### MRO and Multiple inheritence:
Also we want to avoid Multiple inheritence to avoid diamond inheritence or mro calling wrong constructors. There can be conflicting __init__ signatures.   
So, we must choose composition and if needed mixins for isolated features. 
