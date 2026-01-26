# LLD Interivew tips
Structure should look like:
1. Identify *entites* (nouns).  
Example: **User**, **Order**, **Product**
2. Model a stable core as an *entity*: Create classes for core-nouns that are relatively stable. 
3. Identify *behaviours* (Axes for different actions).  
 Pinpoint those that change independently (PaymentMethod, NotificationType)
3. *Plug-in behaviours* like policy, strategy. (Composition)
4. *Interfaces/ ABCs(Protocol)* for contracts.
5. Avoid huge constructors. Use *Factory* for object creation.

This setup helps us have *high cohesion* and *low coupling* 




## OOPS & concepts
```python
"""
PYTHON CLASS DESIGN: REVISION CHEAT SHEET
"""

# ---------------------------------------------------------
# 1. THE "STATE & SAFETY" RULES
# ---------------------------------------------------------

class Rectangle:
    """Enforce rules at birth and never bypass setters."""
    def __init__(self, w, h):
        # Good: Assigning to self.w triggers the @w.setter logic immediately.
        # Bad: Using self._w = w would skip the validation gate.
        self.w = w     
        self.h = h

    @property
    def w(self): 
        return self._w

    @w.setter
    def w(self, value):
        # Pick the right boundary: if spec says positive, use <= 0
        if value <= 0:
            raise ValueError("Width must be > 0")
        self._w = value

# ---------------------------------------------------------
# 2. THE "CLEAN LOGIC" RULES
# ---------------------------------------------------------

class User:
    """Don't Repeat Yourself (DRY) and Separate Concerns."""
    def __init__(self, age):
        self.age = age  # Single source of validation (reuses setter)

    @property
    def age(self): 
        return self._age

    @age.setter
    def age(self, v):
        if v < 0:
            raise ValueError("Age must be >= 0")
        self._age = v

    def get_info(self):
        # Separation of Concerns: Return data, don't print it.
        return f"User age is {self.age}"

# ---------------------------------------------------------
# 3. THE "ANTI-CLUTTER" & "PROFESSIONAL HABITS" RULES
# ---------------------------------------------------------

class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Must deposit positive amount")
        self.balance += amount

# Respect Encapsulation: 
# Good: account.deposit(100)
# Bad:  account._balance += 100 (Don't touch private internals of others!)

# Proofread Names:
# assert my_rect.intersects(other)  <-- Check for typos like 'intersetcs'
```