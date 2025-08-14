from fastapi import FastAPI
from database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from routes import (
    user,
    category,
    consume_hist,
    budget,
    total,
    mail,
    card,
    fixed_consume,
    saving,
    income,
)
from auth import login
from scheduler import scheduler, init_scheduler
from contextlib import asynccontextmanager
from auth import login
from scheduler import scheduler, init_scheduler


@asynccontextmanager
async def lifespan(application: FastAPI):
    Base.metadata.create_all(bind=engine)
    init_scheduler()
    scheduler.start()

    try:
        yield
    finally:
        scheduler.shutdown()


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/api/users", tags=["users"])
app.include_router(category.router, prefix="/api/category", tags=["category"])
app.include_router(
    consume_hist.router, prefix="/api/consume.history", tags=["consume.history"]
)
app.include_router(budget.router, prefix="/api/budgets", tags=["budget"])
app.include_router(card.router, prefix="/api/cards", tags=["card"])
app.include_router(total.router, prefix="/api/total", tags=["total"])
app.include_router(login.router, prefix="/api", tags=["login"])
app.include_router(mail.router, prefix="/api/mail", tags=["mail"])
app.include_router(fixed_consume.router, prefix="/api/fixed", tags=["fixed_consume"])
app.include_router(saving.router, prefix="/api/saving", tags=["saving"])
app.include_router(income.router, prefix="/api/income", tags=["income"])


@app.get("/")
def read_root():
    return {"message": "Welcome DOBU"}
