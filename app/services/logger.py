# app/services/logger.py
from app.database import SessionLocal
from app.models import Analysis

def log_analysis(ticker, benchmark, start, end, files):
    with SessionLocal() as db:
        rec = Analysis(
            ticker=ticker,
            benchmark=benchmark,
            start_date=start,
            end_date=end,
            files=files,
        )
        db.add(rec)
        db.commit()
        db.refresh(rec)
        return rec.id