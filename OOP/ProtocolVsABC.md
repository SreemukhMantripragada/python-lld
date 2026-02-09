# ABCs Vs Protocol
### ABC(Abstract Base Classes)
We use these when we want strict hierarchy. Every subclass **is a** version of its parent and must follow these rules.   
To enforce children to follow rules, we can use the *abstractmethod* decorator.  
We cannot instantiate a parent by itself.  
```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    def print_receipt(self, amount):
        # Shared logic: Every payment type prints a receipt the same way
        print(f"Receipt: Paid ${amount}")

    @abstractmethod
    def process_payment(self, amount):
        # Forced logic: Every subclass MUST define how it pays
        pass

class Stripe(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Processing ${amount} via Stripe API...")
```

### Protocols
These just care about the ability of an object to have some characteristics. Useful when there are totally unrelated classes like **Document** and **User** but both happen to have be an **Exportable**.   
This is called *Static Duck Typing*
```python
from typing import Protocol

class Scannable(Protocol):
    def scan(self) -> str:
        ...

class Passport:
    def scan(self): return "Passport Data"

class Barcode:
    def scan(self): return "Product ID: 123"

def process_item(item: Scannable):
    # This function accepts ANYTHING as long as it has a .scan() method
    print(f"Reading: {item.scan()}")
```


## Choice
#### ABC:
1. We want a common code for subclasses.
2. We have a clear IS-A relationship
3. We want to prevent people from creating base class directly
#### Protocol:
1. We want to define a requirement without forcing relationships
2. We want Duck-Typing, not rigid
3. We want to keep things decoupled and not force inheritance when it is not natural.