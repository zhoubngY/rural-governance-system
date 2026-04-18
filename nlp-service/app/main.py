from fastapi import FastAPI
app = FastAPI(title="NLP Service")

@app.get("/")
async def root():
    return {"message": "NLP Service for Rural Governance"}
