#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 类(Class)学习教程
从基础到进阶，帮助你快速理解Python中的类概念
"""

print("=" * 50)
print("Python 类(Class)学习教程")
print("=" * 50)

# 1. 最简单的类定义
print("\n1. 最简单的类定义")
print("-" * 30)

class Person:
    """这是一个人的类"""
    pass  # pass表示什么都不做，占位符

# 创建对象（实例化）
person1 = Person()
print(f"person1 是 Person 类的实例: {isinstance(person1, Person)}")

# 2. 带属性的类
print("\n2. 带属性的类")
print("-" * 30)

class Student:
    """学生类 - 带有类属性"""
    school = "清华大学"  # 类属性，所有实例共享

    def __init__(self, name, age):
        """构造函数，创建对象时自动调用"""
        self.name = name  # 实例属性
        self.age = age    # 实例属性
        print(f"创建了学生: {name}")

# 创建学生对象
student1 = Student("小明", 18)
student2 = Student("小红", 19)

print(f"学生1: {student1.name}, 年龄: {student1.age}, 学校: {student1.school}")
print(f"学生2: {student2.name}, 年龄: {student2.age}, 学校: {student2.school}")

# 3. 带方法的类
print("\n3. 带方法的类")
print("-" * 30)

class Dog:
    """狗类 - 带有方法"""

    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.energy = 100

    def bark(self):
        """狗叫方法"""
        print(f"{self.name} 汪汪叫!")
        return "汪汪!"

    def run(self):
        """跑步方法"""
        if self.energy > 10:
            self.energy -= 10
            print(f"{self.name} 跑了一圈，剩余体力: {self.energy}")
        else:
            print(f"{self.name} 太累了，需要休息")

    def sleep(self):
        """睡觉方法"""
        self.energy = 100
        print(f"{self.name} 睡了一觉，体力恢复到: {self.energy}")

    def introduce(self):
        """自我介绍"""
        print(f"我是 {self.name}，是一只 {self.breed}")

# 创建狗对象并调用方法
my_dog = Dog("旺财", "金毛")
my_dog.introduce()
my_dog.bark()
my_dog.run()
my_dog.run()
my_dog.sleep()

# 4. 类的继承
print("\n4. 类的继承")
print("-" * 30)

class Animal:
    """动物基类"""

    def __init__(self, name, species):
        self.name = name
        self.species = species
        self.alive = True

    def eat(self):
        print(f"{self.name} 正在吃东西")

    def sleep(self):
        print(f"{self.name} 正在睡觉")

    def make_sound(self):
        print(f"{self.name} 发出了声音")

class Cat(Animal):  # Cat继承自Animal
    """猫类 - 继承自动物类"""

    def __init__(self, name, color):
        super().__init__(name, "猫")  # 调用父类构造函数
        self.color = color

    def make_sound(self):  # 重写父类方法
        print(f"{self.name} 喵喵叫")

    def climb_tree(self):  # 猫特有的方法
        print(f"{self.name} 爬上了树")

class Bird(Animal):  # Bird也继承自Animal
    """鸟类 - 继承自动物类"""

    def __init__(self, name, can_fly=True):
        super().__init__(name, "鸟")
        self.can_fly = can_fly

    def make_sound(self):  # 重写父类方法
        print(f"{self.name} 叽叽喳喳")

    def fly(self):  # 鸟特有的方法
        if self.can_fly:
            print(f"{self.name} 飞起来了")
        else:
            print(f"{self.name} 不会飞")

# 创建不同的动物
cat = Cat("咪咪", "白色")
bird = Bird("小鸟")
penguin = Bird("企鹅", can_fly=False)

print("=== 猫的行为 ===")
cat.eat()  # 继承的方法
cat.make_sound()  # 重写的方法
cat.climb_tree()  # 自己的方法

print("\n=== 鸟的行为 ===")
bird.make_sound()
bird.fly()

print("\n=== 企鹅的行为 ===")
penguin.make_sound()
penguin.fly()

# 5. 私有属性和方法
print("\n5. 私有属性和方法")
print("-" * 30)

class BankAccount:
    """银行账户类 - 演示私有属性"""

    def __init__(self, owner, initial_balance=0):
        self.owner = owner
        self.__balance = initial_balance  # 私有属性，以双下划线开头

    def deposit(self, amount):
        """存款"""
        if amount > 0:
            self.__balance += amount
            print(f"存入 {amount} 元，余额: {self.__balance} 元")
        else:
            print("存款金额必须大于0")

    def withdraw(self, amount):
        """取款"""
        if amount > 0 and amount <= self.__balance:
            self.__balance -= amount
            print(f"取出 {amount} 元，余额: {self.__balance} 元")
        else:
            print("取款失败：金额无效或余额不足")

    def get_balance(self):
        """获取余额 - 公共方法访问私有属性"""
        return self.__balance

    def __validate_transaction(self, amount):
        """私有方法 - 验证交易"""
        return amount > 0 and amount <= self.__balance

# 使用银行账户
account = BankAccount("张三", 1000)
print(f"账户所有者: {account.owner}")
print(f"当前余额: {account.get_balance()} 元")

account.deposit(500)
account.withdraw(200)

# 尝试直接访问私有属性（会出错或得不到预期结果）
# print(account.__balance)  # 这样访问会报错
print(f"通过公共方法获取余额: {account.get_balance()} 元")

# 6. 类方法和静态方法
print("\n6. 类方法和静态方法")
print("-" * 30)

class MathUtils:
    """数学工具类 - 演示类方法和静态方法"""

    pi = 3.14159  # 类属性

    def __init__(self, name):
        self.name = name

    @staticmethod
    def add(a, b):
        """静态方法 - 不需要访问类或实例"""
        return a + b

    @staticmethod
    def multiply(a, b):
        """静态方法"""
        return a * b

    @classmethod
    def circle_area(cls, radius):
        """类方法 - 可以访问类属性"""
        return cls.pi * radius * radius

    @classmethod
    def create_calculator(cls, name):
        """类方法 - 创建实例的另一种方式"""
        return cls(name)

# 使用静态方法（不需要创建实例）
print(f"5 + 3 = {MathUtils.add(5, 3)}")
print(f"4 × 6 = {MathUtils.multiply(4, 6)}")

# 使用类方法
print(f"半径为5的圆的面积: {MathUtils.circle_area(5)}")

# 通过类方法创建实例
calc = MathUtils.create_calculator("我的计算器")
print(f"计算器名称: {calc.name}")

# 7. 特殊方法（魔法方法）
print("\n7. 特殊方法（魔法方法）")
print("-" * 30)

class Book:
    """书籍类 - 演示特殊方法"""

    def __init__(self, title, author, pages):
        self.title = title # 书名
        self.author = author # 作者
        self.pages = pages # 页码

    def __str__(self):
        """字符串表示 - print时调用"""
        return f"《{self.title}》 - {self.author}"

    def __repr__(self):
        """开发者字符串表示"""
        return f"Book('{self.title}', '{self.author}', {self.pages})"

    def __len__(self):
        """长度 - len()函数调用"""
        return self.pages

    def __eq__(self, other):
        """相等比较 - == 操作符"""
        if isinstance(other, Book):
            return self.title == other.title and self.author == other.author
        return False

    def __lt__(self, other):
        """小于比较 - < 操作符"""
        if isinstance(other, Book):
            return self.pages < other.pages
        return False

# 创建书籍对象
book1 = Book("Python编程", "张三", 300)
book2 = Book("Java编程", "李四", 250)
book3 = Book("Python编程", "张三", 300)

print(f"书籍1: {book1}")  # 调用 __str__
print(f"书籍1页数: {len(book1)}")  # 调用 __len__
print(f"book1 == book3: {book1 == book3}")  # 调用 __eq__
print(f"book2 < book1: {book2 < book1}")  # 调用 __lt__

# 8. 属性装饰器
print("\n8. 属性装饰器")
print("-" * 30)

class Temperature:
    """温度类 - 演示属性装饰器"""

    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        """摄氏度属性"""
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """设置摄氏度"""
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度(-273.15°C)")
        self._celsius = value

    @property
    def fahrenheit(self):
        """华氏度属性（只读）"""
        return self._celsius * 9/5 + 32

    @property
    def kelvin(self):
        """开尔文温度（只读）"""
        return self._celsius + 273.15

# 使用温度类
temp = Temperature(25)
print(f"摄氏度: {temp.celsius}°C")
print(f"华氏度: {temp.fahrenheit}°F")
print(f"开尔文: {temp.kelvin}K")

temp.celsius = 30  # 使用setter
print(f"新的摄氏度: {temp.celsius}°C")
print(f"对应华氏度: {temp.fahrenheit}°F")

# 9. 实际应用示例：学生管理系统
print("\n9. 实际应用示例：学生管理系统")
print("-" * 30)

class Course:
    """课程类"""

    def __init__(self, name, credits):
        self.name = name
        self.credits = credits

    def __str__(self):
        return f"{self.name}({self.credits}学分)"

class StudentManager:
    """学生管理类"""

    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.courses = []  # 课程列表
        self.grades = {}   # 成绩字典

    def add_course(self, course):
        """添加课程"""
        if course not in self.courses:
            self.courses.append(course)
            print(f"{self.name} 添加了课程: {course}")
        else:
            print(f"课程 {course} 已存在")

    def set_grade(self, course_name, grade):
        """设置成绩"""
        self.grades[course_name] = grade
        print(f"{self.name} 的 {course_name} 成绩设为: {grade}")

    def get_gpa(self):
        """计算GPA"""
        if not self.grades:
            return 0
        total_points = sum(self.grades.values())
        return total_points / len(self.grades)

    def show_transcript(self):
        """显示成绩单"""
        print(f"\n=== {self.name} 的成绩单 ===")
        print(f"学号: {self.student_id}")
        print("课程成绩:")
        for course in self.courses:
            grade = self.grades.get(course.name, "未评分")
            print(f"  {course}: {grade}")
        print(f"平均分: {self.get_gpa():.2f}")

# 使用学生管理系统
python_course = Course("Python编程", 3)
math_course = Course("高等数学", 4)
english_course = Course("大学英语", 2)

student = StudentManager("王小明", "2023001")
student.add_course(python_course)
student.add_course(math_course)
student.add_course(english_course)

student.set_grade("Python编程", 95)
student.set_grade("高等数学", 88)
student.set_grade("大学英语", 92)

student.show_transcript()

print("\n" + "=" * 50)
print("教程结束！")
print("=" * 50)
print("""
总结：
1. 类是对象的模板，对象是类的实例
2. __init__ 是构造函数，创建对象时调用
3. self 代表当前实例
4. 继承让子类获得父类的属性和方法
5. 私有属性用双下划线开头
6. 特殊方法让类支持内置操作
7. 属性装饰器让方法像属性一样使用

继续练习这些概念，你很快就能掌握Python的类！
""")
