# list of strings
str_nums = [str(i) for i in range(100)]

# Convert strings to ints
int_nums = list(map(int, str_nums)) 

print(str_nums)
print("")
print("Converted strings to ints!\n")
print(int_nums)
