# 🐍 Python OOP — Complete Notes
> **Author:** Bharath Nandipati
>  **Topic:** Object-Oriented Programming in Python  
> **Level:** Beginner → Intermediate  
> **Last Updated:** 2026

---

## 📚 Table of Contents

1. [Memory: Stack vs Heap](#-memory--stack-vs-heap)
2. [What is a Class?](#-what-is-a-class)
3. [What is an Object?](#-what-is-an-object)
4. [How Variables Are Stored (Memory Deep Dive)](#-how-variables-are-stored-memory-deep-dive)
5. [What is a Constructor?](#-what-is-a-constructor)
6. [Non-Parametrized Constructor](#-non-parametrized-constructor)
7. [Parametrized Constructor](#-parametrized-constructor)
8. [The `self` Keyword](#-the-self-keyword)
9. [Real-World Full Example](#-real-world-full-example)
10. [Quick Summary Table](#-quick-summary-table)
11. [Key Reminders / Gotchas](#-key-reminders--gotchas)

---

## 🧠 Memory — Stack vs Heap

Before learning OOP, it is critical to understand **where things live in memory**.

Python uses two memory regions:

```
┌─────────────────────────────────┐     ┌─────────────────────────────────────┐
│            STACK                │     │               HEAP                  │
│─────────────────────────────────│     │─────────────────────────────────────│
│  - Fixed size, Fast             │     │  - Dynamic size, Slightly slower    │
│  - Stores local variables       │     │  - Stores actual OBJECTS & DATA     │
│  - Stores REFERENCES (pointers) │────▶│  - Managed by Python's GC           │
│  - Automatically cleaned up     │     │  - Lives as long as referenced      │
│  - Function call frames live    │     │  - All class instances go here      │
│    here                         │     │                                     │
└─────────────────────────────────┘     └─────────────────────────────────────┘
```

### 🔑 Golden Rule

| What | Where Stored |
|---|---|
| Variable **name** (reference/pointer) | **Stack** |
| Actual **object / data** (value) | **Heap** |
| **Primitive-like** (int, float, str, bool) | **Heap** (Python wraps everything as objects) |
| **Function call frame** | **Stack** |
| **Class instance** | **Heap** |

### Example — Stack and Heap in Action

```python
x = 10          # 'x' is on Stack, integer object 10 is on Heap
name = "Alice"  # 'name' is on Stack, string object "Alice" is on Heap

class Dog:
    def __init__(self, name):
        self.name = name

dog1 = Dog("Bruno")  # 'dog1' reference is on Stack
                     #  Dog object {name: "Bruno"} lives on Heap
```

```
STACK                          HEAP
┌──────────────┐             ┌──────────────────────┐
│  x  ─────────┼────────────▶│  int object: 10      │
│  name ───────┼────────────▶│  str object: "Alice" │
│  dog1 ───────┼────────────▶│  Dog object          │
│              │             │   └─ name: "Bruno"   │
└──────────────┘             └──────────────────────┘
```

### What Happens When Two Variables Point to Same Object?

```python
a = [1, 2, 3]
b = a             # b does NOT copy the list, it copies the REFERENCE

b.append(4)

print(a)   # [1, 2, 3, 4]  ← a is also changed! Both point to same Heap object
print(b)   # [1, 2, 3, 4]
```

```
STACK                          HEAP
┌──────────────┐             ┌──────────────────────┐
│  a  ─────────┼──────┐      │  list: [1, 2, 3, 4]  │
│  b  ─────────┼──────┘─────▶│                      │
└──────────────┘             └──────────────────────┘
```

> ⚠️ This is called a **Shallow Copy** problem. Use `b = a.copy()` to create a separate object on Heap.

### Python's Memory Manager & Garbage Collector

```
Object created on Heap ──▶ Python tracks reference count
                            │
                     count > 0 ──▶ Object stays alive
                            │
                     count == 0 ──▶ Garbage Collector deletes it from Heap
```

```python
dog1 = Dog("Bruno")   # reference count of Dog object = 1
dog2 = dog1           # reference count = 2
dog1 = None           # reference count = 1
dog2 = None           # reference count = 0 → GC deletes from Heap 🗑️
```

---

## 🏛️ What is a Class?

A **class** is a **blueprint / template** used to create objects. It defines:
- **Attributes** → Data / Properties (what the object *has*)
- **Methods** → Functions / Behaviors (what the object *does*)

> 💡 Analogy: Class = **Architect's Blueprint**, Object = **Actual Building**

```python
class Car:              # Class definition (Blueprint)
    brand = "Toyota"    # Class Attribute (shared by ALL objects)
    color = "Red"

    def drive(self):    # Method (behavior)
        print("Car is driving...")
```

### Class Syntax Structure

```
class ClassName:
    │
    ├── Class Variables      → Shared across all objects
    │
    ├── __init__()           → Constructor (runs when object is created)
    │
    └── Methods              → Behaviors / Functions of the object
```

---

## 🚗 What is an Object?

An **object** is a **real instance** created from a class. Each object:
- Has its **own copy of instance variables** (stored on Heap)
- Shares **class variables and methods** (stored once, referenced)
- Has a **unique memory address** on the Heap

```python
class Car:
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color

    def drive(self):
        print(f"{self.brand} ({self.color}) is driving!")

# Creating Objects
car1 = Car("Toyota", "Red")    # Object 1 on Heap
car2 = Car("BMW", "Black")     # Object 2 on Heap (separate memory)

car1.drive()   # Toyota (Red) is driving!
car2.drive()   # BMW (Black) is driving!

# Each object has a unique identity
print(id(car1))   # e.g. 140234567890
print(id(car2))   # e.g. 140234567920  ← Different address on Heap
```

---

## 🔬 How Variables Are Stored (Memory Deep Dive)

### Instance Variables vs Class Variables

```python
class Student:
    school = "ABC School"       # Class Variable  → stored ONCE on Heap (shared)

    def __init__(self, name, age):
        self.name = name        # Instance Variable → each object gets its OWN copy on Heap
        self.age  = age         # Instance Variable → each object gets its OWN copy on Heap


s1 = Student("Alice", 20)
s2 = Student("Bob", 22)
```

```
HEAP MEMORY

┌─────────────────────────────────────────────────────┐
│  Student CLASS object                               │
│   └── school = "ABC School"  (shared, stored once) │
├─────────────────────────────────────────────────────┤
│  s1 Object (Student instance)                       │
│   ├── name = "Alice"                                │
│   └── age  = 20                                     │
├─────────────────────────────────────────────────────┤
│  s2 Object (Student instance)                       │
│   ├── name = "Bob"                                  │
│   └── age  = 22                                     │
└─────────────────────────────────────────────────────┘
```

```
STACK MEMORY

┌──────────────┐
│  s1 ─────────┼──────▶ points to s1's Heap block
│  s2 ─────────┼──────▶ points to s2's Heap block
└──────────────┘
```

### What Happens During a Method Call?

```python
s1.display()
```

```
STACK (during method call)            HEAP
┌──────────────────────────┐        ┌────────────────────┐
│  display() call frame    │        │  s1 Object         │
│   └── self ──────────────┼───────▶│   name = "Alice"   │
│                          │        │   age  = 20         │
└──────────────────────────┘        └────────────────────┘
         ↑ Frame is popped from Stack after method finishes
```

> `self` is just a local variable in the Stack that **holds the reference** (address) to the object on the Heap.

---

## 🏗️ What is a Constructor?

A **constructor** is a **special method** that is **automatically called** the moment an object is created.

- In Python, constructor = `__init__()` method
- The **double underscores** (`__`) = "dunder" = magic/special method
- Used to **initialize** the object's attributes

```
Dog("Bruno")  is called
       │
       ▼
Python creates empty Dog object on Heap
       │
       ▼
__init__(self, "Bruno") is automatically called
       │
       ▼
self.name = "Bruno" is set on the object
       │
       ▼
Object is fully ready ✅
```

```python
class Dog:
    def __init__(self):
        print(f"🐶 New Dog object created! ID: {id(self)}")

d1 = Dog()   # __init__ fires automatically
d2 = Dog()   # __init__ fires again for new object
```

---

## 🔧 Non-Parametrized Constructor

A **non-parametrized constructor** takes **only `self`** — no extra arguments.
Every object created from this class gets the **same default values**.

```python
class Student:

    def __init__(self):                      # Non-Parametrized
        self.name   = "Unknown"              # Default value
        self.age    = 0                      # Default value
        self.grade  = "Not Assigned"         # Default value
        print("📌 Student object created with defaults!")

    def display(self):
        print(f"Name: {self.name} | Age: {self.age} | Grade: {self.grade}")


s1 = Student()
s2 = Student()

s1.display()   # Name: Unknown | Age: 0 | Grade: Not Assigned
s2.display()   # Name: Unknown | Age: 0 | Grade: Not Assigned

# You CAN change values manually after creation
s1.name = "Alice"
s1.display()   # Name: Alice | Age: 0 | Grade: Not Assigned
```

### Memory View

```
HEAP
┌────────────────────────────────┐
│  s1 Object                     │
│   ├── name  = "Unknown"        │  ← same defaults
│   ├── age   = 0                │
│   └── grade = "Not Assigned"   │
├────────────────────────────────┤
│  s2 Object                     │
│   ├── name  = "Unknown"        │  ← same defaults
│   ├── age   = 0                │
│   └── grade = "Not Assigned"   │
└────────────────────────────────┘
```

> ⚠️ **Limitation:** Not flexible. All objects start with identical data.

---

## ✅ Parametrized Constructor

A **parametrized constructor** takes **custom arguments** so each object can have its **own unique data** from the moment it's created.

```python
class Student:

    def __init__(self, name, age, grade):    # Parametrized Constructor
        self.name  = name
        self.age   = age
        self.grade = grade

    def display(self):
        print(f"👤 Name: {self.name} | Age: {self.age} | Grade: {self.grade}")


s1 = Student("Alice",   20, "A")
s2 = Student("Bob",     22, "B")
s3 = Student("Charlie", 19, "A+")

s1.display()   # 👤 Name: Alice   | Age: 20 | Grade: A
s2.display()   # 👤 Name: Bob     | Age: 22 | Grade: B
s3.display()   # 👤 Name: Charlie | Age: 19 | Grade: A+
```

### With Default Parameter Values

```python
class Student:
    def __init__(self, name, age, grade="Not Assigned"):   # grade has a default
        self.name  = name
        self.age   = age
        self.grade = grade

s1 = Student("Alice", 20, "A")   # grade = "A"
s2 = Student("Bob", 22)          # grade = "Not Assigned" (default used)
```

### Memory View

```
HEAP
┌────────────────────────────────┐
│  s1 Object                     │
│   ├── name  = "Alice"          │  ← unique data
│   ├── age   = 20               │
│   └── grade = "A"              │
├────────────────────────────────┤
│  s2 Object                     │
│   ├── name  = "Bob"            │  ← unique data
│   ├── age   = 22               │
│   └── grade = "B"              │
└────────────────────────────────┘
```

### Non-Parametrized vs Parametrized — Comparison

| Feature | Non-Parametrized | Parametrized |
|---|---|---|
| Arguments | Only `self` | `self` + custom args |
| Flexibility | ❌ Low — same defaults | ✅ High — unique per object |
| Use Case | When all objects share defaults | When each object needs unique data |
| Real-world use | Rare | Very Common |

---

## 🔑 The `self` Keyword

`self` is a **reference variable** that points to the **current object** (the one that called the method).

- It is **always the first parameter** of any instance method
- Python automatically passes the calling object as `self`
- The name `self` is a **convention**, not a keyword (you could name it anything, but NEVER do that)

```python
class Dog:

    def __init__(self, name, breed):
        self.name  = name    # self = the specific Dog object being created
        self.breed = breed

    def bark(self):
        print(f"{self.name} ({self.breed}) says: Woof! 🐶")


dog1 = Dog("Bruno", "Labrador")
dog2 = Dog("Max", "Poodle")

dog1.bark()   # Python internally calls Dog.bark(dog1)
dog2.bark()   # Python internally calls Dog.bark(dog2)
```

### How Python Translates `self`

```python
dog1.bark()
# Python internally rewrites this as:
Dog.bark(dog1)   # dog1 is passed as 'self'
```

```
STACK                              HEAP
┌─────────────────────────┐      ┌──────────────────────────┐
│  bark() call frame      │      │  dog1 Object             │
│   └── self (address) ───┼─────▶│   ├── name  = "Bruno"    │
│                         │      │   └── breed = "Labrador"  │
└─────────────────────────┘      └──────────────────────────┘
```

### Why `self` is Critical — Without It, Chaos!

```python
class Counter:
    count = 0              # Class variable (shared — DANGEROUS without self)

    def increment_wrong(self):
        count += 1         # ❌ Error! Python doesn't know WHICH count

    def increment_right(self):
        self.count += 1    # ✅ Refers to THIS object's count

c1 = Counter()
c2 = Counter()

c1.increment_right()
c1.increment_right()
c2.increment_right()

print(c1.count)   # 2  ✅ c1 has its own count
print(c2.count)   # 1  ✅ c2 has its own count
```

### `self` in Memory

```
HEAP

┌─────────────────────────────────────────────┐
│  c1 Object         c2 Object               │
│   └── count = 2     └── count = 1          │
│                                             │
│   self inside c1's method ──▶ points to c1 │
│   self inside c2's method ──▶ points to c2 │
└─────────────────────────────────────────────┘
```

---

## 🏦 Real-World Full Example

```python
class BankAccount:

    bank_name = "Python National Bank"     # Class Variable (shared)

    def __init__(self, owner, account_no, balance=0):    # Parametrized Constructor
        self.owner      = owner            # Instance Variable → Heap
        self.account_no = account_no       # Instance Variable → Heap
        self.balance    = balance          # Instance Variable → Heap
        print(f"✅ Account created for {self.owner} at {self.bank_name}")

    def deposit(self, amount):
        if amount <= 0:
            print("❌ Deposit amount must be positive!")
            return
        self.balance += amount
        print(f"💰 Deposited ₹{amount}. New Balance: ₹{self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print(f"❌ Insufficient funds! Available: ₹{self.balance}")
        else:
            self.balance -= amount
            print(f"💸 Withdrawn ₹{amount}. New Balance: ₹{self.balance}")

    def show(self):
        print(f"""
        ┌─────────────────────────────┐
        │  Bank: {self.bank_name}
        │  Owner: {self.owner}
        │  Account No: {self.account_no}
        │  Balance: ₹{self.balance}
        └─────────────────────────────┘
        """)


# Each account is a separate object with its OWN memory on Heap
acc1 = BankAccount("Alice", "ACC001", 10000)
acc2 = BankAccount("Bob",   "ACC002", 5000)

acc1.deposit(2000)
acc2.withdraw(1000)
acc2.withdraw(9000)   # Should fail

acc1.show()
acc2.show()
```

### Memory Layout for Above Example

```
STACK                          HEAP
┌──────────────┐             ┌──────────────────────────────────────┐
│  acc1 ───────┼────────────▶│  BankAccount Object #1               │
│              │             │   ├── owner      = "Alice"           │
│              │             │   ├── account_no = "ACC001"          │
│              │             │   └── balance    = 12000             │
│              │             ├──────────────────────────────────────┤
│  acc2 ───────┼────────────▶│  BankAccount Object #2               │
│              │             │   ├── owner      = "Bob"             │
│              │             │   ├── account_no = "ACC002"          │
│              │             │   └── balance    = 4000              │
│              │             ├──────────────────────────────────────┤
│              │             │  BankAccount CLASS                   │
│              │             │   └── bank_name = "Python National   │
│              │             │                    Bank" (shared)    │
└──────────────┘             └──────────────────────────────────────┘
```

---

## 📊 Quick Summary Table

| Concept | What it is | Syntax | Memory Location |
|---|---|---|---|
| **Class** | Blueprint / Template | `class MyClass:` | Heap (class object) |
| **Object** | Instance of a class | `obj = MyClass()` | Heap |
| **Reference** | Variable pointing to object | `obj` | Stack |
| **Constructor** | Auto-called init method | `def __init__(self):` | Stack (call frame) |
| **Non-Parametrized** | Constructor, no custom args | `def __init__(self):` | — |
| **Parametrized** | Constructor with custom args | `def __init__(self, x):` | — |
| **self** | Reference to current object | First param of every method | Stack (holds Heap address) |
| **Instance Variable** | Unique data per object | `self.name = name` | Heap (inside object) |
| **Class Variable** | Shared across all objects | `class_var = value` | Heap (inside class object) |

---

## ⚡ Key Reminders & Gotchas

```
✅ DO's
───────────────────────────────────────────────────────
✔ Always use 'self' as the first parameter in instance methods
✔ Use parametrized constructor for real-world objects
✔ Use class variables only for data truly shared across ALL objects
✔ Use .copy() when you want a separate object, not a shared reference
✔ Remember: variable name (Stack) ──▶ object data (Heap)

❌ DON'Ts
───────────────────────────────────────────────────────
✘ Don't rename 'self' (technically allowed but never do it)
✘ Don't confuse class variables with instance variables
✘ Don't assume two variables are different objects just because they have different names
✘ Don't forget: Python wraps EVERYTHING as objects on the Heap
```

---

## 🔮 What's Next? (OOP Pillars)

```
OOP in Python
│
├── ✅ Class & Object          ← You are here
├── ✅ Constructor & self      ← You are here
│
├── 🔜 Encapsulation          → Hiding internal data (private, protected)
├── 🔜 Inheritance            → Child class reusing Parent class
├── 🔜 Polymorphism           → Same method, different behavior
└── 🔜 Abstraction            → Hiding complexity, showing only essentials
```

---

*📌 Keep this file handy for revision. Happy Coding! 🐍🚀*
