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

emp1 = Employee('Adam', 'Sandler', 10000)
emp2 = Employee('John', 'Boyle', 20000) 

# print(emp1.fullname())
# print(emp2.fullname())

# print(emp1.pay)
# print(emp2.pay)
# emp1.apply_raise()
# emp2.apply_raise()
# print(emp1.pay)
# print(emp2.pay)
# print(Employee.raise_amount)

# # Using classmethods
# print(emp1.raise_amount)
# print(emp2.raise_amount)
# print(Employee.raise_amount)

# Employee.set_raise_amnt(1.05)

# print(emp1.raise_amount)
# print(emp2.raise_amount)
# print(Employee.raise_amount)


# import datetime
# today = datetime.date(2025, 7, 10)

# print(Employee.is_workday(today))

# dev1 = Developer("Adam", "Sandler", 10000)
# print(dev1.email)
# print(help(Developer))


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
# print(mgr1.print_emps())
# mgr1.add_emp(dev2)
# print(mgr1.print_emps())
# mgr1.remove_emp(dev1)
mgr1.print_emps()
print(isinstance(dev1, Employee)) #True
print(issubclass(Developer, Employee)) #True
print(issubclass(Developer, Manager)) # False
