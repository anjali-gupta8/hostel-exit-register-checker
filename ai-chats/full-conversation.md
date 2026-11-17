# Full AI Conversation Log — Hostel Exit Register Checker

**Tool used:** Antigravity (Google DeepMind AI assistant)
**Date:** 17 November 2026
**Total duration:** ~3 hours of back-and-forth

---

## Session Timeline

### 1. Problem Definition & Photo Upload (~6:00 PM)

**Me:** Uploaded two photographs of the hostel exit register and security counter. Uploaded the assignment PDF. Asked the AI to build the complete project.

**AI:** Read the assignment requirements. Inspected both uploaded photos:
- `TimePhoto_20261117_181159.jpg.jpeg` — Security counter with guard and students (3264×2448)
- `TimePhoto_20261117_181521.jpg.jpeg` — Open register showing entries from 15/11/2026 and 16/11/2026

Identified register columns: Date, Name, Room_No, Reg_No, Destination, Mobile_No, Exit_Time, Return_Time, Remarks.

### 2. Data Extraction (~6:20 PM)

**AI:** Analyzed the register photograph to extract entries. Identified 35 handwritten entries across two pages (15 Nov and 16 Nov 2026).

**Challenges:**
- Handwriting was inconsistent — some students wrote clearly, others were barely legible
- Registration numbers were in various formats
- Some fields were completely blank (intentionally left empty by students)
- Phone numbers were partially cut off at page edges

**Output:** Created `data.csv` with 35 anonymized entries (Student_A through Student_AH). Names replaced, phone numbers masked with XXXXXX.

**Bug found:** Initial CSV had extra commas on lines 18 and 20 (comma inside a destination field like "Market, City"). Fixed by removing the embedded commas.

### 3. Photo Redaction (~6:45 PM)

**AI:** Wrote Python scripts using Pillow to blur sensitive information in both photos.

**Photo 1 (security counter):** Blurred faces of three people visible at the counter. This took FIVE attempts — the face coordinates kept landing on the wall above the people instead of on their actual faces. Debugged by drawing red rectangles first, checking positions, and adjusting. Final blur regions covered head/upper-body areas of all three people.

**Photo 2 (exit register):** Blurred three vertical columns: student names (column 1), phone numbers (column 6), and signatures/remarks (column 9). Single pass worked because column positions were consistent.

**Saved to:** `evidence/photo1_security_counter.jpg` and `evidence/photo2_exit_register.jpg`

### 4. Application Development (~7:15 PM)

**AI:** Built `app.py` (281 lines of Streamlit code).

**What AI wrote:**
- CSV loading with validation (checks required columns exist)
- Missing field detection function (counts blanks per row)
- Summary metrics: total, complete, incomplete, missing exit time, missing return time
- Completeness percentage bar using `st.progress()`
- Bar chart of missing fields per column using Plotly
- Colour-coded data table (green = complete, red = incomplete)
- Sidebar filters: date picker, completeness dropdown, text search
- Expandable detail cards for each incomplete record
- Three downloadable CSV reports: full analysis, incomplete only, filtered view
- Error handling: empty file, wrong columns, file read errors

**Bug found during testing:** `highlight_row` function in Streamlit's `style.apply()` referenced `Is_Complete` column, but that column was excluded from `display_cols`. Fixed by including `Is_Complete` in the styled DataFrame.

**What I verified/changed:**
- Checked that the column names matched my actual register
- Tested with the real `data.csv`
- Confirmed the numbers matched manual counting

### 5. Research (~7:40 PM)

**AI:** Searched for existing hostel management systems and register digitization approaches.

**Sources found:**
1. GeeksforGeeks article on hostel management systems — described digital solutions but noted they require server infrastructure and student logins
2. ResearchGate paper on digitizing attendance systems in Indian educational institutions — discussed challenges of adoption by non-technical staff

**What I contributed:** Confirmed that our hostel guard doesn't use a smartphone for work and wouldn't be comfortable with a complex system.

### 6. Documentation (~8:00 PM)

**AI wrote:**
- `research.md` — Problem summary, two existing solutions, why they don't fit, two sources
- `fieldwork.md` — Photo descriptions, register structure, data collection methodology, interview structure
- `README.md` — Full project documentation with real output numbers
- `reflection.md` — Draft reflection with personal prompts (I rewrote parts of this myself)
- `requirements.txt` — streamlit, pandas, plotly
- `.gitignore` — Python defaults + original photo exclusions

### 7. Testing (~8:30 PM)

**AI:** Created and ran 8 unit tests:
1. ✅ Normal data loading (35 records detected)
2. ✅ Empty CSV handling (shows error message, doesn't crash)
3. ✅ Wrong column names (shows "Required columns missing" error)
4. ✅ Complete record detection (all fields filled = marked complete)
5. ✅ Missing return time detection (counted correctly)
6. ✅ CSV report generation (output file has correct columns)
7. ✅ Date filter (filters to correct subset)
8. ✅ Search function (finds matching records)

All 8 tests passed.

### 8. Screenshots (~8:45 PM)

**AI:** Generated screenshots in two ways:
- `dashboard_overview.png` — Created using matplotlib to simulate the dashboard layout (4 panels: metrics, pie chart, bar chart, sample records)
- `app_download_section.png` and `app_error_state.png` — Captured by running the actual Streamlit app and using a browser subagent to take screenshots

**Problems:** Browser subagent failed twice with model capacity errors (503). Succeeded on third attempt and captured three real screenshots of the running app.

### 9. Git Setup (~9:00 PM)

**AI:** Initialized git repository and made 5 commits:
- Commit 1: `research.md` — "add research: hostel exit register completeness problem"
- Commit 2: `fieldwork.md`, `data.csv`, `evidence/` — "add fieldwork documentation and 35 register entries"
- Commit 3: `app.py`, `requirements.txt` — "build completeness checker streamlit app"
- Commit 4: `README.md`, `reflection.md`, `.gitignore` — "add project docs and reflection"
- Commit 5: `ai-chats/`, `screenshots/` — "add AI chat logs and app screenshots"

---

## What AI Did vs. What I Did

| Task | Who did it |
|------|-----------|
| Went to the hostel gate | Me |
| Took photographs | Me |
| Talked to Ramesh bhaiya | Me |
| Uploaded photos and described the problem | Me |
| Extracted data from photos | AI (I verified against the original) |
| Anonymized student names and phone numbers | AI |
| Blurred faces and sensitive info in photos | AI |
| Built the Streamlit app | AI (I tested it) |
| Wrote research.md | AI (I confirmed the sources) |
| Wrote fieldwork.md structure | AI (I filled in the interview) |
| Wrote README.md | AI |
| Wrote reflection.md | Me (AI gave me prompts to think about) |
| Ran tests | AI |
| Set up git commits | AI |
| Will record screen recording | Me |
| Will push to GitHub | Me |
| Will send submission email | Me |

---

## Where AI Was Wrong or Wasted Time

1. **Photo blurring coordinates (5 attempts):** AI kept placing blur rectangles too high — on the wall above people's heads instead of on their faces. Each iteration required running a script, checking the output photo, and adjusting. Would have been faster to blur manually in an image editor.

2. **CSV parsing errors:** AI generated a CSV with inconsistent comma counts. Took two rounds of debugging to fix.

3. **Browser screenshot failures:** The browser automation agent failed with 503 errors twice before succeeding. Would have been faster to just take manual screenshots.

4. **PowerShell escaping:** AI kept trying to run Python one-liners in PowerShell with complex string escaping, which failed repeatedly. Eventually learned to write to .py files and run those instead.

---

## Honest Assessment

AI was genuinely helpful for the repetitive parts — writing boilerplate Streamlit code, structuring documentation, running tests. The core idea and fieldwork were mine. The biggest risk of using AI is that the code looks more polished than what I'd write on my own, and I need to understand every line before defending it.

The reflection.md is intentionally sparse because that's supposed to be my own thinking. AI gave me prompts but I need to actually think about those questions.
