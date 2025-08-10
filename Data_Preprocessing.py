import json
import re
import os


# Step 1: Filter out tweets where the word count is less than 3
def preprocess_step1(data):
    processed_data_step1 = []
    removed_ids_step1 = []

    for json_obj in data:
        text = json_obj.get("text", "")
        obj_id = json_obj.get("id", None)  # Get the object ID

        # Count the number of words
        word_count = len(text.split())

        # If word count is less than 3, record the removed ID
        if word_count < 3:
            if obj_id is not None:
                removed_ids_step1.append(obj_id)
        else:
            processed_data_step1.append(json_obj)

    return processed_data_step1, removed_ids_step1


# Step 2: Remove 're:' prefix, URLs, and perform deduplication based on processed text.
def preprocess_step2(data):
    processed_data_step2 = []
    removed_ids_step2 = []
    seen_texts = set()
    for i, obj in enumerate(data):
        original_text = obj.get("text", "")
        obj_id = obj.get("id", None)

        processed_text = re.sub(r'^re:\s*', '', original_text, flags=re.IGNORECASE)
        processed_text = re.sub(r'http[s]?://\S+', '', processed_text, flags=re.IGNORECASE).strip()

        if processed_text not in seen_texts:
            seen_texts.add(processed_text)
            processed_data_step2.append(obj)
        else:
            if obj_id is not None:
                removed_ids_step2.append(obj_id)

    return processed_data_step2, removed_ids_step2


# Extract potential locations from a tweet using a regex pattern, excluding generic references
def regLoc(text):
    regex = r'[0-9A-Za-z]+\s(rd\.?|ave\.?|Street|Avenue|Road|Yard|Lane|Court|Hill|Highwalk|Way|Square|Walk|Park|Underground|Passage|Alley|Close|Gardens|Hall|bayou|river|stream|creek|brook|Circle|Row|Buildings|Crescent|Market|Drive|Arcade|Esplanade|Grove|Garden|Bridge|Overpass|interstate|highway|expressway|freeway|tollway|exit|parkway|route|church|school|center|Ridge|Terrace|Boulevard|Inn|Wharf|St\.?|Ave\.?|Rd\.?|Yd\.?|Ct\.?|Pl\.?|Sq\.?|Bld\.?|Blvd\.?|Cres\.?|Dr\.?|Esp\.?|Grn\.?|Gr\.?|Tce\.?|Bvd\.?|Ln\.?|street|avenue|road|yard|lane|court|square|park|underground|building|Wall|wall|crescent|drive|esplanade|garden|bridge|ridge|terrace|boulevard|Building|grove|underground|(I|i|US|us|Interstate|interstate|United States|united states|SR|State Road)[ -]?\d+)\b'
    locations = re.finditer(regex, text, re.IGNORECASE)

    # Remove some general references, e.g., "his street", "empty streets", that do not refer to specific locations
    listOfStrings = ['his', 'the', 'a', 'my', 'never', 'from', 'in', r'that''s', 'called', 'for', 'to',
                     'at', 'with', 'of', 'minor', 'own', 'against', 'front', 'that', 'make', 'grave', 'were',
                     'busy', 'apartment', 'not', 'worst', 'watering', 'temporary', 'are', 'is', 'and', 'about',
                     'know', 'flooded', 'your', 'access', 'service', 'secret', 'gotta', 'whole', 'this', 'their',
                     'shit', 'save', 'reports', 'posted', 'possible', 'parallel', 'outside', 'our', 'or', 'observe',
                     'one', 'no', 'neighbours', 'multiple', 'localized', 'like', 'its', 'impacted', 'her',
                     'hazardous', 'every', 'empty', 'dear', 'come', 'by', 'gotta', 'of', 'stop', 'much', 'don\'t',
                     'reported', 'before', 'after']

    loc = []
    for m in locations:
        if m.group(0).partition(' ')[0].lower() not in listOfStrings:
            loc.append(m.group().title())

    return loc


# Step 3: Remove tweets without any detected potential locations.
def preprocess_step3(data):
    processed_data_step3 = []
    removed_ids_step3 = []

    for json_obj in data:
        text = json_obj.get("text", "")
        obj_id = json_obj.get("id", None)
        loc = regLoc(text)

        if len(loc) > 0:
            processed_data_step3.append(json_obj)
        else:
            if obj_id is not None:#arwx
                removed_ids_step3.append(obj_id)

    return processed_data_step3, removed_ids_step3


# Run the three-step preprocessing pipeline on one JSON file and save the cleaned data
def preprocess_one_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    data = [json.loads(line) for line in lines]
    original_count = len(data)

    # Step 1
    data_after_step1, removed_ids_step1 = preprocess_step1(data)
    print(f"Object count of original file: {original_count}")
    print(f"Object count after step 1: {len(data_after_step1)}")

    # Step 2
    data_after_step2, removed_ids_step2 = preprocess_step2(data_after_step1)
    print(f"Object count after step 2: {len(data_after_step2)}")

    # Step 3
    data_after_step3, removed_ids_step3 = preprocess_step3(data_after_step2)
    print(f"Object count after step 3: {len(data_after_step3)}")

    # Write the final processed data to the output JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in data_after_step3:
            f.write(json.dumps(item) + '\n')


# Process all JSON files in the input folder and save them to the output folder.
def process_all_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename)

            preprocess_one_file(input_file, output_file)
            print(f"Processed {filename}\n")


def main():
    input_folder = '' # Path to the folder containing the original JSON files
    output_folder = '' # Path to the folder where the processed files will be saved
    process_all_files(input_folder, output_folder)


if __name__ == "__main__":
    main()

