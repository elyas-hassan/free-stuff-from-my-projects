# 📸 Wikimedia Image Auto-Fetcher for Google Sheets

This Google Apps Script fetches the **first available image from Wikimedia Commons** for each name in your spreadsheet and displays it in the next column using the `=IMAGE()` formula.

It adds a custom menu to your Google Sheet for easy access.

---

## ✅ Features

- 📷 Fetches public images based on keywords (e.g., "Eiffel Tower", "Mars")
- 📄 Uses Wikimedia Commons API
- 🧩 Displays them in Google Sheets using `=IMAGE(...)`
- 🧭 Custom menu: **📸 Image Tools > Auto Get & Display Images**
- 🛡️ Handles empty cells, API errors, and rate limits safely

---

## 🧪 Example Use Case

| Column A (Names)     | Column B (Images)          |
|----------------------|----------------------------|
| Eiffel Tower         | 🖼️ *(displays an image)*   |
| Albert Einstein      | 🖼️ *(displays an image)*   |
|                      | *(skipped — empty cell)*   |

---

## ▶️ How to Use

### Step 1: Open Google Sheets

1. Click `Extensions > Apps Script`
2. Paste the code into the editor and click ✅ Save

### Step 2: Reload the Sheet

A new menu will appear:
📸 Image Tools > Auto Get & Display Images

yaml
نسخ
تحرير

---

## ⚙️ Customization Guide

You can modify these **3 variables** at the top of the script:

```javascript
const NAME_COLUMN = 1;      // Column A (1) — where names/terms are
const IMAGE_DISPLAY_COLUMN = 2; // Column B (2) — where image formulas go
🔁 Change starting row
To skip headers (like a title row), change this:

javascript
نسخ
تحرير
for (let i = 1; i <= lastRow; i++) {
⬇️ to:

javascript
نسخ
تحرير
for (let i = 2; i <= lastRow; i++) {
This will start from row 2 instead of row 1.

📏 Optional Tweaks
You can change the image size with this line:

javascript
نسخ
تحرير
const imageFormula = '=IMAGE("' + imageUrl + '", 4, 100, 100)';
Mode 4 allows you to manually set width/height.

You can log results by opening Apps Script > Executions to debug what’s happening.

📜 License
This script is part of the free-stuff-from-my-projects repository.

Licensed under CC BY-NC 4.0

✅ Free to use, modify, and share for non-commercial use

🙏 Attribution is appreciated, but not required

🚫 Do not use in paid or commercial products
