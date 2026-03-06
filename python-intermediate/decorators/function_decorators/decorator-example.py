def add_five(num):
    def add_two(num):
        return num + 2
    
    num_plus_two = add_two(num) # num is passed to outter function
    print(num_plus_two + 3)
    print(f"\n Inside nested function: {locals()}\n")
#add_five(10)

def get_math_function(operation):

    def add(n1, n2):
        return n1 + n2

    def subtract(n1, n2):
        return n1 - n2

    def divide(n1, n2):
        return n1 / n2

    def multiply(n1, n2):
        return n1 * n2

    operations = {
        "+": add,
        "-": subtract,
        "/": divide,
        "*": multiply
    }

    return operations.get(operation)

sum1 = get_math_function('*')
print(sum1(30, 98))