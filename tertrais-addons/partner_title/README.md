# Partner Title Module - Contact Titles Import Documentation

## Overview

This module restores the title field in the partner form for Odoo v19.0. The title field was removed in Odoo v19.0, and this module provides a way to maintain existing title data during the upgrade process.

## ⚠️ CRITICAL: Pre-Upgrade Data Export

**This procedure MUST be completed BEFORE upgrading to v19.0. Failure to do so will result in permanent data loss of contact titles.**

---

## Migration Procedure

### Step 1: Export Partner Titles (BEFORE Upgrade)

**When to do this:** Before upgrading the production database to v19.0

1. Navigate to **Contacts** > **Configuration** > **Partner Titles**
2. Select all title records (click the checkbox in the header)
3. Click **Action** > **Export**
4. In the export wizard:
   - ✅ **Enable "Compatible for re-import" option** (this includes external IDs)
   - Select the following fields to export:
     - `id` (External ID)
     - `name`
     - `shortcut`
   - Choose **CSV** format
5. Download the file and save it as `res.partner.title (res.partner.title).csv`

**Why this is important:** The external IDs are necessary to maintain the relationships between partners and their titles after the upgrade.

---

### Step 2: Export Partners with Titles (BEFORE Upgrade)

**When to do this:** Before upgrading the production database to v19.0

1. Navigate to **Contacts**
2. **Apply filter** to show only partners with titles:
   - Add a custom filter: `Title is set`
   - This prevents exporting thousands of partners without titles
3. After filtering, click **"Select All Records"** at the top of the list
   - ⚠️ Simply clicking the header checkbox is NOT enough - you must click the "Select All Records" button that appears
4. Click **Action** > **Export**
5. In the export wizard:
   - ✅ **Enable "Compatible for re-import" option**
   - ⚠️ **Select XLSX format (NOT CSV)** - This is critical for handling special characters like quotes: `"`
   - Select the following fields to export:
     - `id` (External ID)
     - `name`
     - `title/id` (External ID of the title)
6. Download the file and save it as `Contact (res.partner).xlsx`

**Why XLSX format:** CSV can have encoding issues and problems with special characters in names and titles. XLSX format preserves all data correctly.

---

### Step 3: Clean Export Files

**When to do this:** Immediately after exporting both files

Some title external IDs may have the prefix `base.` (e.g., `base.res_partner_title_miss`). These references need to be cleaned up to work with the new module.

#### For the Titles File (`res.partner.title (res.partner.title).csv`):

1. Open the file in a text editor or spreadsheet application
2. Find all external IDs that start with `base.`
3. Remove the `base.` prefix from these IDs
   - Example: `base.res_partner_title_miss` → `res_partner_title_miss`

#### For the Partners File (`Contact (res.partner).xlsx`):

1. Open the file in a spreadsheet application (Excel, LibreOffice Calc, etc.)
2. Find the column containing title external IDs (`title/id`)
3. Find all cells that start with `base.`
4. Remove the `base.` prefix from these references
   - Example: `base.res_partner_title_miss` → `res_partner_title_miss`
5. Save the file

**Find and Replace Method:**
- Use Find & Replace functionality
- Find: `base.` (at the beginning of cells in the ID columns)
- Replace with: (empty string)
- Make sure to only replace in the external ID columns

---

### Step 4: Test in Staging Environment

**When to do this:** After cleaning the files and BEFORE upgrading production

⚠️ **DO NOT SKIP THIS STEP**

1. Set up a staging environment with a copy of your production database
2. Upgrade the staging database to v19.0
3. Install the `partner_title` module
4. Import the cleaned titles file:
   - Navigate to **Contacts** > **Configuration** > **Partner Titles**
   - Click **Import records**
   - Upload `res.partner.title (res.partner.title).csv`
   - Map the columns correctly
   - Click **Test**
   - If everything seems ok, click **Import**
5. Import the cleaned partners file:
   - Navigate to **Contacts**
   - Click **Import records**
   - Upload `Contact (res.partner).xlsx`
   - Map the columns correctly
   - Click **Test**
   - If everything seems ok, click **Import**
6. Verify the import:
   - Check that all titles are present
   - Check that partners have the correct titles assigned
   - Look for any error messages in the logs

**If ANY errors occur:**
- ❌ **STOP - Do NOT proceed to production**
- Investigate and fix the issues
- Re-export and clean the data if necessary
- Re-test until the import succeeds without errors

---

### Step 5: Upgrade to v19.0

**When to do this:** Only after successful testing in staging

1. Schedule maintenance window
2. Create a full backup of the production database
3. Perform the upgrade to Odoo v19.0
4. Install the `partner_title` module

---

### Step 6: Import Titles File

**When to do this:** Immediately after upgrading to v19.0

1. Navigate to **Contacts** > **Configuration** > **Partner Titles**
2. Click **Import records**
3. Upload the cleaned file: `res.partner.title (res.partner.title).csv`
4. Map the columns:
   - `id` → External ID
   - `name` → Name
   - `shortcut` → Abbreviation
5. Click **Import**
6. Verify all titles were imported successfully

---

### Step 7: Import Partners File

**When to do this:** After successfully importing titles

1. Navigate to **Contacts**
2. Click **Import records**
3. Upload the cleaned file: `Contact (res.partner).xlsx`
4. Map the columns:
   - `id` → External ID
   - `name` → Name
   - `title/id` → Title/External ID
5. Click **Import**
6. Verify:
   - All partners were imported/updated successfully
   - Partners have the correct titles assigned
   - Check a sample of partners in the UI

---

## Troubleshooting

### Import Errors: "Record not found"

**Cause:** A partner references a title that doesn't exist

**Solution:**
1. Check that all titles were imported first (Step 6)
2. Verify that the `base.` prefix was removed from all external IDs
3. Check for typos in the external ID references

### Import Errors: "External ID already exists"

**Cause:** External ID conflicts

**Solution:**
1. Make sure you're using the "Compatible for re-import" option
2. The import should update existing records, not create duplicates

### Encoding Issues

**Cause:** Special characters not handled correctly

**Solution:**
1. Make sure you used XLSX format for the partners export

### Missing Titles After Import

**Cause:** Filter wasn't applied correctly during export

**Solution:**
1. Re-export partners, ensuring the title filter is applied
2. Verify "Select All Records" was clicked

---

## Data Files

The `data/` directory contains sample export files:
- `res.partner.title (res.partner.title).csv` - Title records
- `Contact (res.partner).csv` - Partner records with titles

These files are for reference and were used during the initial migration. They are not to be used for production migration.

---

## Technical Details

### Models

- `res.partner.title`: Restored title model with name, shortcut, and display format
- `res.partner`: Extended with title field relationship

### Fields

- `res.partner.title`:
  - `name`: Title name (e.g., "Mister", "Miss", "Doctor")
  - `shortcut`: Abbreviation (e.g., "M.", "Dr.")
  
- `res.partner`:
  - `title`: Many2one field referencing `res.partner.title`

---

## Support

For issues or questions:
- **Maintainer:** Louis-de-Bontin
- **Website:** https://www.ouiddoo.com

---

## License

AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
