# Serviço de Ingestão Python

Serviço responsável por receber produtos vindos de ERPs em formatos diferentes, normalizar os dados para um modelo canônico e publicar os produtos em uma fila RabbitMQ.

Este serviço também possui uma estratégia de outbox para evitar perda de dados caso o RabbitMQ esteja indisponível no momento da ingestão.

---

## Tecnologias utilizadas

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- RabbitMQ
- uv

---

## Responsabilidades do serviço

Este serviço é responsável por:

- Receber produtos em JSON, XML e TXT.
- Converter os diferentes formatos para um modelo canônico.
- Publicar os produtos normalizados no RabbitMQ.
- Salvar produtos no outbox quando houver falha na publicação.
- Permitir reprocessamento dos produtos pendentes no outbox.

---

## Modelo canônico do produto

Após a normalização, todos os produtos seguem o mesmo formato:

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
```

---

## Estrutura principal

```txt
servico-ingestao-python/
├── system/
│   ├── api/
│   ├── constants/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── .env.example
└── README.md
```

---

## Variáveis de ambiente

Crie um arquivo `.env` com base no `.env.example`.

Exemplo para rodar localmente:

```env
NOME_APLICACAO=Serviço de Ingestão - Catálogo Multi-ERP
AMBIENTE=desenvolvimento

RABBITMQ_HOST=localhost
RABBITMQ_PORTA=5672
RABBITMQ_USUARIO=catalogo
RABBITMQ_SENHA=catalogo
RABBITMQ_FILA_PRODUTOS=catalogo.produtos.normalizados

DATABASE_URL=postgresql+psycopg://catalogo:catalogo@localhost:5432/catalogo_db
```

Quando estiver rodando via Docker Compose, os hosts devem apontar para os nomes dos serviços:

```env
RABBITMQ_HOST=rabbitmq
DATABASE_URL=postgresql+psycopg://catalogo:catalogo@postgres:5432/catalogo_db
```

---

## Como rodar com Docker

Na raiz do projeto principal, execute:

```bash
docker compose up --build
```

O serviço Python ficará disponível em:

```txt
http://localhost:8000
```

Documentação Swagger:

```txt
http://localhost:8000/docs
```

---

## Como rodar localmente com uv

Entre na pasta do serviço:

```bash
cd servico-ingestao-python
```

Instale as dependências:

```bash
uv sync
```

Suba a aplicação:

```bash
uv run uvicorn system.main:app --reload
```

Acesse:

```txt
http://localhost:8000/docs
```

---

## Como rodar localmente com pip

Entre na pasta do serviço:

```bash
cd servico-ingestao-python
```

Crie o ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente no Linux/macOS:

```bash
source .venv/bin/activate
```

Ative o ambiente no Windows:

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Suba a aplicação:

```bash
uvicorn system.main:app --reload
```

---

## Gerar ou atualizar o requirements.txt

Este projeto foi desenvolvido usando `uv`, mas o arquivo `requirements.txt` foi mantido para facilitar execução local com `pip`.

Para gerar ou atualizar o arquivo:

```bash
uv export --format requirements-txt --output-file requirements.txt --without-hashes
```

Caso sua versão do `uv` não aceite esse comando, use:

```bash
uv pip freeze > requirements.txt
```

---

## Rotas principais

### Health check

```txt
GET /api/v1/health
```

Exemplo de resposta:

```json
{
  "status": "online",
  "servico": "servico-ingestao-python"
}
```

---

### Ingestão JSON

```txt
POST /api/v1/ingestao/json
```

Exemplo de payload:

```json
{
  "items": [
    {
      "productCode": "A-778",
      "skuCode": "NB-DELL-INS-15",
      "description": "Notebook Dell Inspiron 15",
      "value": 3500.90,
      "discountValue": 3200.00,
      "department": "TI",
      "updated_at": "2026-01-10T10:14:30Z"
    }
  ]
}
```

---

### Ingestão XML

```txt
POST /api/v1/ingestao/xml
```

Header:

```txt
Content-Type: application/xml
```

Exemplo de payload:

```xml
<products>
    <product>
        <id>1001</id>
        <sku>NB-DELL-INS-15</sku>
        <name>Notebook Dell Inspiron 15</name>
        <price>
            <list>3500.90</list>
            <discount>3200.00</discount>
        </price>
        <category>Informática</category>
        <lastUpdate>2026-01-10T10:15:00</lastUpdate>
    </product>
</products>
```

---

### Ingestão TXT

```txt
POST /api/v1/ingestao/txt
```

Header:

```txt
Content-Type: text/plain
```

Exemplo de payload:

```txt
0000001001NB-DELL-INS-15Notebook Dell Inspiron 15        00003500900000320000INFORMATICA       20260110101500
```

---

## Retorno esperado da ingestão

Quando o RabbitMQ está disponível:

```json
{
  "mensagem": "Produtos JSON processados e publicados com sucesso.",
  "status": "PUBLICADO",
  "origem": "JSON",
  "quantidade_normalizada": 1,
  "quantidade_publicada": 1,
  "quantidade_pendente": 0,
  "fila": "catalogo.produtos.normalizados"
}
```

Quando o RabbitMQ está indisponível:

```json
{
  "mensagem": "Produtos JSON normalizados, mas não publicados. Eles foram salvos para reprocessamento.",
  "status": "PENDENTE_REPROCESSAMENTO",
  "origem": "JSON",
  "quantidade_normalizada": 1,
  "quantidade_publicada": 0,
  "quantidade_pendente": 1,
  "fila": "catalogo.produtos.normalizados"
}
```

---

## Tratamento de erros de payload

As rotas de ingestão tratam erros de normalização dos payloads e retornam HTTP 400 quando o JSON, XML ou TXT recebido estiver inválido.

Exemplo:

```json
{
  "detail": "Payload JSON inválido: 'productCode'"
}
```

Isso evita que falhas de formato sejam confundidas com falhas internas da aplicação.

---

## Outbox

Para tratar falhas na comunicação assíncrona, foi implementado o padrão Outbox no serviço de ingestão.

Caso o RabbitMQ esteja indisponível no momento do recebimento dos produtos, os dados normalizados são salvos na tabela `outbox_produtos` com status pendente.

Depois, por meio de uma rota de reprocessamento, esses registros podem ser publicados novamente na fila, evitando perda de dados e garantindo maior consistência no fluxo.

---

## Rota de reprocessamento

```txt
POST /api/v1/reprocessamento/outbox-produtos?limite=100
```

Exemplo de resposta:

```json
{
  "mensagem": "Reprocessamento do outbox executado.",
  "total_pendentes_encontrados": 1,
  "total_publicados": 1,
  "total_com_erro": 0
}
```

---

## Tabela outbox_produtos

A tabela `outbox_produtos` armazena produtos que foram normalizados, mas não puderam ser publicados na fila.

Campos principais:

```txt
id
origem
payload
status
tentativas
erro
criado_em
atualizado_em
publicado_em
```

Os campos `criado_em` e `atualizado_em` são preenchidos automaticamente pelo SQLAlchemy por meio do model `OutboxProduto`.

---

## Observação sobre criação de tabelas

Para simplificar a execução do teste técnico, as tabelas são criadas automaticamente na inicialização da aplicação.

---
