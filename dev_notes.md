# 开发记录

## Python的特殊变量

- 以双下划线开头，已字符结尾的变量、函数是私有函数，只有类自身能访问，比如 `__func_a()`、`__var_a`，为了防止被直接访问，Python 使用命名映射，将 `__X` 映射成 `_classname__X` 。这样无论变量还是函数都可以通过 `instance._calssname__X` 这样的形式来访问 `__X`
- 以单下划线开头的变量、函数称为保护数据，意思是这些变量只给实例自身和子类访问，不能 被其他模块通过 `import` 访问到。
- 以双下划线开头和结尾的变量，是系统定义的的函数，有其特殊意义，比如 `__init__()` 标识类的构造函数。

## MongoClient 与多进程的冲突

MongoClient不能通过父进程共享给子进程，每个子进程都要创建自己的MongoClient。由于MongoClient内部机制，即使父进程使用MongoClient也要在自己成创建完毕后再在父进程中创建MongoClient，否则会抛出异常`MongoClient opened before fork. Create MongoClient only` 。同时，要将创建连接的参数` connect=False`。

## PyCharm 中运行代码，Click与系统编码不兼容问题
