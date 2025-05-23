function doGet(e) {
  // This function is required for the web app to work
  return ContentService.createTextOutput(JSON.stringify({status: "ok"}))
    .setMimeType(ContentService.MimeType.JSON);
}

// Handle preflight OPTIONS requests
function doOptions(e) {
  return HtmlService.createHtmlOutput("")
    .addHeader("Access-Control-Allow-Origin", "*")
    .addHeader("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
    .addHeader("Access-Control-Allow-Headers", "Content-Type")
    .addHeader("Access-Control-Max-Age", "1800");
}

function doPost(e) {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName("Responses") || ss.insertSheet("Responses_cgreplay_demo_2025");
    var data = JSON.parse(e.postData.contents);
    
    // Add headers if sheet is empty
    if (sheet.getLastRow() === 0) {
      var headers = [
        "Timestamp",
        "User ID",
        "Scene",
        "Video A Filename",
        "Video B Filename",
        "Video A Score",
        "Video B Score",
        "Video A Comment",
        "Video B Comment",
        "Video A Is Real",
        "Video B Is Real",
        "Which Video Real",
        "Gameplay Affected",
        "Inform Preference",
        "Visual Cues",
        "Other Cues"
      ];
      sheet.appendRow(headers);
    }
    
    // Add the data row
    var row = [
      data.timestamp,
      data.user_id,
      data.scene,
      data.video_A_filename,
      data.video_B_filename,
      data.A_score,
      data.B_score,
      data.A_comment,
      data.B_comment,
      data.video_A_is_real,
      data.video_B_is_real,
      data.which_video_real,
      data.gameplay_affected,
      data.inform_preference,
      data.visual_cues,
      data.other_cues
    ];
    sheet.appendRow(row);
    
    // Return success response with CORS header
    var output = ContentService.createTextOutput(JSON.stringify({result: "success"}))
      .setMimeType(ContentService.MimeType.JSON);
    return output;
  } catch (error) {
    // Log the error for debugging
    Logger.log("Error: " + error.toString());
    
    // Return error response
    var output = ContentService.createTextOutput(JSON.stringify({
      result: "error", 
      error: error.toString()
    }))
    .setMimeType(ContentService.MimeType.JSON);
    return output;
  }
}