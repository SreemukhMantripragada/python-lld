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