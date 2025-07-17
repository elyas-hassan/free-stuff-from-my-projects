# 📸 Wikimedia Image Auto-Fetcher for Google Sheets

This Google Apps Script fetches the **first available Wikimedia Commons image** for each name in your spreadsheet and displays it in the next column.

## ✅ Features

- Pulls public images for terms like "Eiffel Tower", "Mars", etc.
- Uses Wikimedia Commons API
- Displays them directly using the `=IMAGE()` formula
- Adds a convenient custom menu to run from Sheets UI
- Safe and polite (with delays and error handling)

## ▶️ How to Use

1. Open Google Sheets → Extensions → Apps Script
2. Paste the code into the editor
3. Save and reload the sheet
4. Click on the new menu **📸 Image Tools > Auto Get & Display Images**

📌 Put your search terms in **Column A** — results appear in **Column B**.

## 🔐 License

Shared under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).  
Use it freely for non-commercial projects. Attribution is appreciated but not required.
