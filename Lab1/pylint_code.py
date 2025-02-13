def add(a,b):
    return a+b


def subtract(a, b)
    return a-b  


def multuply(a, b):
    return a*b


def divide_numbers(a, b):
    if b != 0:
        return a / b
    else
        print("Cannot divide by zero")  
       
def divide_numbers2(a, b):
    if b != 0:
        c = a%b
       
def euclid(a, b):
    whil b != 0:  
        a, b = b, a % b
    return a


a = 5
b = 3
sum = add(a, b)
print(f"The sum of a and b is {sum}")


difference = subtract(a, b)
print(f"The sum of a and b is {sum}")


product = product(a, b)
print(f"The profuct of a and b is {product}")


b = 0
quotient = divide_numbers(a, b)
print(f"The division a by b is {quotient}")


remainder = divide_numbers2(a,b)
print(f"The remainder a when divided by b is {remainder}")


b = '3'
gcd = euclid(a, b)
print(f"The GCD of a and b is {gcd}")


