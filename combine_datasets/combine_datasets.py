import os

# --- Configuration ---

# List of the JSONL files you want to merge.
# Add the paths to your generated files here.
SOURCE_FILES = [
    "training_data.jsonl",         
    "training_data2.jsonl"  
]

# The name of the final, combined dataset file.
MERGED_OUTPUT_FILE = "final_training_dataset.jsonl"

# --- Main Execution ---

def merge_jsonl_files():
    """
    Merges multiple .jsonl files into a single .jsonl file.
    """
    print("Starting dataset merge process...")
    
    lines_written = 0
    
    # Open the final output file in write mode
    with open(MERGED_OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        # Loop through each source file
        for source_file in SOURCE_FILES:
            print(f"  Processing '{source_file}'...")
            
            # Check if the source file exists
            if not os.path.exists(source_file):
                print(f"    [Warning] File '{source_file}' not found. Skipping.")
                continue
            
            # Open the source file and append its content to the output file
            with open(source_file, 'r', encoding='utf-8') as infile:
                for line in infile:
                    # Copy each line directly to the new file
                    outfile.write(line)
                    lines_written += 1
            
            print(f"    -> Done.")

    if lines_written > 0:
        print("\nMerge complete!")
        print(f"Wrote a total of {lines_written} records.")
        print(f"Your final, combined dataset is ready: '{MERGED_OUTPUT_FILE}'")
    else:
        print("\nNo data was merged. Please check your source file names and locations.")


if __name__ == "__main__":
    # Assumption: You might have named the Lua data file differently.
    # Let's rename the output from the Lua folder to be more specific before merging.
    if os.path.exists("training_data.jsonl") and os.path.exists("lua_manual_knowledge_base/training_data.jsonl"):
         os.rename(
             "lua_manual_knowledge_base/training_data.jsonl", 
             "lua_manual_training_data.jsonl"
         )
         print("Renamed 'lua_manual_knowledge_base/training_data.jsonl' to 'lua_manual_training_data.jsonl' for clarity.")

    merge_jsonl_files()

