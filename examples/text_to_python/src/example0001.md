# description

```
These are the assertions for your function:

assert is_not_prime(2) == False

Write a python function to identify non-prime numbers.
```

# code

```
import math
def is_not_prime(n):
    result = False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
        result = True
    return result
```