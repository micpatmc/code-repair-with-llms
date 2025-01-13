def fibonacci_iterative(n):
    """Calculate nth Fibonacci number using iteration (more memory efficient)."""
    if n <= 0:
        return "Please enter a positive integer"
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    
    a, b = 0, 1
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b

def fibonacci_sequence(n):
    """Generate the Fibonacci sequence up to the nth number using iteration."""
    if n <= 0:
        return "Please enter a positive integer"
    
    sequence = []
    a, b = 0, 1
    
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    
    return sequence

def fibonacci_recursive(n):
    """Calculate nth Fibonacci number using recursion (not recommended for large n)."""
    if n <= 0:
        return "Please enter a positive integer"
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

def main():
    while True:
        try:
            n = int(input("Enter a positive number (or 0 to exit): "))
            if n == 0:
                print("Exiting program...")
                break
            
            if n < 0:
                print("Please enter a positive number")
                continue
            
            # Get single Fibonacci number
            print(f"\nThe {n}th Fibonacci number is: {fibonacci_iterative(n)}")
            
            # Get full sequence
            sequence = fibonacci_sequence(n)
            print(f"\nFibonacci sequence up to {n} numbers:")
            print(sequence)
            
        except ValueError:
            print("Please enter a valid number")

if __name__ == "__main__":
    main()
