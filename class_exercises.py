#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 类练习题
动手实践，加深理解
"""

print("=" * 50)
print("Python 类练习题")
print("=" * 50)

# 练习1：创建一个简单的汽车类
print("\n练习1：汽车类")
print("-" * 30)
print("任务：创建一个Car类，包含品牌、型号、颜色属性，以及启动、停止方法")

class Car:
    """汽车类 - 练习1答案"""

    def __init__(self, brand, model, color):
        self.brand = brand
        self.model = model
        self.color = color
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.is_running = True
            print(f"{self.color}的{self.brand} {self.model} 启动了！")
        else:
            print("汽车已经在运行中")

    def stop(self):
        if self.is_running:
            self.is_running = False
            print(f"{self.brand} {self.model} 停止了")
        else:
            print("汽车已经停止")

    def info(self):
        status = "运行中" if self.is_running else "停止"
        print(f"汽车信息：{self.brand} {self.model}，颜色：{self.color}，状态：{status}")

# 测试汽车类
my_car = Car("丰田", "卡罗拉", "白色")
my_car.info()
my_car.start()
my_car.info()
my_car.stop()

# 练习2：创建一个矩形类
print("\n练习2：矩形类")
print("-" * 30)
print("任务：创建Rectangle类，计算面积和周长")

class Rectangle:
    """矩形类 - 练习2答案"""

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        """计算面积"""
        return self.width * self.height

    def perimeter(self):
        """计算周长"""
        return 2 * (self.width + self.height)

    def __str__(self):
        return f"矩形(宽:{self.width}, 高:{self.height})"

# 测试矩形类
rect = Rectangle(5, 3)
print(f"{rect}")
print(f"面积: {rect.area()}")
print(f"周长: {rect.perimeter()}")

# 练习3：继承练习 - 动物园
print("\n练习3：动物园继承练习")
print("-" * 30)
print("任务：创建动物基类和具体动物子类")

class Animal:
    """动物基类"""

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def eat(self):
        print(f"{self.name} 正在吃东西")

    def sleep(self):
        print(f"{self.name} 正在睡觉")

    def make_sound(self):
        print(f"{self.name} 发出声音")

class Lion(Animal):
    """狮子类"""

    def __init__(self, name, age, mane_color):
        super().__init__(name, age)
        self.mane_color = mane_color

    def make_sound(self):
        print(f"{self.name} 发出威猛的吼声：吼吼吼！")

    def hunt(self):
        print(f"{self.name} 正在狩猎")

class Elephant(Animal):
    """大象类"""

    def __init__(self, name, age, trunk_length):
        super().__init__(name, age)
        self.trunk_length = trunk_length

    def make_sound(self):
        print(f"{self.name} 发出响亮的叫声：嗷嗷嗷！")

    def spray_water(self):
        print(f"{self.name} 用{self.trunk_length}米长的鼻子喷水")

# 测试动物类
lion = Lion("辛巴", 5, "金色")
elephant = Elephant("大象", 10, 2.5)

print("=== 狮子的行为 ===")
lion.eat()
lion.make_sound()
lion.hunt()

print("\n=== 大象的行为 ===")
elephant.eat()
elephant.make_sound()
elephant.spray_water()

# 练习4：银行账户系统
print("\n练习4：银行账户系统")
print("-" * 30)
print("任务：创建银行账户类，支持存款、取款、转账")

class BankAccount:
    """银行账户类"""

    # 类属性：银行名称
    bank_name = "Python银行"

    def __init__(self, account_holder, account_number, initial_balance=0):
        self.account_holder = account_holder
        self.account_number = account_number
        self.__balance = initial_balance  # 私有属性
        self.transaction_history = []

    def deposit(self, amount):
        """存款"""
        if amount > 0:
            self.__balance += amount
            self.transaction_history.append(f"存款: +{amount}")
            print(f"存款成功！当前余额: {self.__balance}")
        else:
            print("存款金额必须大于0")

    def withdraw(self, amount):
        """取款"""
        if amount > 0 and amount <= self.__balance:
            self.__balance -= amount
            self.transaction_history.append(f"取款: -{amount}")
            print(f"取款成功！当前余额: {self.__balance}")
        else:
            print("取款失败：金额无效或余额不足")

    def transfer(self, other_account, amount):
        """转账"""
        if amount > 0 and amount <= self.__balance:
            self.__balance -= amount
            other_account.__balance += amount
            self.transaction_history.append(f"转出: -{amount} 到 {other_account.account_holder}")
            other_account.transaction_history.append(f"转入: +{amount} 从 {self.account_holder}")
            print(f"转账成功！向 {other_account.account_holder} 转账 {amount} 元")
        else:
            print("转账失败：金额无效或余额不足")

    def get_balance(self):
        """获取余额"""
        return self.__balance

    def show_statement(self):
        """显示账单"""
        print(f"\n=== {self.account_holder} 的账单 ===")
        print(f"账号: {self.account_number}")
        print(f"当前余额: {self.__balance}")
        print("交易记录:")
        for transaction in self.transaction_history[-5:]:  # 显示最近5笔交易
            print(f"  {transaction}")

# 测试银行账户
account1 = BankAccount("张三", "001", 1000)
account2 = BankAccount("李四", "002", 500)

print(f"银行名称: {BankAccount.bank_name}")
account1.deposit(200)
account1.withdraw(100)
account1.transfer(account2, 300)

account1.show_statement()
account2.show_statement()

# 练习5：图书管理系统
print("\n练习5：图书管理系统")
print("-" * 30)
print("任务：创建图书和图书馆类")

class Book:
    """图书类"""

    def __init__(self, title, author, isbn, copies=1):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.total_copies = copies
        self.available_copies = copies

    def __str__(self):
        return f"《{self.title}》 - {self.author}"

    def __eq__(self, other):
        if isinstance(other, Book):
            return self.isbn == other.isbn
        return False

class Library:
    """图书馆类"""

    def __init__(self, name):
        self.name = name
        self.books = []
        self.borrowed_books = {}  # {用户名: [借阅的书]}

    def add_book(self, book):
        """添加图书"""
        if book in self.books:
            # 如果书已存在，增加副本数
            existing_book = self.books[self.books.index(book)]
            existing_book.total_copies += book.total_copies
            existing_book.available_copies += book.available_copies
            print(f"增加了 {book.total_copies} 本《{book.title}》")
        else:
            self.books.append(book)
            print(f"添加了新书：{book}")

    def borrow_book(self, user, book_title):
        """借书"""
        for book in self.books:
            if book.title == book_title and book.available_copies > 0:
                book.available_copies -= 1
                if user not in self.borrowed_books:
                    self.borrowed_books[user] = []
                self.borrowed_books[user].append(book)
                print(f"{user} 成功借阅了《{book_title}》")
                return True
        print(f"借阅失败：《{book_title}》暂时无法借阅")
        return False

    def return_book(self, user, book_title):
        """还书"""
        if user in self.borrowed_books:
            for book in self.borrowed_books[user]:
                if book.title == book_title:
                    book.available_copies += 1
                    self.borrowed_books[user].remove(book)
                    print(f"{user} 成功归还了《{book_title}》")
                    return True
        print(f"归还失败：{user} 没有借阅《{book_title}》")
        return False

    def show_books(self):
        """显示所有图书"""
        print(f"\n=== {self.name} 图书列表 ===")
        for book in self.books:
            print(f"{book} - 可借阅: {book.available_copies}/{book.total_copies}")

    def show_user_books(self, user):
        """显示用户借阅的书"""
        if user in self.borrowed_books and self.borrowed_books[user]:
            print(f"\n=== {user} 的借阅记录 ===")
            for book in self.borrowed_books[user]:
                print(f"  {book}")
        else:
            print(f"{user} 没有借阅任何图书")

# 测试图书管理系统
library = Library("市图书馆")

# 添加图书
book1 = Book("Python编程", "张三", "978-1234567890", 3)
book2 = Book("数据结构", "李四", "978-0987654321", 2)
book3 = Book("算法导论", "王五", "978-1122334455", 1)

library.add_book(book1)
library.add_book(book2)
library.add_book(book3)

library.show_books()

# 借书和还书
library.borrow_book("小明", "Python编程")
library.borrow_book("小红", "Python编程")
library.borrow_book("小明", "数据结构")

library.show_books()
library.show_user_books("小明")

library.return_book("小明", "Python编程")
library.show_books()

print("\n" + "=" * 50)
print("练习完成！")
print("=" * 50)
print("""
🎉 恭喜你完成了所有练习！

通过这些练习，你应该掌握了：
1. 基本的类定义和实例化
2. 构造函数 __init__ 的使用
3. 实例方法和属性的定义
4. 类的继承和方法重写
5. 私有属性的使用
6. 特殊方法的实现
7. 实际项目中类的应用

继续练习建议：
- 尝试修改这些类，添加新的功能
- 创建更复杂的继承关系
- 实现更多的特殊方法
- 结合异常处理让代码更健壮

加油！你已经在Python面向对象编程的路上了！
""")
