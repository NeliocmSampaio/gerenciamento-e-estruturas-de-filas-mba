# README - Ingestão de Dados

Este módulo faz parte da aula de Filas do curso de MBA em Engenharia de Software da USP ESALQ e demonstra o uso de filas em pipelines de ingestão e processamento de dados.

## Requisitos

Antes de iniciar, certifique-se de ter instalado em seu ambiente:

- **Docker**
- **Extensão do Docker para VS Code**

## Configuração Adicional

O procedimento a seguir é necessário para o serviço do Elasticsearch funcionar corretamente e deverá ser feito antes de iniciar os containers:

### Linux/macOS:

```sh
sudo sysctl -w vm.max_map_count=262144
```

### Windows (PowerShell, dentro do WSL):

```sh
wsl -d docker-desktop sysctl -w vm.max_map_count=262144
```

## Como Executar

1. Acesse a pasta do módulo:
   ```sh
   cd ingestao_de_dados
   ```
2. Inicie os containers com o Docker Compose:
   ```sh
   docker-compose up -d
   ```
3. Para interromper a execução, utilize:
   ```sh
   docker-compose down -v
   ```

## Observações

Se houver necessidade de ajustes adicionais, eles serão incluídos neste arquivo.
