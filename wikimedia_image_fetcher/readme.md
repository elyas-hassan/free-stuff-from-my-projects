function autoGetAndDisplayImages() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const lastRow = sheet.getLastRow();

  const NAME_COLUMN = 1;      // Column A: where your names are (e.g., "Albake", "Eiffel Tower")
  const IMAGE_DISPLAY_COLUMN = 2; // Column B: where the image or status will be displayed

  // Base URL for Wikimedia Commons API
  const WIKIMEDIA_API_BASE = "https://commons.wikimedia.org/w/api.php";

  // Display a message box at the start
  Browser.msgBox("Starting Image Automation", "The script will now try to find and display images. This might take a while for many rows.", Browser.Buttons.OK);

  for (let i = 1; i <= lastRow; i++) { // Loop through rows, starting from row 2 (assuming header in row 1)
    const name = sheet.getRange(i, NAME_COLUMN).getValue();
    let imageUrl = ''; // Variable to store the found URL

    // Only process if the name cell is not empty
    if (name && typeof name === 'string' && name.trim() !== '') {
      Logger.log('Processing: ' + name); // Log for debugging (viewable in Apps Script editor -> Executions)

      try {
        // Construct the API URL for Wikimedia Commons search
        // - action=query: perform a query
        // - format=json: get results in JSON format
        // - prop=imageinfo: request information about images
        // - iiprop=url: specifically request the direct URL of the image
        // - generator=search: generate a list of pages based on a search
        // - gsrsearch=: the search term (encoded)
        // - gsrnamespace=6: filters results to only 'File' namespace (where images are stored)
        // - gsrlimit=1: gets only the first result
        const apiUrl = WIKIMEDIA_API_BASE +
                       "?action=query" +
                       "&format=json" +
                       "&prop=imageinfo" +
                       "&iiprop=url" +
                       "&generator=search" +
                       "&gsrsearch=" + encodeURIComponent(name) +
                       "&gsrnamespace=6" +
                       "&gsrlimit=1" +
                       "&continue="; // 'continue' is good practice for API calls

        // Fetch the data from the Wikimedia API
        const response = UrlFetchApp.fetch(apiUrl, {muteHttpExceptions: true}); // mute to handle errors gracefully
        const json = JSON.parse(response.getContentText()); // Parse the JSON response

        // --- Parse the JSON response to find the image URL ---
        if (json.query && json.query.pages) {
          const pages = json.query.pages;
          // The pages object will contain a single key (the pageId) due to gsrlimit=1
          for (const pageId in pages) {
            if (pages.hasOwnProperty(pageId)) {
              const page = pages[pageId];
              // Check if imageinfo and a URL exists
              if (page.imageinfo && page.imageinfo.length > 0 && page.imageinfo[0].url) {
                imageUrl = page.imageinfo[0].url;
                Logger.log('Found URL for ' + name + ': ' + imageUrl);
                break; // Found an image, exit the loop over pages
              }
            }
          }
        }

        // --- Insert the IMAGE formula into the sheet ---
        if (imageUrl) {
          const imageFormula = '=IMAGE("' + imageUrl + '")'; // Create the Google Sheets IMAGE formula
          sheet.getRange(i, IMAGE_DISPLAY_COLUMN).setFormula(imageFormula); // Set the formula in Column B
        } else {
          sheet.getRange(i, IMAGE_DISPLAY_COLUMN).setValue("No image found"); // Report if no image URL was found
          Logger.log('No image URL found for: ' + name);
        }

      } catch (e) {
        // Catch any errors during API call or parsing
        sheet.getRange(i, IMAGE_DISPLAY_COLUMN).setValue("Error fetching image");
        Logger.log('Error for ' + name + ': ' + e.message);
      }
      
      // IMPORTANT: Add a small delay to avoid hitting Wikimedia's rate limits
      // This is crucial for automation, especially with many rows
      Utilities.sleep(500); // Pause for 0.5 seconds between requests
    } else {
      // If the name cell is empty, clear the display cell
      sheet.getRange(i, IMAGE_DISPLAY_COLUMN).clearContent(); 
    }
  }
  // Display a message box when the entire process is complete
  Browser.msgBox("Image Automation", "Process complete! Check Column B for images or status messages.", Browser.Buttons.OK);
}

// This function creates the custom menu in your Google Sheet
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu("📸 Image Tools")
    .addItem("Auto Get & Display Images", "autoGetAndDisplayImages") // New menu item to run the main function
    .addToUi();
}
