# description

```
These are the assertions for your function:

assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)

Write a function to find the similar elements from the given two tuple lists.
```

# code

```
def similar_elements(test_tup1, test_tup2):
    res = tuple(set(test_tup1) &amp; set(test_tup2))
    return res
```