# Healthcare Compliance Dashboard (Streamlit)

This project delivers a **complete** Streamlit app that satisfies the exam case study requirements:

- Weekly waiting-time compliance trend  
- Department-wise performance with traffic-light indicators (🟢/🔴)  
- Doctor-level compliance and **licensing risk** detection  
- **Daily refresh** automation example (`refresh_pipeline.py`)  
- One-click **PowerPoint** summary export (editable .pptx)  

## 🧰 What’s inside

```
ComplianceDashboard_Streamlit/
├── app.py
├── refresh_pipeline.py
├── requirements.txt
├── .streamlit/
│   └── config.toml
└── data/
    └── Healthcare CaseStudy Data.xlsx   ← (bundled if you provided it)
```

## 🚀 Run locally

1. **Create a virtual environment** (recommended)  
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```
2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
3. **Start the app**  
   ```bash
   streamlit run app.py
   ```
4. In the **sidebar**, keep "Use bundled example" ON or upload your own Excel/CSV, then map columns.

## 📈 Dashboard outputs

- **Weekly compliance %** (line chart)  
- **Department performance** (table + bar chart) with 🟢/🔴 based on your threshold  
- **Doctor compliance & licensing issues** (table + "at-risk" view)

## 🧩 Column mapping

Your Excel schema may differ. Use the sidebar to map:  
- Visit date  
- Department  
- Waiting minutes or Arrival + Seen times  
- Doctor  
- (Optional) License expiry date  

## 🔁 Daily refresh (automation)

Use `refresh_pipeline.py` (edit column names at the top) and schedule it:

**Windows Task Scheduler**  
- Create task → Trigger Daily 06:00 → Action: `python refresh_pipeline.py`

**Linux/Mac cron**  
- `crontab -e` and add:  
  ```
  0 6 * * * /usr/bin/python3 /path/to/refresh_pipeline.py
  ```

**Alerts** (add your SMTP/webhook): alert when weekly compliance drops < threshold or % noncompliant rises.

## 🖼️ Export PPT

In the **Export** tab → *Create PPTX* → Download `Compliance_Summary.pptx`.  
The PPT includes key findings + weekly/department charts + doctor risk list.

## ✅ Tips

- Tune the **target minutes** and **dept compliance threshold** in the sidebar.
- For DB sources, replace the Excel reader with a DB query.
- Keep a **data dictionary** and **access controls** for governance best practices.
