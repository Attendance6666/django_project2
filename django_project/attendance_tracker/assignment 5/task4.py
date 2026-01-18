class Employee:
    def __init__(self, salary):
        self._salary = salary

    def get_salary(self):
        return self._salary

    def get_role(self):
        return "Employee"


class Manager(Employee):
    def __init__(self, salary, bonus):
        super().__init__(salary)
        self._bonus = bonus

    def get_role(self):
        return "Manager"

    def get_bonus(self):
        return self._bonus


def print_employees(employees):
    for emp in employees:
        print(emp.get_role(), "-", emp.get_salary())


e1 = Employee(200000)
e2 = Manager(350000, 50000)

print_employees([e1, e2])
