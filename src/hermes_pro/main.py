from fastapi import FastAPI
from hermes_pro.api import endpoints

app = FastAPI(
    title="Hermes Pro API",
    description="The Agentic Engineering OS",
    version="2.0.0"
)

# Include the router from our endpoints file
app.include_router(endpoints.router, prefix="/api/v1")

@app.get("/")
def get_root():
    return {"message": "Hermes Pro is alive!"}