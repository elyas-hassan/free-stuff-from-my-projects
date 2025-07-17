# 🧹 Format `.txt` Files into `.jsonl` for Fine-Tuning

This script converts a folder of `.txt` files into a `.jsonl` file, where each line is a JSON object containing a `"text"` field. It's designed to help prepare data for training or fine-tuning language models on platforms like OpenAI, HuggingFace, Cohere, etc.

---

## 🔧 What It Does

- Reads all `.txt` files in a given directory
- Skips very short or empty files (default: <50 characters)
- Creates a `.jsonl` file with one object per line like:
  ```json
  { "text": "Content of the text file..." }


## 📦 Requirements

Just Python 3 — no external packages required.


## 📁 Usage

1- Edit the script and set your desired paths:

SOURCE_DIR = "your_folder_with_txt_files"
OUTPUT_FILE = "your_output_file.jsonl"

2- run :

python format_finetune_data.py

3- After running, you’ll find the output in the same directory or wherever you set OUTPUT_FILE.

