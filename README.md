# SoCo-Lab2
Objective In this assignment you will extend the Little German Language (LGL) interpreter by adding support for infix and boolean expressions, lexical scoping, and tracing

## Step 02 设计文档
### 设计思路
1. 修改环境操作：修改 do_setzen 和 do_bekommen 函数。

2. 添加函数定义和调用：添加处理函数定义和函数调用的操作。

3. 修改主执行函数：修改 do 函数，以便它能够正确地处理函数定义和函数调用。
### 测试思路
用lgl写出文档中类似的测试代码，详见example_scoping.gsc。
```python
x = 100

function one():
    print(x)
    
function two():
    x = 42
    one()
    
function main():
    two()
    
main()
```
如果是dynamic scoping输出42，如果是lexical scoping输出100。
