import math

def check_number_sign(number):
    if number > 0:
        return "Positive"
    elif number < 0:
        return "Negative"
    else:
        return "Zero"

def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def get_first_n_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    print(f"The first {n} prime numbers are: {primes}")
    return primes

def sum_with_while_loop(limit):
    current_number = 1
    total_sum = 0
    while current_number <= limit:
        total_sum += current_number
        current_number += 1
    return total_sum

if __name__ == "__main__":
    print(f"\nChecking number signs:")
    print(f"The number 5 is: {check_number_sign(5)}")
    print(f"The number -3 is: {check_number_sign(-3)}")
    print(f"The number 0 is: {check_number_sign(0)}")

    print(f"\nFinding the first 10 prime numbers:")
    first_10_primes = get_first_n_primes(10)

    print(f"\nSumming numbers from 1 to 100:")
    sum_1_to_100 = sum_with_while_loop(100)
    print(f"The sum of numbers from 1 to 100 is: {sum_1_to_100}")
