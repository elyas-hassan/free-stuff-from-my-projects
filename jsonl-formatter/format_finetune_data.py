import os
import json

# --- Configuration ---

# The directory where you saved all your scraped .txt files.
# This should match the OUTPUT_DIR from your scraper script.
SOURCE_DIR = "file_name_here"

# The name of the final, formatted file ready for finetuning.
OUTPUT_FILE = "file_name_here_for_the_wanted_output"

# --- Main Execution ---

def format_data_for_finetuning():
    """
    Reads all .txt files from the source directory, combines them
    into a single .jsonl file, with each line being a JSON object.
    """
    print(f"Starting data formatting process...")
    print(f"Source directory: '{SOURCE_DIR}'")

    # Check if the source directory exists
    if not os.path.isdir(SOURCE_DIR):
        print(f"[Error] Source directory '{SOURCE_DIR}' not found.")
        print("Please make sure you have run the scraper script first and that the directory name is correct.")
        return

    # Counter for the number of files processed
    files_processed = 0

    # Open the output file in write mode
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        # Loop through all files in the source directory
        for filename in os.listdir(SOURCE_DIR):
            # Process only .txt files
            if filename.endswith(".txt"):
                filepath = os.path.join(SOURCE_DIR, filename)
                
                try:
                    # Read the entire content of the text file
                    with open(filepath, 'r', encoding='utf-8') as infile:
                        text_content = infile.read()

                    # Skip empty or very short files to avoid low-quality data
                    if len(text_content.strip()) < 50:
                        print(f"  [Skipping] File '{filename}' is too short.")
                        continue

                    # Create a JSON object in the required format for finetuning.
                    # Many platforms expect a simple {"text": "..."} structure.
                    json_record = {
                        "text": text_content
                    }
                    
                    # Write the JSON object as a string to the output file,
                    # followed by a newline character.
                    outfile.write(json.dumps(json_record) + "\n")
                    files_processed += 1

                except Exception as e:
                    print(f"  [Error] Could not process file {filename}: {e}")

    if files_processed > 0:
        print(f"\nFormatting complete!")
        print(f"Successfully processed {files_processed} files.")
        print(f"Your finetuning dataset is ready: '{OUTPUT_FILE}'")
    else:
        print("\nNo files were processed. Please check your source directory.")


if __name__ == "__main__":
    format_data_for_finetuning()
