import json 


def most_frequent_ip(file_path: str) -> dict:
    counts = {}

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                line_parts = line.strip().split()
                ip = line_parts[0].strip()
                counts[ip] = counts.get(ip, 0) + 1
                
    except FileNotFoundError:
        return count

    max_ip = max(counts, key=counts.get)
    max_count = counts[max_ip]

    result = {
        "IP": max_ip,
        "COUNT": max_count
    }

    with open("highestip2.txt", 'w') as file:
        file.write(result["IP"])

result = most_frequent_ip("access.log")
