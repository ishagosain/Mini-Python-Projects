def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Test it
numbers = [2, 4, 17, 18, 23, 100]
for num in numbers:
    print(f"{num} is prime: {is_prime(num)}")
