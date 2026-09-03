/**
 * Returns the number of sheets in the workbook.
 *
 * @return {Int} number
**/
function SHEETCOUNT() {
  return SpreadsheetApp.getActive().getSheets().length;
}


/**
 * Returns a 1D array of all sheet names.
 * Useful for nesting inside other formulas.
 *
 * @return {String[]} A 1D array of sheet names.
 */
function SHEETNAMES() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheets = ss.getSheets();
  return [sheets.map(sheet => sheet.getName())];
}


/**
 * Updates the list of sheet names used by the report.
 * Sheet names are written to report!Z2:Z.
 */
function updateSheetNames() {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const reportSheet = ss.getSheetByName("report");

    if (!reportSheet) {
        throw new Error('Sheet named "report" was not found.');
    }

    const sheetNames = ss.getSheets()
        .map(sheet => sheet.getName())
        .filter(name => name.toLowerCase() !== "report")
        .map(name => [name]);

    // Clear the existing helper list.
    reportSheet.getRange("Z2:Z").clearContent();

    // Write the current sheet names.
    if (sheetNames.length > 0) {
        reportSheet
            .getRange(2, 26, sheetNames.length, 1)
            .setValues(sheetNames);
    }
}


/**
 * Installable spreadsheet change trigger.
 * Runs when sheets are added, removed, renamed, etc.
 */
function workbookChanged(e) {
    updateSheetNames();
}


/**
 * Run this ONCE manually to create the installable trigger.
 */
function installWorkbookChangeTrigger() {
    const ss = SpreadsheetApp.getActiveSpreadsheet();

    // Prevent duplicate triggers.
    ScriptApp.getProjectTriggers().forEach(trigger => {
        if (trigger.getHandlerFunction() === "workbookChanged") {
            ScriptApp.deleteTrigger(trigger);
        }
    });

    ScriptApp.newTrigger("workbookChanged")
        .forSpreadsheet(ss)
        .onChange()
        .create();

    // Populate the list immediately.
    updateSheetNames();
}

