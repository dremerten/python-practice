import json


def highest_ip_count(file_path: str):
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
        print(f"The file {file_path} can't be found or does not exist")
        return None, None

    # find the IP with the highest count
    max_ip = None
    max_count = 0

    for ip, count in counts.items():
        if count > max_count:
            max_ip = ip
            max_count = count

    #print (f"IP with highest count is: {max_ip}, {max_count}")
    return max_ip, max_count

if __name__ == "__main__":
    ip, count = highest_ip_count("access.log")

    if ip is not None:
        # optional sanity check
        print(f"Top IP: {ip}, Count: {count}")

        # write result to file
        with open("highestip.txt", "w") as f:
            f.write(ip + "\n")