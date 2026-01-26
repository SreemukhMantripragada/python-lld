# Dataclasses
Saves us with the struggle of writing so much boilerplate code.   
They do not enforce types at runtime.   
Type hints are mandatory for declaring fields in a dataclass.    
Data class is also just a regular class if we want to add functions etc.  
```python
from dataclasses import dataclass
import inspect

@dataclass
class Comment:
    id: int
    text: str

comment = Comment(1, "comment")
print(comment) # Comment(id=1, text='comment')
print(inspect.getmembers(Comment, inspect.isfunction)) 
# Implements __init__, __repr__, __eq__
```
If we want to hash the *Comment* class, we must use frozen=True to make it immutable.
```python
@dataclass(frozen=True)
class Comment:
    id: int
    text: str
# Now this has __hash__, __setattr__, __delattr__ also implemented which make it hashable.
```
If we want basic comparisions for our objects, we can use order=True. 
```python
@dataclass(frozen=True,order=True)
class Comment:
    id: int
    text: str

# Implements greater than, less than, greater than equal to etc.
# Has extra __ge__, __gt__, __le__, __lt__ 
# Same order that a tuple of attributes have.
```
We can provide default values for our attributes but we must be careful, we dont want different objects to share a reference to a mutable object, for example a list.     
Under the hood all the attributes are defined as fields.   
So *text:str = field(default="")*
```python
from dataclasses import dataclass, field
@dataclass(frozen=True,order=True)
class Comment:
    id: int
    text: str = ""
    replies: list[int] = field(default_factory=list)
```
If we want some field to be prevented from being compared, we can pass *compare=False* in the field.   
Other options: *hash=False*, *repr=False*
```python
@dataclass(slots=True)
class Point:
    x: int
    y: int
```
Using slots=True automatically generates the *__slots\_\_* atribute for a class which provides significant memory and performance benifits by preventing creation of an instance *__dict\_\_*
1. Memory Efficiency: By default, Python instances have a *__dict\_\_* for dynamic attribute assignment. *__slots\_\_* replaces this with a fixed-size, more memory-efficient internal structure, which is very useful when creating a large number of instances.
2. Performance: Direct access to attributes is generally faster than dictionary lookups.
3. Code Clarity: The *__slots\_\_* declaration explicitly defines which attributes the class is intended to have, enforcing a predictable structure. 

We cannot dynamically add new attributes to the objects with slots set to True.

## Interview tips
1. *tuples/dicts*: Issue with these are: error-prone, key consistency must be maintained, positional mistakes etc. Are generally lightweight, but harder to evolve. 
2. *namedtuple*: Immutable by nature, and behaves like a tuple. Not easy to use or extend. But have nice repr. Harder to attach methods, not class like. 
3. *attrs*: Very powerful third party library, but also adds dependency, dataclasses are now used everywhere.

Use dataclass when we want mostly data objects and some functionalities. 
### Most used features in interviews:
1. Default values:
For mutables, we can use other classes like dict, set, some complex object we defined.   
If we are not careful enough, the objects might be shared, using default_factory, it generates is as the object is instantiated.
    ```python
        x: int = 0 # Immutables
        nums: list[int] = field(default_factory=list) # Mutables
    ```
2. Every field must be annotated like : int, : str etc, but type is not enforced. We need to use other static tools like (mypy/pyright) to enforce typing. 
3. Customising *field*:   
    * default: Fixed default value(for immutables)
    * default_factory: Callable that produces a new default object(Must not need some more arguments to create)
    * init: True/False, lets us not initialise some fields and we can do it later on.
    * Other true or false options are *compare*, *__repr\_\_*. (when we have fields like metadata, we dont want them to be used for comparision or display ex. created_at timestamp)
4. We can add domain specific methods if needed. Usecases: distance_to, total_price, from_json, to_json etc.   
But we need to try and keep it to bare minimum functionality, is class grows heavily with logic, we might consider separating dataclass to be just a data container.   
5. Setting order=True, we can compare objects in the declared order of fields. Useful for scheduling, priority queues etc. We can also add something that we know can be used to compare, ex. a field sort_index declared at the start can be a tiebreaking decider. We can compute it as needed. We can keep it out of repr, init
6. *__post_init\_\_*: This is run automatically after the dataclass is initiated.    
    Common uses:  
    * Compute derived_variables like sort_index, cache_key etc
    * Validate invariants(check field values)
    
    ```python
    from dataclasses import dataclass, field

    @dataclass
    class Person:
        first_name: str
        last_name: str
        full_name: str = field(init=False)

        def __post_init__(self):
            self.full_name = f"{self.first_name} {self.last_name}"
    ```
7. *FrozenInstanceError* is raised if we try to set some attributes of an object of a (frozen=True) dataclass.   
Although if a list is present in a immutable dataclass object, we can still append to that list, for true immutability, use immutable fields as well. 
8. Inheritence: 
    * Sub-classes must not have non-default fields if atleast one of the field has default field. 
    * Field order is unchanged from the parent, if we set a few fields, they will still be in the order as they were in the parent.  
Most cases suit composition over inheritence due to these complications. 
