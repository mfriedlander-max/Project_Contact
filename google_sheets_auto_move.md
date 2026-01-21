# Google Sheets Auto-Move Rows by Connection Level

**Goal:** When you change the "Connection Level" column, automatically move the entire row to the matching sheet.

**Sheets:**
- Main sheet (source) - where contacts start
- "Message Sent" - for Connection Level = "Message Sent"
- "Connected" - for Connection Level = "Connected"
- "In touch" - for Connection Level = "In touch"
- "Friend" - for Connection Level = "Friend"
- "Didn't Connect" - for Connection Level = "Didn't Connect"

**Behavior:**
- Change Connection Level → row moves to matching sheet
- Row is deleted from source sheet (no empty rows)
- Can move back by changing Connection Level again
- Formatting preserved

---

## How to Install

1. Open your Google Sheet
2. Go to **Extensions → Apps Script**
3. Delete any existing code
4. Paste the script below
5. Click **Save** (disk icon)
6. The script auto-runs on edits - no manual trigger needed

---

## The Script

```javascript
/**
 * Auto-move rows between sheets based on Connection Level column.
 * Triggers on any edit to the Connection Level column.
 */

// Configuration - sheet names must match Connection Level values exactly
const CONNECTION_LEVEL_COLUMN = "Connection Level";
const TARGET_SHEETS = ["Message Sent", "Connected", "In touch", "Friend", "Didn't Connect"];

function onEdit(e) {
  const sheet = e.source.getActiveSheet();
  const range = e.range;
  const row = range.getRow();
  const col = range.getColumn();

  // Skip header row
  if (row === 1) return;

  // Get headers to find Connection Level column
  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  const connectionLevelCol = headers.indexOf(CONNECTION_LEVEL_COLUMN) + 1;

  // Only trigger if Connection Level column was edited
  if (col !== connectionLevelCol) return;

  const newValue = e.value;

  // Check if new value matches a target sheet
  if (!TARGET_SHEETS.includes(newValue)) return;

  // Don't move if already on the target sheet
  if (sheet.getName() === newValue) return;

  // Get the target sheet
  const targetSheet = e.source.getSheetByName(newValue);
  if (!targetSheet) {
    SpreadsheetApp.getUi().alert(`Sheet "${newValue}" not found!`);
    return;
  }

  // Get the entire row data
  const rowData = sheet.getRange(row, 1, 1, sheet.getLastColumn()).getValues()[0];

  // Ensure target sheet has headers (copy from source if empty)
  if (targetSheet.getLastRow() === 0) {
    targetSheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  }

  // Find next empty row in target sheet
  const targetRow = targetSheet.getLastRow() + 1;

  // Copy row to target sheet
  targetSheet.getRange(targetRow, 1, 1, rowData.length).setValues([rowData]);

  // Delete row from source sheet
  sheet.deleteRow(row);
}

/**
 * Initialize all sheets with headers from the main sheet.
 * Run this once manually if target sheets are empty.
 */
function initializeSheets() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const mainSheet = ss.getSheets()[0]; // First sheet is main
  const headers = mainSheet.getRange(1, 1, 1, mainSheet.getLastColumn()).getValues();

  TARGET_SHEETS.forEach(sheetName => {
    let sheet = ss.getSheetByName(sheetName);

    // Create sheet if it doesn't exist
    if (!sheet) {
      sheet = ss.insertSheet(sheetName);
    }

    // Add headers if sheet is empty
    if (sheet.getLastRow() === 0) {
      sheet.getRange(1, 1, 1, headers[0].length).setValues(headers);
    }
  });

  SpreadsheetApp.getUi().alert('All sheets initialized with headers!');
}
```

---

## First-Time Setup

After pasting the script:

1. Click the dropdown next to "Debug" and select `initializeSheets`
2. Click **Run**
3. Authorize when prompted (click through the warnings)
4. This creates any missing sheets and copies headers

---

## How It Works

| Action | Result |
|--------|--------|
| Change Connection Level to "Connected" | Row moves to "Connected" sheet |
| Change it back to "Message Sent" | Row moves back to "Message Sent" sheet |
| Change to value not in list | Nothing happens (row stays) |
| Edit any other column | Nothing happens |

---

## Edge Cases Handled

- **Empty target sheet:** Headers auto-copied from source
- **Missing sheet:** Shows alert, row not moved
- **Header row edit:** Ignored
- **Non-matching value:** Ignored (row stays put)
- **Same sheet as target:** Ignored (no duplicate)

---

## Customization

To add more connection levels, edit this line in the script:

```javascript
const TARGET_SHEETS = ["Message Sent", "Connected", "In touch", "Friend", "Didn't Connect"];
```

Add or remove values as needed. Sheet names must match exactly (case-sensitive).

---

## Verification

1. Add a test contact to your main sheet
2. Set Connection Level to "Message Sent"
3. Check the "Message Sent" sheet - row should appear
4. Change Connection Level to "Connected"
5. Row should move from "Message Sent" to "Connected"
6. No empty rows left behind
