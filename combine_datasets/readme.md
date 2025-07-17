# 📂 JSONL Dataset Merger

This script helps you **merge multiple `.jsonl` files** (usually for fine-tuning or training data) into one clean output file. It’s part of the [free-stuff-from-my-projects](https://github.com/elyas-hassan/free-stuff-from-my-projects) repo and is designed to be simple, safe, and effective.

---

## ✅ Features

- 🔄 Merges any number of `.jsonl` files into one
- 🚫 Skips missing files gracefully (with warnings)
- 📝 Appends all lines line-by-line (as expected by most training APIs)
- 🗂️ Optionally renames files for clarity before merging
- 📊 Shows how many records were written

---

## 🧪 Example Use Case

You have:
training_data.jsonl
training_data2.jsonl

You want:

final_training_dataset.jsonl

---

## ▶️ How to Use

### 1. Update your file list:

Edit the `SOURCE_FILES` list in the script:

```python
SOURCE_FILES = [
    "training_data.jsonl",
    "training_data2.jsonl"
]

```
### 2. Run the script:

python merge_finetune_data.py
You’ll get an output file:

نسخ
تحرير
final_training_dataset.jsonl


##📦 Requirements
Python 3.x

No external dependencies


📜 License
This script is part of the free-stuff-from-my-projects repository and is licensed under the Creative Commons BY-NC 4.0 License.

✅ Free to use and modify for non-commercial purposes

🙏 Attribution is appreciated but not required

🚫 Commercial use is not allowed
تح
