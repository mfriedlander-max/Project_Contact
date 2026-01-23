# Google Sheets Auto-Move Rows by Connection Level

**Goal:** When you change the "Connection Level" column, automatically move the entire row to the matching sheet.

**Sheets:**
- Main sheet (source) - where contacts start
- "Message Sent" - for Connection Level = "Message Sent"
- "Connected" - for Connection Level = "Connected"
- "In Touch" - for Connection Level = "In Touch"
- "Friends" - for Connection Level = "Friends"
- "Didn't Connect" - for Connection Level = "Didn't Connect"

**Columns (all sheets have identical headers):**
| Column | Purpose |
|--------|---------|
| Campaign | Git branch name (campaign identifier) |
| Name | Contact name |
| Email | Email address |
| Email Confidence | HIGH/MEDIUM/LOW for email |
| Company | Company name |
| Title | Role/title |
| Personalized Insert | The 15-25 word insert |
| Word Count | Insert word count |
| Insert Confidence | HIGH/MEDIUM/LOW for insert |
| Sources | Where facts came from |
| Email Status | blank → "drafted" → "sent" |
| Draft Created | Timestamp when draft was created |
| Sent Date | Date email was sent |
| Connection Level | Determines which sheet the row belongs to |

**Behavior:**
- Change Connection Level → row moves to matching sheet
- Row is deleted from source sheet (no empty rows)
- Can move back by changing Connection Level again
- All columns preserved (script reads headers dynamically)
- After move, target sheet auto-sorts (rows WITH Connection Level above rows WITHOUT)

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
const CONNECTION_LEVEL_COLUMN = "Connection Level";
const TARGET_SHEETS = ["Message Sent", "Connected", "In Touch", "Friends", "Didn't Connect"];

function testSetup() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getActiveSheet();
  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  Logger.log("Headers: " + JSON.stringify(headers));
  Logger.log("Connection Level col: " + headers.indexOf(CONNECTION_LEVEL_COLUMN));
  Logger.log("Sheets: " + ss.getSheets().map(s => s.getName()));
}

function onEdit(e) {
  const sheet = e.source.getActiveSheet();
  const range = e.range;
  const row = range.getRow();
  const col = range.getColumn();
  if (row === 1) return;
  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  const connectionLevelCol = headers.indexOf(CONNECTION_LEVEL_COLUMN) + 1;
  if (col !== connectionLevelCol) return;
  const newValue = e.value;
  if (!TARGET_SHEETS.includes(newValue)) return;
  if (sheet.getName() === newValue) return;
  const targetSheet = e.source.getSheetByName(newValue);
  if (!targetSheet) {
    SpreadsheetApp.getUi().alert(`Sheet "${newValue}" not found!`);
    return;
  }
  const rowData = sheet.getRange(row, 1, 1, headers.length).getValues()[0];
  if (targetSheet.getLastRow() === 0) {
    targetSheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  }
  const targetRow = targetSheet.getLastRow() + 1;
  targetSheet.getRange(targetRow, 1, 1, rowData.length).setValues([rowData]);
  sheet.deleteRow(row);
  sortSheetByConnectionLevel(targetSheet);
}

function sortSheetByConnectionLevel(sheet) {
  const lastRow = sheet.getLastRow();
  if (lastRow <= 1) return;
  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  const connectionLevelCol = headers.indexOf(CONNECTION_LEVEL_COLUMN);
  if (connectionLevelCol === -1) return;
  const dataRange = sheet.getRange(2, 1, lastRow - 1, headers.length);
  const data = dataRange.getValues();
  const withLevel = [];
  const withoutLevel = [];
  data.forEach(row => {
    const connectionLevel = row[connectionLevelCol];
    if (connectionLevel && connectionLevel.toString().trim() !== '') {
      withLevel.push(row);
    } else {
      withoutLevel.push(row);
    }
  });
  const sorted = [...withLevel, ...withoutLevel];
  dataRange.setValues(sorted);
}

function sortCurrentSheet() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  sortSheetByConnectionLevel(sheet);
}
```

---

## First-Time Setup

After pasting the script:

1. Click **Run** to authorize (click through the warnings)
2. Run `testSetup` to verify headers and sheet names are correct
3. Ensure all target sheets exist and have matching headers

---

## How It Works

| Action | Result |
|--------|--------|
| Change Connection Level to "Connected" | Row moves to "Connected" sheet |
| Change it back to "Message Sent" | Row moves back to "Message Sent" sheet |
| Change to value not in list | Nothing happens (row stays) |
| Edit any other column | Nothing happens |
| Run `sortCurrentSheet` | Manually sort current sheet (Connection Level above empty) |
| Run `testSetup` | Debug: log headers and sheet names |

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
const TARGET_SHEETS = ["Message Sent", "Connected", "In Touch", "Friends", "Didn't Connect"];
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
