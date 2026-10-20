# CLPN From Scratch · Course Folder

This folder, `clpn-course-en/` (what you get when you extract `clpn-course-en.zip`), is the whole course: the website (offline version), the data, the R scripts and the exercise solutions. You don't need an internet connection.

## 1. Where to start

1. Open `START_HERE.html` in your browser (the study guide: how to study, in what order, and the {{C:weeks}}-week plan).
2. Then open `index.html` (the syllabus); every lesson is reached from there.

Just double-click them; there is nothing to install.

## 2. What is in the folder

| Location | Contents |
| --- | --- |
| `index.html`, `START_HERE.html` | Syllabus and study guide |
| `lessons/`, `materials/` | Interactive lessons ({{C:size}}); glossary, cheat sheets, formula reference, FAQ, study log, writing workshop, paper reading pack, real-data case, assessments |
| `data/` | Simulated data (800 people × 3 waves) and the data dictionary (`data_dictionary.html`); two real public datasets: `coaches_mhc_raw.csv` for the Lesson 7.6 exercises, and `elsoc_phq8_wide.csv` with its original file in `elsoc/` for the ELSOC case (both CC0; sources and citations are in the data dictionary) |
| `R/` | The R script for each lesson, `_setup.R`, `run_all.R`, `assess_answers.R`, the real-data case scripts `data_elsoc.R` and `case_elsoc.R`, and the instructions `README.html` |
| `R/solutions/` | Exercise solutions |
| `R/output/` | Reference results (the figures and logs shown on the website); running the scripts overwrites them with your own results |
| `clpn-course.Rproj` | RStudio project file |
| `LICENSE`, `THIRD_PARTY_NOTICES.md` | Licenses |

## 3. Running R

1. Install R first, then RStudio (steps in `R/README.html`).
2. Double-click `clpn-course.Rproj` to open the course project in RStudio. Don't double-click the `.R` files directly.
3. Open `R/L2-4.R` and click Source to install the packages the course uses (needed only once).
4. For each lesson, open its script `R/Lx-y.R` (e.g. `R/L1-1.R`) and run it line by line (Ctrl/Cmd + Enter).

## 4. Running order

Running the scripts in lesson order works. These depend on each other:

- L6-4 → L6-5
- L4-3 → L10-1 → L10-2 → L10-3
- L8-3 → exercise solution for L8-3

If a result file a script needs is missing, the script stops and tells you which script to run first.

To run all lesson scripts and exercise solutions in one go, type this in the RStudio Console:

```r
source("R/run_all.R")
```

This takes about 40–95 minutes; a summary is written to `R/output/run_all_status.csv`. The two real-data case scripts are included too; see `materials/case_elsoc.html`.

## 5. License

© 2026 ZHANG. Course content (text, lessons, figures, data and documentation) is licensed under CC BY 4.0; code (R scripts, web scripts, etc.) under the MIT License. See `LICENSE`.
