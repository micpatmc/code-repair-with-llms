def calculate(expression):
    result = eval(expression)
    return result

user_input = input("Enter a mathematical expression to evaluate: ")
print("Result:", calculate(user_input))
