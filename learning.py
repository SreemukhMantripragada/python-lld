from __future__ import annotations
print("-"*30)
"""
1.1 Point distance + repr

Build: Point(x, y) with distance_to(other) and a readable __repr__.
Done when:

Point(0,0).distance_to(Point(3,4)) == 5

repr(Point(1,2)) looks like Point(x=1, y=2)

1.6 Point translate (immutability not required yet)

Build: translate(dx, dy) mutates self.
Done when:

p = Point(1,2); p.translate(2,3) → p is (3,5)
"""
import math
class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
    
    def distance_to(self, other: Point) -> float:
        return math.sqrt((self.x-other.x)**2+(self.y-other.y)**2)
    
    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

    def translate(self, dx, dy)-> None:
        self.x += dx
        self.y += dy
print(Point(0,0).distance_to(Point(3,4)))
print(repr(Point(1,2)))

p = Point(1, 2)
print(repr(p))
p.translate(2, 3)
print(repr(p))
print("-"*30)
"""
1.2 Rectangle invariants

Build: Rectangle(x, y, w, h) where w,h must be > 0.
Add: area(), contains(point).
Done when:

Creating with w<=0 or h<=0 raises ValueError

contains includes boundary: (x,y) to (x+w, y+h)

1.5 Rectangle intersection check (no geometry library)

Build: intersects(other) for axis-aligned rectangles.
Done when:

Overlapping returns True

Touching edge counts as True (or False) — pick one and stay consistent
"""

class Rectangle:
    def __init__(self, x, y, w, h) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    @property
    def w(self):
        return self._w
    @property
    def h(self):
        return self._h
    @w.setter
    def w(self, w):
        if w<=0:
            raise ValueError("Width cannot be <=0")
        self._w = w
    @h.setter
    def h(self, h):
        if h<=0:
            raise ValueError("Height cannot be <=0")
        self._h = h

    def area(self) -> float:
        return self._w*self._h
    def contains(self, point: Point) -> bool:
        # We must check if point.x lies between self.x and self.x+h
        # Similarly for y
        if point.x>=self.x and point.x<=(self.x+self._w):
            if point.y>=self.y and point.y<=(self.y+self._h):
                return True
        return False
    def intersetcs(self, other: Rectangle) -> bool:
        # We will consider just touching also to be intersecting.
        # The possibilites for intersections are-> atleast one of the corner points of one rec are in other rec.
        # Or viceversa
        corners = [[0, 0], [self._w, 0], [0, self._h], [self._w, self._h]]
        for i, j in corners:
            pt = Point(self.x+i, self.y+j)
            if other.contains(pt):
                return True
        corners = [[0, 0], [other._w, 0], [0, other._h], [other._w, other._h]]
        for i, j in corners:
            pt = Point(other.x+i, other.y+j)
            if self.contains(pt):
                return True        
        return False
try:
    rect = Rectangle(0, 0, -1, 2)
except Exception as v:
    print(f"Error occured: {v}")
print(Rectangle(0, 0, 2, 2).contains(Point(1, 1)))
print(Rectangle(0, 0, 2, 2).contains(Point(3, 1)))

print(Rectangle(0, 0, 2, 2).intersetcs(Rectangle(1, 1, 2, 2)))
print(Rectangle(0, 0, 2, 2).intersetcs(Rectangle(3, 3, 2, 2)))
print("-"*30)
"""
1.3 BankAccount: deposit/withdraw with rules

Build: BankAccount(owner, balance=0) with:

deposit(amount) amount > 0

withdraw(amount) amount > 0 and can’t go below 0
Done when:

Invalid operations raise ValueError

Balance never negative

1.4 BankAccount transfer

Build: transfer_to(other, amount) using withdraw/deposit.
Done when:

Total money conserved

Transfer fails safely if insufficient funds (no partial changes)
"""
import threading
class BankAccount:
    def __init__(self, owner: str, balance: float)->None:
        self._owner = owner
        self._balance = balance
        self._lock = threading.Lock()

    def deposit(self, amount: float)->None:
        if amount<0:
            raise ValueError("Amount to deposit cannot be negative")
        self._balance += amount
        print(f"Amount ${amount} deposited!")
    
    def withdraw(self, amount: float)->None:
        if amount<0:
            raise ValueError("Amount to be withdrawn cannot be negative")
        if amount<=self._balance:
            self._balance -= amount
            print(f"Amount ${amount} withdrawn!")
        else:
            raise ValueError("Cannot withdraw more than available balance")

    def transfer_to(self, other: BankAccount, amount: float)-> None:
        if amount<0:
            raise ValueError("Amount to transfer must be positive")
        if self._balance<amount:
            raise ValueError("Insufficient funds to transfer")
        with self._lock:
            self._balance -= amount
            other._balance += amount
            print(f"Amount ${amount} transferred from {self._owner} to {other._owner}!")

bnkact = BankAccount("Steve", 20)
try: 
    bnkact.withdraw(15)
except Exception as e:
    print(e)
try: 
    bnkact.deposit(-1)
except Exception as e:
    print(e)
try: 
    bnkact.deposit(10)
except Exception as e:
    print(e)
try: 
    bnkact.withdraw(20)
except Exception as e:
    print(e)
try: 
    bnkact.withdraw(5)
except Exception as e:
    print(e)

otheract = BankAccount("John", 25)
try: 
    bnkact.transfer_to(otheract, -5)
except Exception as e:
    print(e)
try: 
    bnkact.transfer_to(otheract, 100)
except Exception as e:
    print(e)
try: 
    bnkact.transfer_to(otheract, 5)
except Exception as e:
    print(e)


print("-"*30)
"""
1.7 Simple “domain object”

Build: TodoItem(title, done=False) with mark_done().
Done when:

Marking done flips state, no weird extra fields
"""
class TodoItem:
    def __init__(self, title: str, done:bool =False)-> None:
        self.title = title
        self.done = done

    def mark_done(self):
        self.done = True
    def __repr__(self):
        return f"Task: {self.title} Status: {self.done}"
td_item = TodoItem("Task1")
print(td_item)
td_item.mark_done()
print(td_item)

print("-"*30)
"""
1.8 Tiny “system” using objects

Build: TodoList with add(item) and pending_count().
Done when:

Pending count changes when items marked done
"""
class TodoList:
    def __init__(self):
        self.items = []
        self._pending_count = 0
    
    @property
    def pending_count(self):
        count = 0
        for item in self.items:
            if not item.done:
                count += 1
        return count
    
    def add(self, item: TodoItem):
        self.items.append(item)
    
todolist = TodoList()
item1 = TodoItem("task1")
todolist.add(item1)
item2 = TodoItem("task2")
todolist.add(item2)
print(todolist.pending_count)
item3 = TodoItem("task3")
todolist.add(item3)
item1.mark_done()
item2.mark_done()
print(todolist.pending_count)