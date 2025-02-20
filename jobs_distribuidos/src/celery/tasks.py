from app.celery.worker import celery, logger
import time
import random
import datetime

@celery.task(name="task_with_high_latency")
def task_with_high_latency(enqueued_time=None):
    task_id = task_with_high_latency.request.id

    # Se o tempo de enfileiramento não for passado, considera o início como agora
    if enqueued_time:
        enqueued_time = datetime.datetime.fromisoformat(enqueued_time)
    else:
        enqueued_time = datetime.datetime.utcnow()

    start_time = datetime.datetime.utcnow()

    # Calcular o tempo que a tarefa ficou na fila
    queue_wait_time = (start_time - enqueued_time).total_seconds()

    delay = random.uniform(17, 20)

    try:
        time.sleep(delay)
        logger.info(
            f"Tarefa {task_id} concluída após {delay:.2f} segundos, com {queue_wait_time:.2f} segundos na fila."
        )
        return f"Tarefa {task_id} concluída após {delay:.2f} segundos, com {queue_wait_time:.2f} segundos na fila."
    except Exception as e:
        logger.error(f"Erro na tarefa {task_id}: {e}")
        raise e