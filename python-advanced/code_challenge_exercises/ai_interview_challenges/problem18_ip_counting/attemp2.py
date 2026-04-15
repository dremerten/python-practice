import json



def highest_count(file_path: str) -> dict:
    counts = {}

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split()
                ip_address = parts[0].strip()
                counts[ip_address] = counts.get(ip_address, 0) + 1
            
    except FileNotFoundError:
        print(f"The file {file_path} can't be found or does not exist")

    winning_ip = max(counts, key=counts.get)
    highest_count = counts[winning_ip]
    
    return {
        "Highest IP": winning_ip,
        "Highest Count": highest_count
    }


if __name__ == "__main__":
    results = highest_count("access.log")
    print(json.dumps(results, indent=4))