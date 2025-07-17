/**
 * @OnlyCurrentDoc
 *
 * The above comment directs App Script to limit the scope of script authorization
 * to only the current spreadsheet.
 */

//================================================================
// 1. SETUP: Create a custom menu when the spreadsheet is opened.
//================================================================
/**
 * Creates a custom menu in the spreadsheet UI.
 * This function runs automatically when the spreadsheet is opened.
 */
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Image Analyzer')
    .addItem('1. Set API Key', 'setApiKey')
    .addSeparator()
    .addItem('2. Identify Entities in Photos', 'identifyEntities')
    .addToUi();
}


//================================================================
// 2. API KEY MANAGEMENT: Securely store and retrieve your API key.
//================================================================
/**
 * Prompts the user to enter their Google AI API key and stores it
 * securely in User Properties, scoped to the user and the script.
 */
function setApiKey() {
  const ui = SpreadsheetApp.getUi();
  const promptResponse = ui.prompt(
    'Set Google AI API Key',
    'Please enter your Gemini API key. You can get one from Google AI Studio.',
    ui.ButtonSet.OK_CANCEL);

  // Process the user's response
  if (promptResponse.getSelectedButton() == ui.Button.OK) {
    const apiKey = promptResponse.getResponseText();
    if (apiKey) {
      PropertiesService.getUserProperties().setProperty('GEMINI_API_KEY', apiKey);
      ui.alert('Success', 'Your API key has been saved.', ui.ButtonSet.OK);
    } else {
      ui.alert('Error', 'API key cannot be empty.', ui.ButtonSet.OK);
    }
  }
}


//================================================================
// 3. CORE LOGIC: Analyze the images.
//================================================================
/**
 * Main function to process images. It loops through the active sheet,
 * fetches the image from the URL in Column B, sends it to the Gemini API,
 * and writes the result to Column C.
 */
function identifyEntities() {
  const ui = SpreadsheetApp.getUi();

  // Step 1: Get the stored API key
  const apiKey = PropertiesService.getUserProperties().getProperty('GEMINI_API_KEY');
  if (!apiKey) {
    ui.alert('API Key Not Found', 'Please set your API key first using "Image Analyzer > 1. Set API Key".', ui.ButtonSet.OK);
    return;
  }

  // Step 2: Get the active sheet and its data
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const startRow = 2; // Assuming row 1 is the header
  const lastRow = sheet.getLastRow();
  
  // Exit if there are no data rows to process
  if (lastRow < startRow) {
    ui.alert('No Data', 'No data found to process below the header row.', ui.ButtonSet.OK);
    return;
  }
  
  const dataRange = sheet.getRange(startRow, 1, lastRow - startRow + 1, 3);
  const data = dataRange.getValues();
  const formulas = dataRange.getFormulas(); // **NEW**: Get formulas in addition to values.

  // Step 3: Define the API endpoint and the prompt
  const geminiApiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=${apiKey}`;
  const prompt = "what is the entity in this photo? Be concise and specific.";

  ui.alert('Starting Analysis', `Found ${data.length} rows to process. This may take some time.`, ui.ButtonSet.OK);

  // Step 4: Loop through each row
  for (let i = 0; i < data.length; i++) {
    const currentRow = i + startRow;
    const formula = formulas[i][1]; // Get formula from Column B
    let imageUrl = data[i][1]; // Get value from Column B as a fallback
    const resultValue = data[i][2]; // Column C

    // **NEW LOGIC**: If there's an IMAGE formula, extract the URL from it.
    if (formula && formula.toUpperCase().startsWith('=IMAGE(')) {
        const match = formula.match(/=IMAGE\("([^"]+)"/i);
        if (match && match[1]) {
            imageUrl = match[1]; // Successfully extracted URL from formula
        }
    }

    // Validate the extracted or original URL
    if (typeof imageUrl !== 'string' || !imageUrl.toLowerCase().startsWith('http')) {
      if (imageUrl && !resultValue) { // Only write error if cell is not empty and has no result yet
         sheet.getRange(currentRow, 3).setValue('Error: Column B must have a valid URL or =IMAGE("url") formula.');
      }
      continue; // Skip this row and move to the next one
    }

    // Process the row only if there's a valid-looking URL and no result yet
    if (imageUrl && !resultValue) {
      try {
        // Step 5: Fetch the image from the URL and convert to Base64
        const imageBlob = UrlFetchApp.fetch(imageUrl).getBlob();
        const base64Image = Utilities.base64Encode(imageBlob.getBytes());
        const mimeType = imageBlob.getContentType();
        
        if (!mimeType || !mimeType.startsWith('image/')) {
            throw new Error('URL does not point to a valid image file.');
        }

        // Step 6: Construct the payload for the Gemini API
        const payload = {
          "contents": [{
            "parts": [{
              "text": prompt
            }, {
              "inline_data": {
                "mime_type": mimeType,
                "data": base64Image
              }
            }]
          }]
        };

        const options = {
          'method': 'post',
          'contentType': 'application/json',
          'payload': JSON.stringify(payload),
          'muteHttpExceptions': true // Important to catch API errors
        };

        // Step 7: Call the Gemini API
        const response = UrlFetchApp.fetch(geminiApiUrl, options);
        const responseCode = response.getResponseCode();
        const responseBody = response.getContentText();
        
        let entityText = '';
        
        if (responseCode === 200) {
           const parsedResponse = JSON.parse(responseBody);
           entityText = parsedResponse.candidates[0]?.content?.parts[0]?.text || "No description found.";
        } else {
           entityText = `Error: API responded with code ${responseCode}. Details: ${responseBody}`;
        }
        
        // Step 8: Write the result back to the sheet in Column C
        sheet.getRange(currentRow, 3).setValue(entityText.trim());
        
        SpreadsheetApp.flush(); 

      } catch (e) {
        // Handle errors like invalid URLs or other script issues
        sheet.getRange(currentRow, 3).setValue(`Error: ${e.message}`);
      }
    }
  }
  
  ui.alert('Analysis Complete', 'All rows have been processed.', ui.ButtonSet.OK);
}
