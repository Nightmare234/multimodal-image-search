from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router import search_router

app = FastAPI(title="Image Search API")

# Cho phép frontend gọi (React, v.v.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hoặc chỉ domain của bạn
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_router.router)

@app.get("/")
def root():
    return {"message": "Image Search API is running 🚀"}

