from fastapi import FastAPI
from celery.result import AsyncResult
from app.celery.worker import celery
from app.celery.tasks import task_with_high_latency
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CeleryTaskOutputDto(BaseModel):
    state: str  # Estado da tarefa
    output: Optional[str] = None  # Resultado, se disponível

app = FastAPI()

@app.post("/start-task")
def start_task():
    """Inicia uma tarefa Celery e retorna seu ID."""
    task = task_with_high_latency.delay(enqueued_time=datetime.utcnow().isoformat())
    return {"task_id": task.id}

@app.get("/task-status/{task_id}")
def task_status(task_id: str):
    """Obtém o status de uma tarefa pelo ID."""
    task_result = AsyncResult(task_id, app=celery)
    return CeleryTaskOutputDto(state=task_result.state, output=task_result.info)
