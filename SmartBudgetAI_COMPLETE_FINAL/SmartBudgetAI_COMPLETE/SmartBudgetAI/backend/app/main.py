from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.db.session import Base,engine
from app.api.transactions import router as transactions_router
from app.api.budget import router as budget_router
from app.api.analytics import router as analytics_router
from app.api.dashboard import router as dashboard_router
from app.api.chat import router as chat_router

settings=get_settings()
Base.metadata.create_all(bind=engine)
app=FastAPI(title=settings.app_name,version='1.0.0',description='AI-assisted personal budgeting and expense analytics')
origins=[x.strip() for x in settings.cors_origins.split(',') if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
app.include_router(transactions_router,prefix=settings.api_prefix)
app.include_router(budget_router,prefix=settings.api_prefix)
app.include_router(analytics_router,prefix=settings.api_prefix)
app.include_router(dashboard_router,prefix=settings.api_prefix)
app.include_router(chat_router,prefix=settings.api_prefix)
@app.get('/health')
def health(): return {'status':'ok','service':settings.app_name}
