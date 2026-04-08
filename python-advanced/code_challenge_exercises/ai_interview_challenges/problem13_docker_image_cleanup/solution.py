import json
from pprint import pprint


# 1)

def analyze_docker_images(images_file_path: str, running_image_ids_path: str, stale_threshold_days: int = 30) -> dict:
    
    # 2)
    results = {
    "repository_counts": {},
    "tag_state_counts": {},
    "largest_unused_image": None,
    "cleanup_candidates": {},
    "oldest_unused_created_at": None,
    "average_size_mb_unused": None,
    }

    # 3)
    in_use_image_ids = set()
    unused_image_sizes = {}
    unused_created_at_values = []
    unused_size_total = 0
    unused_size_count = 0

    
    try:
        # 4 A)
        with open(running_image_ids_path, 'r') as ids_file:
            for line in ids_file:
                line = line.strip()
                if not line:
                    continue
                in_use_image_ids.add(line)

        # 4 B)
        with open(images_file_path, 'r') as images_file:
            # 4 C)
            for line in images_file:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except ValueError:
                    continue

                # 5 A)
                image_id = data.get("image_id")
                repository = data.get("repository")
                tag = data.get("tag")
                size_mb = data.get("size_mb")
                created_at = data.get("created_at")
                age_days = data.get("age_days")

                # 5 B)
                if not all((
                    image_id,
                    repository,
                    tag, 
                    created_at
                )):
                    continue
                
                # 5 C1)
                results["repository_counts"][repository] = results["repository_counts"].get(repository, 0) + 1
                
                # 5 C2)
                if tag == "latest":
                    tag_state = "latest"
                elif tag == "<none>":
                    tag_state = "dangling"
                else:
                    tag_state = "versioned"

                # 5 C3)
                results["tag_state_counts"][tag_state] = results["tag_state_counts"].get(tag_state, 0) + 1
                
                # 6 A)
                if image_id not in in_use_image_ids:
                    if isinstance(size_mb, int) or isinstance(size_mb, float):
                        unused_image_sizes[image_id] = size_mb
                        unused_size_total += size_mb
                        unused_size_count += 1

                    # 6 B)
                    unused_created_at_values.append(created_at)
                    
                    # 6 C)
                    if tag == "<none>" or (isinstance(age_days, int) and age_days >= stale_threshold_days):
                        if isinstance(size_mb, int) or isinstance(size_mb, float):
                            results["cleanup_candidates"][image_id] = {"size_mb": size_mb}
    except FileNotFoundError:
        return results
    
    # 7) FINAL COMPUTATION RULES

    # 7 A)
    if unused_image_sizes:
        largest_size_mb = max(unused_image_sizes.values())
        results["largest_unused_image"] = min([
            image_id_value
            for image_id_value in unused_image_sizes
            if unused_image_sizes[image_id_value] == largest_size_mb
        ])

    # 7 B)
    if unused_created_at_values:
        results["oldest_unused_created_at"] = min(unused_created_at_values)
    
    # 7 C)
    if unused_size_count > 0:
        average_size_mb = unused_size_total / unused_size_count
        results["average_size_mb_unused"] = round(average_size_mb, 2)
    
    # 8)
    return results

if __name__ == "__main__":
    in_use_file_path = "docker_images.jsonl"
    images_file_path = "running_image_ids.txt"
    result = analyze_docker_images(in_use_file_path, images_file_path)
    pprint(result)
