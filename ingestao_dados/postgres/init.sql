-- Criar a tabela users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Inserir três usuários iniciais
INSERT INTO users (name, email) VALUES 
('Alice Silva', 'alice@email.com'),
('Bruno Souza', 'bruno@email.com'),
('Carla Mendes', 'carla@email.com');

-- Criar o slot de replicação lógico para o Debezium
SELECT pg_create_logical_replication_slot('debezium_slot', 'pgoutput');
