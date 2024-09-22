from database.configure import SessionLocal, get_db
from database.models import User
from repo.users.user_repo import get_current_user
from repo.scraper.scraper_repo import process_data
from fastapi import APIRouter, BackgroundTasks, Depends
from schema.scraper.scraper_request import ScraperRequest

router = APIRouter(tags=["Scraper"])

@router.post("/scraper")
def scrape_data(request: ScraperRequest, background_tasks: BackgroundTasks, db: SessionLocal = Depends(get_db), current_user: User = Depends(get_current_user)):
    background_tasks.add_task(process_data, db, request, current_user)  # Use the instance here
    return {"message": "Your request is being processed, you will be notified when it's complete."}
