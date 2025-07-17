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
2. Paste the script into the editor and click ✅ Save

### Step 2: Reload the Sheet

A new menu will appear:
```
📸 Image Tools > Auto Get & Display Images
```
Click it to run the script.

---

## ⚙️ Customization Guide

You can modify these **2 variables** at the top of the script:

```javascript
const NAME_COLUMN = 1;      // Column A (1) — where names/terms are
const IMAGE_DISPLAY_COLUMN = 2; // Column B (2) — where image formulas go
```

### 🔁 Change Starting Row

To **skip the header row**, update this line:

```javascript
for (let i = 1; i <= lastRow; i++) {
```

⬇️ change to:

```javascript
for (let i = 2; i <= lastRow; i++) {
```

---

## 📏 Optional Tweaks

- **Change Image Size:**

Use this line for manual sizing (e.g. 100x100 pixels):

```javascript
const imageFormula = '=IMAGE("' + imageUrl + '", 4, 100, 100)';
```

---

## 📜 License

This script is part of the [free-stuff-from-my-projects](https://github.com/elyas-hassan/free-stuff-from-my-projects) repository.

Licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)

- ✅ Free to use, modify, and share for **non-commercial use**
- 🙏 Attribution is appreciated, but not required
- 🚫 Do **not** use in paid or commercial products
