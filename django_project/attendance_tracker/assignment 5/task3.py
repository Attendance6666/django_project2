class Person:
    def __init__(self, name):
        self._name = name

    def get_role(self):
        return "Person"


class Student(Person):
    def __init__(self, name, student_id):
        super().__init__(name)
        self.__student_id = student_id

    def get_role(self):
        return "Student"


person = Person("Alex")
student = Student("Aisultan", "S123")

print(person.get_role())
print(student.get_role())
