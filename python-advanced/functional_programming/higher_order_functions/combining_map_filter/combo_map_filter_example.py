# combining map&filter
def double_greater_than_10(nums):
    """
    we can combine the map() and filter() functions.

    Conceptually, if you’re working with a collection of items and find yourself saying, 
    “I need to map only values that have property x,” you will likely need to use map() and filter() together. in English, “
    I need to map filtered values” translates into Python like this:

        map(mapping_function, filter(predicate, iterable))
    """
    # map(mapping_function, filter(predicate, iterable))
    greater_than_10_doubled = map(lambda x: x * 2, filter(lambda x: x > 10, nums))
    return tuple(greater_than_10_doubled)

# call function
nums = (2, 12, 5, 8, 9, 3, 16, 7, 13, 19, 21, 1, 15, 4, 22, 20, 11)
# result = double_greater_than_10(nums)
# print(result)

#### Alternative (more Pythonic) using a generator expression: ####

def double_greater_than_10(nums):
    return tuple(x * 2 for x in nums if x > 10)

# return a tuple
def functional_way(nums):
  return tuple(i * 3 for i in nums if i % 3 == 0)

# return a list
def functional_way_lst(nums):
  return [i * 3 for i in nums if i % 3 == 0]

result_lst = functional_way_lst(nums)
result_tup = functional_way(nums)
print(f"\nReturned as a list: =====> {result_lst}")
print(f"Returned as a tuple: ======>  {result_tup}\n")

