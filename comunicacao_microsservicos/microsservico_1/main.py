from fastapi import FastAPI, Depends
import aio_pika
import json
import os
from sqlalchemy.orm import Session
from app.database import get_session, Base, engine
from app.models import UserModel
from uuid import uuid4
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


app = FastAPI()

RABBITMQ_URL = f"amqp://{os.environ['RABBITMQ_USER']}:{os.environ['RABBITMQ_PASS']}@{os.environ['RABBITMQ_HOST']}/"
QUEUE_NAME = "mensagens"

async def get_rabbit_connection():
    return await aio_pika.connect_robust(RABBITMQ_URL)

@app.post("/send")
async def send_message(message: str):
    connection = await get_rabbit_connection()
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps({"message": message}).encode()),
            routing_key=QUEUE_NAME
        )
    return {"status": "Message sent"}


@app.post("/criar_usuario")
async def criar_usuario(nome: str, email: str, password:str, session: Session = Depends(get_session)):
    try:
        user_model = UserModel(
            id=uuid4(),
            nome=nome,
            email=email,
            password=password
        )
        
        session.add(user_model)
        session.commit()
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    
    connection = await get_rabbit_connection()
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps({"user": {"id": str(user_model.id), "nome": user_model.nome, "email": user_model.email}}).encode()),
            routing_key=QUEUE_NAME
        )
    return {"message": "User created."}

@app.get("/listar_usuarios")
async def listar_usuarios(session: Session = Depends(get_session)):
    users_models = session.query(UserModel).all()
    return users_models

@app.on_event("startup")
async def startup_event():
    # Cria a tabela no banco de dados se ela ainda não existir
    Base.metadata.create_all(bind=engine)
    logger.info(f"Tabelas criadas com sucesso.")
    

