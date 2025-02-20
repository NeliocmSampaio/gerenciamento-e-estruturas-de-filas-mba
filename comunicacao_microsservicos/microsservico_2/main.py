from fastapi import FastAPI, Depends
import aio_pika
import asyncio
import json
import os
import logging
from sqlalchemy.orm import Session
from app.database import get_session, Base, engine
from app.models import UserModel
from uuid import uuid4

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

RABBITMQ_URL = f"amqp://{os.environ['RABBITMQ_USER']}:{os.environ['RABBITMQ_PASS']}@{os.environ['RABBITMQ_HOST']}/"
QUEUE_NAME = "mensagens"

async def process_incoming_message(message: aio_pika.IncomingMessage):
    message.ack()
    body = message.body
    logger.info("Received message")
    
    if body:
        parsed_message = json.loads(body)
        created_user = parsed_message['user']
        
        session: Session = next(get_session())  # Obtendo uma sessão válida
        try:
            user_model = UserModel(
                id=created_user['id'],
                nome=created_user['nome'],
                email=created_user['email']
            )
            
            session.add(user_model)
            session.commit()
            logger.info(f"Usuário {user_model.id} criado com sucesso.")
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao processar mensagem: {str(e)}")
        finally:
            session.close()
        
        logger.info(f"Message content: {parsed_message}")

async def consume(loop):
    try:
        connection = await aio_pika.connect_robust(RABBITMQ_URL, loop=loop)
        channel = await connection.channel()
        queue = await channel.declare_queue(QUEUE_NAME)
        await queue.consume(process_incoming_message, no_ack=False)
        logger.info("Waiting for messages...")
        return connection
    except Exception as e:
        logger.error(f"Erro no consumidor: {e}")
        
@app.get("/listar_usuarios")
async def listar_usuarios(session: Session = Depends(get_session)):
    users_models = session.query(UserModel).all()
    return users_models


@app.on_event("startup")
async def startup_event():
    # Cria a tabela no banco de dados se ela ainda não existir
    Base.metadata.create_all(bind=engine)
    logger.info("Tabelas criadas com sucesso.")
    
    loop = asyncio.get_running_loop()
    task = loop.create_task(consume(loop=loop))
    await task
