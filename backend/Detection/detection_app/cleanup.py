from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
from detection_app.models import Screenshot  
from detection_app.extensions import db



def delete_expired_screenshots():
    from detection_app import create_app
    app = create_app()

    with app.app_context():  
        expired_screenshots = Screenshot.query.filter(Screenshot.expires_at < datetime.now()).all()

        for screenshot in expired_screenshots:
            try:
                if os.path.exists(screenshot.filepath):
                    os.remove(screenshot.filepath)
                    print(f"Deleted file: {screenshot.filepath}")

                db.session.delete(screenshot)
                db.session.commit()
                print(f"Deleted database record: {screenshot.filename}")

            except Exception as e:
                print(f"Error deleting screenshot {screenshot.filename}: {e}")
                db.session.rollback()  


def start_cleanup_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=delete_expired_screenshots, trigger="interval", minutes=1)
    scheduler.start()