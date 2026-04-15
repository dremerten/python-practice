import json


def find_highest_ip_count(file_path: str) -> dict:
    counts = {}

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split()
                ip = parts[0]

                counts[ip] = counts.get(ip, 0) + 1

    except FileNotFoundError:
        print(f"The File {file_path} can't be found or does not exist")

    max_ip = max(counts, key=counts.get)
    max_count = counts[max_ip]

    return {
        "IP": max_ip,
        "Count": max_count
    }


if __name__ == "__main__":
    result = find_highest_ip_count("access.log")

    with open("highestip.txt", 'w') as file:
        file.write(result["IP"])

    print(json.dumps(result, indent=4))