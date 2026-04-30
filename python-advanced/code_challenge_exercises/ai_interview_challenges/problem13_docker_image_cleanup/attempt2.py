import json


def analyze_docker_images(images_file_path: str, running_image_ids_path: str, stale_threshold_days: int = 30) -> dict:
    results = {
    "repository_counts": {},
    "tag_state_counts": {},
    "largest_unused_image": None,
    "cleanup_candidates": {},
    "oldest_unused_created_at": None,
    "average_size_mb_unused": None,
    }

    in_use_image_ids = set()
    unused_image_sizes = {}
    unused_created_at_values = []
    unused_size_total = 0
    unused_size_count = 0

    try:
        with open(running_image_ids_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                in_use_image_ids.add(line)


        with open(images_file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except ValueError:
                    continue
                
                image_id = data.get("image_id")
                repository = data.get("repository")
                tag = data.get("tag")
                size_mb = data.get("size_mb")
                created_at = data.get("created_at")
                age_days = data.get("age_days")
                if not image_id or not repository or not tag or not created_at:
                    continue

                results["repository_counts"][repository] = results["repository_counts"].get(repository, 0) + 1

                if tag == "latest":
                    tag_state = "latest"
                else:
                    if tag == "<none>":
                        tag_state = "dangling"
                    else:
                        tag_state = "versioned"

                results["tag_state_counts"][tag_state] = results["tag_state_counts"].get(tag_state, 0) + 1

                if image_id not in in_use_image_ids:
                    if isinstance(size_mb, (int, float)):
                        unused_image_sizes[image_id] = size_mb
                        unused_size_total += size_mb
                        unused_size_count += 1
                
                unused_created_at_values.append(created_at)
                if tag == "<none>" or isinstance(age_days, int) and age_days >= stale_threshold_days:
                    if isinstance(size_mb, (int, float)):
                        results["cleanup_candidates"][image_id] = size_mb
                    
    except FileNotFoundError:
        print(f"The files {images_file_path} or {running_image_ids_path} does not exist or can't be found")
        return results
    
    if unused_image_sizes:
        largest_size_mb = max(unused_image_sizes.values())
        largest_image_candidates = []
        for image_id_value in unused_image_sizes:
            if unused_image_sizes[image_id_value] == largest_size_mb:
                largest_image_candidates.append(image_id_value)
        results["largest_unused_image"] = min(largest_image_candidates)

    if unused_created_at_values:
        results["oldest_unused_created_at"] = min(sorted(unused_created_at_values))
    
    if unused_size_count > 0:
        average_size_mb = unused_size_total / unused_size_count
        results["average_size_mb_unused"] = round(average_size_mb, 2)

    return results

if __name__ == "__main__":
    in_use_file_path = "docker_images.jsonl"
    images_file_path = "running_image_ids.txt"
    result = analyze_docker_images(in_use_file_path, images_file_path)
    print(json.dumps(result, indent=4))