# Consolidador de Catálogo Multi-ERP

Projeto desenvolvido para consolidar produtos recebidos de múltiplos ERPs em formatos diferentes, normalizando os dados e disponibilizando um catálogo único para consulta.

## Objetivo

A solução recebe produtos em JSON, XML e TXT, normaliza os dados para um modelo canônico, publica as mensagens em uma fila RabbitMQ e persiste o catálogo consolidado em PostgreSQL.

Também possui um painel simples para vincular imagens aos produtos manualmente.

## Arquitetura

A solução possui dois serviços independentes:

### Serviço 1 — Ingestão Python

Responsável por:

- Receber payloads de ERPs em JSON, XML e TXT
- Normalizar os produtos
- Publicar os produtos normalizados no RabbitMQ
- Salvar mensagens pendentes em outbox caso o RabbitMQ esteja indisponível
- Permitir reprocessamento do outbox

Tecnologias:

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- RabbitMQ

### Serviço 2 — Catálogo Node.js

Responsável por:

- Consumir produtos normalizados da fila RabbitMQ
- Persistir os produtos no PostgreSQL
- Evitar sobrescrita com dados antigos usando `atualizado_em`
- Disponibilizar API de consulta de produtos
- Disponibilizar painel simples de mídia

Tecnologias:

- Node.js
- Express
- PostgreSQL
- RabbitMQ

## Modelo canônico do produto

```json
{
  "id": "A-778",
  "sku": "NB-DELL-INS-15",
  "nome": "Notebook Dell Inspiron 15",
  "preco_lista": 3500.90,
  "preco_desconto": 3200.00,
  "categoria": "TI",
  "atualizado_em": "2026-01-10T10:14:30Z"
}