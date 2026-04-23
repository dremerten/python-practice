

def avg_score(file_path: str) -> float:
    
    try:
        with open(file_path, 'r') as file:
            nums = [float(line.split()[1]) for line in file if line.strip()]
            avg = sum(nums) / len(nums)

        with open("answer.txt", 'w') as file:
            file.write(str(f"{avg:.2f}"))
            
    except FileNotFoundError:
        print(f"The file {file_path} can't be found or does not exist")

    return avg

result = avg_score("scores.txt")
print(f"The avg score is {result:.2f}")