from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
import uuid

# New Input Model:
class TaskCreate(BaseModel):
    title: str
    description: str
    is_completed: bool = False

# Output Model:
class Task(TaskCreate): # Inherits from TaskCreate
    id: str

#Create an instance of the FastAPI class
app = FastAPI(
    title="Project Hermers API",
    description="The unified intelligence layer for your software team.",
    version = "0.1.0"
)

# A simple in-memory database (a dictionary) to store our tasks
db: Dict[str, Task] = {}


# Define API endpoint
@app.get("/")
def get_root():
    """
    Root endpoint to welcome users and check API health.
    """
    return {"message": "Welcome to Project Hermes. The API is running."}


# Define an endpoint to create a new task
@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task_in: TaskCreate): # Notice we are using TaskCreate here for input
    """
    Receives a task creation object, generates an ID,
    and stores the new task in the database.
    """
    # Generate a unique ID
    task_id = str(uuid.uuid4())
    
    # Create the full Task object including the new ID
    new_task = Task(id=task_id, **task_in.dict())
    
    # Save to our 'database'
    db[new_task.id] = new_task
    
    print(f"Database contains: {db}") # For debugging
    
    # Return the newly created task
    return new_task


# Endpoint to get all tasks
@app.get("/tasks", response_model=List[Task])
def get_all_tasks():
    """
    Returns a list of all tasks in our database.
    """
    return list(db.values())




