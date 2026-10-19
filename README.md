# Condominium Maintenance UI Prototype

A Python/Tkinter final-assessment desktop prototype for recording and managing
condominium maintenance incidents. This is an individual project by
[Tan Yi Heng](https://github.com/tan0480). The original application is retained
in a single file, `final_assessment.py`.

## Features

- Dashboard with incident totals, status counts and an incident table.
- Incident entry with required-field, category and priority checks.
- Search by ID, title, category, location or status, plus status/priority filters.
- Assignment to maintenance teams or vendors.
- Status updates and an in-memory update log.
- On-screen summary reports, including an automatic report after 10 logged
  updates. The update counter and log are cleared after that report.
- Exit confirmation, dark styling and a window fade-in effect.

## Run

Use Python 3 with Tkinter installed, on Windows. There are no third-party Python
dependencies; the script imports only `tkinter` and `datetime`.

From this repository folder:

```text
python final_assessment.py
```

The application starts with six embedded example incidents. Category and status
inputs must match the displayed options, including capitalization.

## Scope and known limitations

- This is an interactive UI prototype, not a production maintenance system.
  There is no database, file persistence, authentication or backend service.
  Changes disappear when the application closes.
- The description field is validated but is not stored in the incident record.
- Some report labels and notes are demonstration text. The displayed "Today"
  incident totals count all incidents in memory rather than filtering by date.
  Response-time claims are not calculated from recorded timings.
- The report text mentions automatic generation at 23:59, but there is no
  corresponding scheduled task. Automatic reports are triggered by logged
  updates; date rollover is checked when another update is logged.
- Updates to the same status still count. The counter resets after each
  automatic report, so it is not a cumulative daily audit total.
- Window maximization uses the Windows-oriented `zoomed` state. Other operating
  systems and display layouts have not been verified.

## Verification

The source passed an in-memory Python syntax compilation check and Tkinter
import check using Python 3.14.7 / Tk 9.0. Full GUI interaction testing was not
performed for this repository import; syntax checks do not prove UI behavior.

## Authorship and repository contents

Tan Yi Heng implemented the complete application. No teammate contributions are
claimed for this individual assessment. Import commits use current timestamps,
not the original development dates. This README and the ignore rules were
prepared with AI assistance for repository setup; the application source was
not modified during the import.

Only the Python source, this README and `.gitignore` are included. The assessment
PDF and originality-report PDF remain local and are excluded from Git.
