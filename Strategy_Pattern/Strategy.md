# Strategy Design Pattern
A **Behavioural** Design pattern that lets us define a family of algorithms and choose their objects interchangably.
We can define interface of the way we want to do something, and then use this in place of specific classes.    
Example: Notification service can support SMS, Email, Push notifications. We cannot write if else statements inside our notification class. We can use a common interface of INotificationService and it will be concretely implemented for each of the options.   
We can keep adding other notification services or alter their implementations keeping the rest of the code intact.   

This is a solution to Open-Closed principle. 
```python
#BAD: Violates OCP. Every new vehicle type requires changing this class.
class ParkingFeeCalculator:
    def calculate(self, minutes, vehicle_type):
        if vehicle_type == "COACH":
            return minutes * 5
        elif vehicle_type == "CAR":
            return minutes * 2
        elif vehicle_type == "BIKE":
            return minutes * 1
```
```python
from abc import ABC, abstractmethod

class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, minutes: int) -> int:
        ...
class CarPricing(PricingStrategy):
    def calculate(self, minutes: int) -> int:
        return 5*minutes
class BikePricing(PricingStrategy):
    def calculate(self, minutes: int) -> int:
        return 2*minutes

class ParkingTicket:
    def __init__(self, strategy: PricingStrategy) -> None:
        self.strategy = strategy
    def get_amount(self, minutes: int) -> int:
        return self.strategy.calculate(minutes)
```

### Combo with Factory Pattern
The **Factory Design Pattern** is the perfect partner for Strategy Pattern.   
If the strategies are the tools needed, the Factory can be one choosing the right one based on our need.   
Without the Factory Pattern, Client code must decide on which strategy to instantiate and pass.  

We can extend the above example as follows:
```python
from __future__ import annotations

class PricingFactory:
    _strategies = {
        "CAR": CarPricing,
        "BIKE": BikePricing
    }

    @staticmethod
    def get_strategy(vehicle_type: str) -> PricingStrategy:
        strategy_class = PricingFactory._strategies.get(vehicle_type.upper())

        if not strategy_class:
            raise ValueError(f"No pricing strategy for {vehicle_type}")
        
        return strategy_class()
```

This makes our Client code simpler and abstracted away from the internal implementations and instantiations of strategies
```python
vehicle_type = "CAR"
duration = 60

strategy = PricingFactory.get_strategy(vehicle_type)

fee = strategy.calculate(duration)
```