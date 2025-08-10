import os
import json
import random

input_folder = ''  # Path to the folder containing processed JSON files
output_folder = ''  # Path to the folder where the randomly sampled tweets will be saved
random_seed = 42


# Read all lines from a processed JSON file containing tweets and parse them into a list of JSON objects
def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        json_objects = [json.loads(line) for line in lines]
    return json_objects


# Save the randomly sampled JSON objects to a specific output file
def save_sampled_objects(sampled_objects, output_filename):
    output_path = os.path.join(output_folder, output_filename)
    with open(output_path, 'w', encoding='utf-8') as file:
        for obj in sampled_objects:
            file.write(json.dumps(obj) + '\n')


# Randomly sample tweets from each JSON file
def random_sample_tweets(files, random_seed=42):
    total_sampled = 0
    random.seed(random_seed)

    for file in files:
        json_objects = read_file(file)
        num_objects = len(json_objects)
        if int(num_objects * 0.1) > 500:
            sample = random.sample(json_objects, int(num_objects * 0.1))
        else:
            if num_objects >= 500:
                sample = random.sample(json_objects, 500)
            else:
                sample = json_objects

        if len(sample) > 0:
            output_filename = f"{os.path.basename(file)}"
            print(f"{os.path.basename(file)}, Total: {num_objects}, Sampled: {len(sample)}")
            save_sampled_objects(sample, output_filename)
            total_sampled += len(sample)

    print(str(total_sampled))


def main():
    os.makedirs(output_folder, exist_ok=True)
    files_path = [
        os.path.join(input_folder, file)
        for file in os.listdir(input_folder)
        if file.endswith('.json')
    ]
    random_sample_tweets(files_path)


if __name__ == "__main__":
    main()

