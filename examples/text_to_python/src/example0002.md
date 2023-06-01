# description

```
These are the assertions for your function:

assert heap_queue_largest([25, 35, 22, 85, 14, 65, 75, 22, 58], 3) == [85, 75, 65]

Write a function to find the largest integers from a given list of numbers using heap queue algorithm.
```

# code

```
import heapq as hq
def heap_queue_largest(nums,n):
    largest_nums = hq.nlargest(n, nums)
    return largest_nums
```