# 🧠 Image Entity Identifier (via Gemini API)

This Google Apps Script allows you to identify the **main entity in an image** using [Google Gemini API](https://aistudio.google.com/app). It works directly inside a Google Spreadsheet — just paste image URLs (or use `=IMAGE("url")`) and let the script process each one.

---

## ✅ Features

- 📷 Analyzes images from URLs or `=IMAGE(...)` formulas
- 🤖 Uses **Gemini 1.5 Flash** model to detect the key entity in each photo
- 📊 Results are written to **Column C** next to each image
- 🔐 Securely stores your API key using Google Apps Script’s `UserProperties`
- 🧭 Adds a custom menu for easy use

---

## 🧪 Example Layout

| A (optional) | B (Image URL or `=IMAGE()` formula)      | C (Result)              |
|-------------|-------------------------------------------|--------------------------|
| Eiffel Tower | `=IMAGE("https://upload.wikimedia.org/...")` | Eiffel Tower             |
| Cat          | `https://upload.wikimedia.org/...cat.jpg`    | A domestic cat           |

---

## ▶️ How to Use

### 1. 🧬 Set Up the Script

1. Open your **Google Sheet**
2. Click `Extensions > Apps Script`
3. Paste the code from `image-entity-identifier.gs` and click **Save**

### 2. 🔑 Add Your Gemini API Key

1. Reload your sheet
2. A menu will appear:  
   **Image Analyzer > 1. Set API Key**
3. Paste your [Google AI Studio](https://aistudio.google.com/app) API key when prompted

### 3. 🧠 Run Image Analysis

Use the menu:  
**Image Analyzer > 2. Identify Entities in Photos**

The script will:
- Scan rows from **row 2** (skipping headers)
- Read image from **Column B**
- Write entity description to **Column C**

---

## ⚙️ Customization Guide

### 🧭 Change Where the Script Looks

In the code, adjust:

```javascript
const startRow = 2; // Start from row 2
const dataRange = sheet.getRange(startRow, 1, lastRow - startRow + 1, 3);
```

### 🖼️ Accept Formulas or Plain URLs

The script supports:

- `=IMAGE("https://...")` in Column B
- Direct URLs like `https://...jpg` in Column B

---

## 🛑 Error Handling

If no image is detected or something goes wrong:
- An error message will appear in Column C
- HTTP/API issues are caught and logged

---

## 🔐 Privacy Note

- Your Gemini API key is stored **only in your account’s User Properties**.
- It is **not shared** with others using the sheet.

---

## 📜 License

This script is part of the [free-stuff-from-my-projects](https://github.com/elyas-hassan/free-stuff-from-my-projects) repository.

Licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/):

- ✅ Use freely for **non-commercial** projects
- 🙏 Mentioning the original author is appreciated, but not required
- 🚫 Do **not** include this in commercial or paid products

---
