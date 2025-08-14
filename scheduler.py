from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from crud.fixed_consume import process_monthly_expenses
from sqlalchemy.orm import Session
from database import get_db

scheduler = BackgroundScheduler()


def process_monthly_expenses_with_db():
    db_generator = get_db()
    db: Session = next(db_generator)

    try:
        process_monthly_expenses(db)
    except Exception as e:
        print(f"Error during process_monthly_expenses execution: {e}")
    finally:
        next(db_generator, None)


def job_listener(event):
    if event.exception:
        print(f"Job {event.job_id} failed with exception: {event.exception}")
    else:
        print(f"Job {event.job_id} executed successfully.")


def init_scheduler():
    scheduler.add_job(process_monthly_expenses_with_db, "interval", days=1)
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
