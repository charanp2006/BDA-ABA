<style>
:root {
  --oc-bg: #0a0a0a;
  --oc-panel: #141414;
  --oc-raised: #1e1e1e;
  --oc-border: #3c3c3c;
  --oc-border-strong: #484848;
  --oc-text: #eeeeee;
  --oc-muted: #808080;
  --oc-heading: #9d7cd8;
  --oc-primary: #fab283;
  --oc-link: #56b6c2;
  --oc-code: #7fd88f;
  --oc-strong: #f5a742;
  --oc-emph: #e5c07b;
  --oc-error: #e06c75;
  --oc-font: Consolas, "Cascadia Mono", "Cascadia Code", "Courier New", monospace;
}
html { background: var(--oc-bg) !important; }
body {
  background: var(--oc-bg) !important;
  color: var(--oc-text) !important;
  font-family: var(--oc-font) !important;
  font-size: 16px !important;
  line-height: 1.55 !important;
  font-variant-ligatures: none;
  -webkit-font-smoothing: antialiased;
}
body.vscode-body {
  max-width: 100ch !important;
  margin: 0 auto !important;
  padding: 34px 28px 64px !important;
}
#write {
  max-width: 100ch !important;
  margin: 0 auto !important;
  padding: 34px 28px 64px !important;
  font-family: var(--oc-font) !important;
  font-size: 16px !important;
  line-height: 1.55 !important;
  color: var(--oc-text) !important;
  background: transparent !important;
}
body.vscode-body *, #write *, .oc-doc * { font-family: var(--oc-font) !important; }
h1, h2, h3, h4, h5, h6 {
  color: var(--oc-heading) !important;
  font-weight: 700 !important;
  line-height: 1.3 !important;
  margin: 1.6em 0 .6em !important;
  padding: 0 !important;
  border: 0 !important;
  background: transparent !important;
}
h1 { font-size: 1.5em !important; text-decoration: underline !important; text-underline-offset: 5px; text-decoration-thickness: 1px; }
h2 { font-size: 1.3em !important; }
h3 { font-size: 1.15em !important; }
h4 { font-size: 1.05em !important; }
h5, h6 { font-size: 1em !important; }
p { margin: .8em 0 !important; }
strong, b { color: var(--oc-strong) !important; font-weight: 700 !important; }
em, i { color: var(--oc-emph) !important; font-style: italic !important; }
del, s { color: var(--oc-muted) !important; }
a { color: var(--oc-link) !important; text-decoration: underline !important; text-underline-offset: 2px; }
a[href^="http"]::after {
  content: " (" attr(href) ")";
  color: var(--oc-primary) !important;
  font-size: .88em;
  word-break: break-all;
}
code {
  color: var(--oc-code) !important;
  background: transparent !important;
  border: 0 !important;
  padding: 0 !important;
  font-size: 1em !important;
  font-family: var(--oc-font) !important;
  white-space: break-spaces;
}
pre {
  background: var(--oc-panel) !important;
  border: 1px solid var(--oc-border) !important;
  padding: 14px 16px !important;
  margin: 1em 0 !important;
  overflow-x: auto !important;
  line-height: 1.5 !important;
  font-size: 1em !important;
  box-shadow: none !important;
}
pre code {
  color: var(--oc-text) !important;
  background: transparent !important;
  border: 0 !important;
  padding: 0 !important;
  font-size: 1em !important;
  white-space: pre;
}
ul, ol { margin: .8em 0 !important; padding-left: 1.7em !important; }
li { margin: .28em 0 !important; }
li::marker { font-family: var(--oc-font) !important; }
ul > li::marker { color: var(--oc-primary) !important; }
ol > li::marker { color: var(--oc-link) !important; }
ul ul > li::marker { color: var(--oc-link) !important; }
ul ul ul > li::marker { color: var(--oc-emph) !important; }
input[type="checkbox"] { accent-color: var(--oc-code) !important; }
blockquote {
  margin: 1em 0 !important;
  padding: .15em 0 .15em 1em !important;
  border-left: 2px solid var(--oc-border-strong) !important;
  background: transparent !important;
  color: var(--oc-emph) !important;
  font-style: italic !important;
}
blockquote p { color: var(--oc-emph) !important; margin: .3em 0 !important; }
hr {
  border: 0 !important;
  border-top: 1px solid var(--oc-muted) !important;
  height: 0 !important;
  margin: 1.8em 0 !important;
  background: transparent !important;
}
table { border-collapse: collapse !important; margin: 1em 0 !important; width: auto !important; }
th, td { border: 1px solid var(--oc-border) !important; padding: 6px 12px !important; }
th { background: var(--oc-raised) !important; color: var(--oc-text) !important; font-weight: 700 !important; }
img { max-width: 100% !important; border: 1px solid var(--oc-border) !important; border-radius: 3px !important; }
kbd {
  background: var(--oc-raised) !important;
  border: 1px solid var(--oc-border-strong) !important;
  border-bottom-width: 2px !important;
  padding: 1px 5px !important;
  color: var(--oc-text) !important;
  font-size: .9em !important;
}
::selection { background: var(--oc-heading) !important; color: var(--oc-bg) !important; }
* { scrollbar-color: var(--oc-border) var(--oc-bg); }
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--oc-bg); }
::-webkit-scrollbar-thumb { background: var(--oc-border); }
.hljs-comment, .hljs-quote { color: var(--oc-muted) !important; font-style: italic; }
.hljs-keyword, .hljs-selector-tag, .hljs-literal { color: var(--oc-heading) !important; font-style: italic; }
.hljs-type { color: var(--oc-emph) !important; font-style: italic; font-weight: 700; }
.hljs-string, .hljs-regexp, .hljs-symbol, .hljs-bullet { color: var(--oc-code) !important; }
.hljs-number { color: var(--oc-strong) !important; }
.hljs-title, .hljs-section, .hljs-title.function_, .hljs-function .hljs-title { color: var(--oc-primary) !important; }
.hljs-variable, .hljs-template-variable, .hljs-params, .hljs-built_in, .hljs-builtin-name { color: var(--oc-error) !important; }
.hljs-class .hljs-title, .hljs-title.class_ { color: var(--oc-emph) !important; }
.hljs-operator, .hljs-punctuation { color: var(--oc-link) !important; }
.hljs-attr, .hljs-attribute, .hljs-property { color: var(--oc-primary) !important; }
.hljs-tag { color: var(--oc-error) !important; }
.hljs-name { color: var(--oc-heading) !important; }
.hljs-meta { color: var(--oc-muted) !important; }
.hljs-addition { color: #4fd6be !important; background: #20303b !important; }
.hljs-deletion { color: #c53b53 !important; background: #37222c !important; }
.token.comment, .token.prolog, .token.doctype, .token.cdata { color: var(--oc-muted) !important; font-style: italic; }
.token.keyword { color: var(--oc-heading) !important; font-style: italic; }
.token.tag { color: var(--oc-error) !important; }
.token.string, .token.attr-value, .token.char { color: var(--oc-code) !important; }
.token.number, .token.boolean { color: var(--oc-strong) !important; }
.token.function, .token.class-name { color: var(--oc-primary) !important; }
.token.variable, .token.parameter { color: var(--oc-error) !important; }
.token.operator, .token.punctuation { color: var(--oc-link) !important; }
.cm-keyword { color: var(--oc-heading) !important; font-style: italic; }
.cm-builtin { color: var(--oc-error) !important; }
.cm-string, .cm-string-2, .cm-atom { color: var(--oc-code) !important; }
.cm-number, .cm-literal { color: var(--oc-strong) !important; }
.cm-def, .cm-variable-2, .cm-variable-3 { color: var(--oc-primary) !important; }
.cm-variable, .cm-variable-1 { color: var(--oc-error) !important; }
.cm-comment { color: var(--oc-muted) !important; font-style: italic; }
.cm-operator, .cm-bracket { color: var(--oc-link) !important; }
.cm-property, .cm-attribute { color: var(--oc-primary) !important; }
.cm-tag { color: var(--oc-error) !important; }
.cm-type { color: var(--oc-emph) !important; }
.cm-meta { color: var(--oc-muted) !important; }
.oc-green { color: var(--oc-code) !important; }
.oc-orange { color: var(--oc-strong) !important; }
.oc-purple { color: var(--oc-heading) !important; }
</style>

# Campus Attendance Hive – Live Demo Notes

**Team:** Bharath Krishna K K (4VV23CS033) | Charan P (4V23CS042) | Abu Safwan (4VV23CS006)

## 1) Team Split

| Member | Part | Time |
|---|---|---|
| **Bharath Krishna K K** | Problem Statement, Hadoop Ecosystem, HDFS & Architecture | 1 - 1.5 min |
| **Charan P** | Hive Table, HiveQL & Live Queries | 2.5 - 3 min |
| **Abu Safwan** | Validation, Cross-Check, Charts, Key Findings & Conclusion | 1.5 - 2 min |

**Total:** 7 - 9 Minutes

## 2) Pre-Demo Setup

Before starting, do the following in order.

### A) Resume Docker
Resume **Docker Desktop**. Wait till it's fully up.

### B) Open Required Things
Open these in advance:

- **Terminal** (Git Bash) in `C:/Charan/ABA/BDA-ABA/campus-attendance-hive/`
- **File Explorer** with `results/`, `charts/` & `screenshots/` folders (Keep as backup)
- **Browser Tabs**:
  - `http://localhost:50070/dfshealth.html#tab-overview`
  - `http://localhost:50070/explorer.html#/bda/attendance`

### C) Verify Stack & Set Path Fix

```bash
cd C:/Charan/ABA/BDA-ABA/campus-attendance-hive
export MSYS_NO_PATHCONV=1
export MSYS2_ARG_CONV_EXCL='*'
docker compose -f docker/docker-compose.yml ps
```

All 5 must be `Up` (`campus-namenode`, `campus-datanode`, `campus-hive-postgres`, `campus-hive-metastore`, `campus-hive-server`).

If any is down, run: 

```bash
docker compose -f docker/docker-compose.yml up -d
```

*(Wait 2-3 mins for HiveServer2 & Metastore to fully start)*

## 3) Step-By-Step Live Demo

### Step 1: Problem Statement (30s) – *Bharath*

**Say:**

> *"Our project is 'Campus Attendance Trend Analytics Using Apache Hive on the Hadoop Ecosystem'. We store attendance records in HDFS and analyze them using Apache HiveQL. Python is used only to generate, validate, cross-check and visualize the results. The core analysis is done entirely by Hive."*

### Step 2: Show The Dataset (20-30s) – *Bharath/Anyone*

```bash
wc -l data/attendance.csv
head -3 data/attendance.csv
```

**Say:**

> *"This is a synthetically generated dataset with 15,360 attendance records + 1 header, totaling 15,361 lines. It has 480 students, 80 subject offerings, 5 departments (CSE, ISE, ECE, EEE, ME), across 65 class dates. The data is fully anonymized and reproducible using seed 42."*

### Step 3: Show HDFS Live (40-50s) – *Bharath*

**Check HDFS from terminal**

```bash
docker compose -f docker/docker-compose.yml exec -T namenode hdfs dfs -ls -h /bda/attendance
```

**Now show in browser**

Open `http://localhost:50070/explorer.html#/bda/attendance` and show `attendance.csv` present there.

**Say:**

> *"The CSV is uploaded to HDFS at `/bda/attendance/`. HDFS acts as our distributed storage and is the source of truth for this project. Our Hive external table points directly to this HDFS path."*

### Step 4: Connect To Hive & Verify Table (45-60s) – *Charan*

**Connect via Beeline**

```bash
docker compose -f docker/docker-compose.yml exec -it hive-server beeline -u "jdbc:hive2://localhost:10000/campus_attendance" -n hive
```

**Run inside Beeline one by one**

```sql
SHOW TABLES;
DESCRIBE attendance;
SELECT COUNT(*) FROM attendance;
```

**Expected Output:** `attendance` table | 9 columns | `15360`

**Exit Beeline**

```sql
!quit
```

**Say:**

> *"We have created an external Hive table named `attendance` inside the `campus_attendance` database over the HDFS file. Notice it's an EXTERNAL table, so even if we drop this table, the data in HDFS remains untouched."*

### Step 5: Run Live HiveQL Queries (2 - 2.25 mins) – *Charan*

*(Keep the path fix ready if you open a new terminal)*

#### (a) Overall Attendance

```bash
docker compose -f docker/docker-compose.yml exec -T hive-server beeline -u "jdbc:hive2://localhost:10000/campus_attendance" -n hive --silent=true --outputformat=csv2 -e "SELECT total_records,present_records,attendance_pct FROM (SELECT COUNT(*) AS total_records, SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END) AS present_records, ROUND(100.0*SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END)/COUNT(*),2) AS attendance_pct FROM attendance) t;"
```

**Say:** *"Overall attendance is 74.95% i.e., 11,512 out of 15,360 records are PRESENT."*

#### (b) Department-wise Attendance

```bash
docker compose -f docker/docker-compose.yml exec -T hive-server beeline -u "jdbc:hive2://localhost:10000/campus_attendance" -n hive --silent=true --outputformat=csv2 -e "SELECT department,COUNT(*) AS total_records,SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END) AS present_count,ROUND(100.0*SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END)/COUNT(*),2) AS attendance_pct FROM attendance GROUP BY department ORDER BY attendance_pct DESC;"
```

**Say:** *"CSE and ISE are doing better, whereas ME is the lowest at 73.34%."*

#### (c) Subject-wise (Top 5 & Bottom 5)

```bash
docker compose -f docker/docker-compose.yml exec -T hive-server beeline -u "jdbc:hive2://localhost:10000/campus_attendance" -n hive --silent=true --outputformat=csv2 -e "SELECT subject_code,subject_name,ROUND(100.0*SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END)/COUNT(*),2) AS attendance_pct FROM attendance GROUP BY subject_code,subject_name ORDER BY attendance_pct DESC LIMIT 5;"
```

```bash
docker compose -f docker/docker-compose.yml exec -T hive-server beeline -u "jdbc:hive2://localhost:10000/campus_attendance" -n hive --silent=true --outputformat=csv2 -e "SELECT subject_code,subject_name,ROUND(100.0*SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END)/COUNT(*),2) AS attendance_pct FROM attendance GROUP BY subject_code,subject_name ORDER BY attendance_pct ASC LIMIT 5;"
```

**Say:** *"Best performing subjects are IS302 and IS503 at 83.85%. Worst are IS601 and ME403 at 67.19%."*

#### (d) Low Attendance Groups (< 75%)

```bash
docker compose -f docker/docker-compose.yml exec -T hive-server beeline -u "jdbc:hive2://localhost:10000/campus_attendance" -n hive --silent=true --outputformat=csv2 -e "SELECT COUNT(*) AS low_groups_below_75 FROM (SELECT student_id,subject_code,COUNT(*) AS total, SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END) AS present, ROUND(100.0*SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END)/COUNT(*),2) AS pct FROM attendance GROUP BY student_id,subject_code HAVING ROUND(100.0*SUM(CASE WHEN status='PORDER'
```

**Say:** *"We found 650 student-subject groups below 75%, affecting 343 different students. Also, 199 students are below 75% overall."*

#### (e) Weekly Trend (Show the Dip)

```bash
docker compose -f docker/docker-compose.yml exec -T hive-server beeline -u "jdbc:hive2://localhost:10000/campus_attendance" -n hive --silent=true --outputformat=csv2 -e "SELECT weekofyear(attendance_date) AS week_no, CONCAT('2025-W',LPAD(weekofyear(attendance_date),2,'0')) AS week_label, COUNT(*) AS total_records, SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END) AS present_count, ROUND(100.0*SUM(CASE WHEN status='PRESENT' THEN 1 ELSE 0 END)/COUNT(*),2) AS attendance_pct FROM attendance GROUP BY weekofyear(attendance_date) ORDER BY week_no;"
```

**Say:** *"Attendance was high in early weeks (W36 - 82.06%) but shows a clear dip in W42 (63.45%) and gradually recovers towards the end."*

> *Note:* The first query may take 20-40 seconds due to local MapReduce. That's expected.

### Step 6: Validation, Cross-Check & Visuals (1 - 1.5 mins) – *Abu Safwan*

**Show validation & cross-check**

```bash
cat results/validation_report.txt | tail -6
echo "--------------------------------"
cat results/crosscheck_report.txt | tail -4
```

**Say:**

> *"Our dataset passed all 15 validation checks. More importantly, we independently recomputed every metric in Python and compared with Hive outputs. All 8 comparisons passed with a maximum difference of just 0.01% due to rounding. This proves our Hive results are correct."*

**Show Charts from File Explorer**

Open and explain these one by one:

- `charts/weekly_trend.png` – *Shows the gradual decline and sharp dip in W42*
- `charts/department_attendance.png` – *Department-wise comparison*
- `charts/subject_attendance.png` – *Subject-wise comparison*
- `charts/low_attendance_distribution.png` – *Distribution of student-subject groups below 75%*
- `charts/student_attendance_distribution.png` – *Overall student-wise attendance spread*

**Quickly show summary**

```bash
cat results/key_findings.md
```

### Step 7: Conclusion (25-35s) – *Abu Safwan*

**Say this exact line:**

> *"We stored 15,360 synthetic attendance records in HDFS, analysed them with eight HiveQL queries in Apache Hive, independently verified every result in Python with 8/8 matches, and produced charts showing 74.95% overall attendance, 650 low-attendance student-subject groups, and a declining weekly trend."*

**End with:** *"Thus, we have successfully implemented Campus Attendance Trend Analytics using the Hadoop Ecosystem with HDFS and Apache Hive at its core."*

## 4) Viva Q&A – Quick Answers

| Question | Answer |
|---|---|
| **Why Hive and not Pandas?** | *"Hive is the main analytics engine over HDFS as per the project requirement. Pandas is used only for dataset generation, validation, independent cross-checking and charting."* |
| **What is an External Table?** | *"An external table keeps the data in HDFS. Dropping the Hive table does not delete the actual CSV file from HDFS. This matches our setup."* |
| **Why Docker?** | *"Native Hadoop/Hive wasn't available on Windows and our system had Java 26 which is incompatible with Hadoop 2.7. Docker gave us a real Hadoop 2.7.4 + Hive 2.3.2 environment."* |
| **How did you verify correctness?** | *"Dataset validation gave 15/15 PASS. Independent Python cross-check gave 8/8 PASS against actual Hive CSV results."* |
| **Why MapReduce in local mode?** | *"We didn't start YARN in this single-node container setup. Hive compiles queries to MapReduce jobs and runs them locally inside HiveServer2."* |
| **Is the data real?** | *"No, it's completely synthetic and anonymized. Generated using Python with seed 42 for reproducibility."* |
| **Why is some % exactly in multiples of 12.5?** | *"Each student-subject pair has 8 sessions. So attendance is calculated out of 8, hence percentages like 12.5%, 25%, 37.5% appear."* |

## 5) Backup Plan (If Anything Fails)

| Situation | Action |
|---|---|
| **Docker/containers slow to load** | Give 2-3 more mins. Check `docker compose -f docker/docker-compose.yml ps` again. |
| **Beeline fails to connect** | Wait 30-60s and retry. HiveServer2 takes time after restart. |
| **A live query runs too long (>40s)** | Hit `Ctrl + C`, switch to backup and say *"Here are the exact Hive results saved from our clean run"* then show `results/<query_name>.csv` |
| **HDFS UI doesn't load** | Show `screenshots/01_hdfs_namenode_overview.png` and `screenshots/02_hdfs_bda_attendance.png` instead. |
| **Any doubt** | Rely on `results/`, `charts/` and `key_findings.md`. All are real outputs from the actual executed run. |

## 6) Final Quick Checklist

- [ ] **Docker resumed** and all 5 containers `Up`
- [ ] **Path exports** done (`MSYS_NO_PATHCONV=1` & `MSYS2_ARG_CONV_EXCL='*'`)
- [ ] **HDFS UI** loading at `localhost:50070`
- [ ] **Beeline** able to connect to `campus_attendance`
- [ ] **Backup folders** (`results/`, `charts/`) ready
- [ ] **Team** clear with assigned parts
- [ ] **Memorized** the 1-line conclusion
