# refresh_pipeline.py
# Example daily-refresh ETL script for the dashboard.
# Reads the Excel file, computes summaries, and writes CSV outputs.
# Schedule this with Windows Task Scheduler or cron.

import pandas as pd
from pathlib import Path
import datetime as dt

SOURCE = Path("data/Healthcare CaseStudy Data.xlsx")  # adjust if needed
OUTDIR = Path("data/derived")
OUTDIR.mkdir(parents=True, exist_ok=True)

# ---- Edit these to match your schema ----
VISIT_DATE = "Visit Date"          # e.g., 'Visit Date'
DEPARTMENT = "Department"          # e.g., 'Department'
WAIT_MINUTES = "Waiting Minutes"   # numeric minutes column
DOCTOR = "Doctor"                  # doctor name column
LICENSE_EXPIRY = "License Expiry"  # optional, if present
TARGET_MINUTES = 30

def _infer_week_start(d):
    d = pd.to_datetime(d, errors="coerce")
    return (d - pd.to_timedelta(d.dt.dayofweek, unit="d")).dt.normalize()

def main():
    df = pd.read_excel(SOURCE)
    # Coerce
    df[VISIT_DATE] = pd.to_datetime(df[VISIT_DATE], errors="coerce")
    df["waiting_minutes"] = pd.to_numeric(df[WAIT_MINUTES], errors="coerce")
    df["is_compliant"] = df["waiting_minutes"] <= TARGET_MINUTES
    df["week_start"] = _infer_week_start(df[VISIT_DATE])

    # Weekly
    weekly = df.groupby("week_start")["is_compliant"].mean().mul(100).reset_index()
    weekly.rename(columns={"is_compliant":"compliance_pct"}, inplace=True)
    weekly.to_csv(OUTDIR / "weekly_compliance.csv", index=False)

    # Department
    dept = df.groupby(DEPARTMENT)["is_compliant"].mean().mul(100).reset_index()
    dept.rename(columns={"is_compliant":"Compliance %", DEPARTMENT:"Department"}, inplace=True)
    dept.to_csv(OUTDIR / "department_performance.csv", index=False)

    # Doctor + License
    doctor = df.groupby(DOCTOR)["is_compliant"].agg(["mean","count"]).reset_index()
    doctor["Compliance %"] = doctor["mean"]*100
    doctor.rename(columns={DOCTOR:"Doctor", "count":"Visits"}, inplace=True)
    if LICENSE_EXPIRY in df.columns:
        now = pd.Timestamp.today().normalize()
        latest_expiry = df.groupby(DOCTOR)[LICENSE_EXPIRY].max().reset_index()
        latest_expiry.rename(columns={DOCTOR:"Doctor", LICENSE_EXPIRY:"License Expiry"}, inplace=True)
        doctor = doctor.merge(latest_expiry, on="Doctor", how="left")
        doctor["Days to Expiry"] = (pd.to_datetime(doctor["License Expiry"], errors="coerce") - now).dt.days
    doctor[["Doctor","Visits","Compliance %","License Expiry","Days to Expiry"]].to_csv(OUTDIR / "doctor_compliance_licensing.csv", index=False)

    print("Refresh complete. CSVs written to", OUTDIR.resolve())

if __name__ == "__main__":
    main()
