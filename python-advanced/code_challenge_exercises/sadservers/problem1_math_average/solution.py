

def find_average(file_path: str) -> float:
    with open(file_path, 'r') as file:
        nums = [float(line.split()[1]) for line in file if line.strip()]
        avg = round(sum(nums) / len(nums), 2)
    
    with open("answer.txt", 'w') as file:
        file.write(str(avg))



result = find_average("scores.txt")
print(result) # 5.20