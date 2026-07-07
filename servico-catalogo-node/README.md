# Serviço de Catálogo Node.js

Serviço responsável por consumir produtos normalizados da fila RabbitMQ, persistir o catálogo consolidado no PostgreSQL e disponibilizar uma API de consulta externa.

Também possui um painel simples para vincular imagens aos produtos manualmente.

---

## Tecnologias utilizadas

- Node.js
- Express
- PostgreSQL
- RabbitMQ
- amqplib
- pg
- dotenv

---

## Responsabilidades do serviço

Este serviço é responsável por:

- Consumir produtos normalizados da fila RabbitMQ.
- Salvar produtos no PostgreSQL.
- Atualizar produtos somente quando a mensagem recebida for mais recente.
- Ignorar mensagens duplicadas ou antigas.
- Disponibilizar API de consulta do catálogo.
- Disponibilizar painel simples de mídia.
- Permitir vínculo manual de URL de imagem aos produtos.

---

## Estrutura principal

```txt
servico-catalogo-node/
├── src/
│   ├── config/
│   ├── consumers/
│   ├── database/
│   │   └── queries/
│   ├── public/
│   ├── repositories/
│   ├── routes/
│   ├── services/
│   ├── templates/
│   └── server.js
├── Dockerfile
├── package.json
├── package-lock.json
├── .env.example
└── README.md
```

---

## Variáveis de ambiente

Crie um arquivo `.env` com base no `.env.example`.

Exemplo para rodar localmente:

```env
PORTA=3000
NOME_SERVICO=Serviço de Catálogo - Multi-ERP
AMBIENTE=desenvolvimento

DATABASE_URL=postgresql://catalogo:catalogo@localhost:5432/catalogo_db

RABBITMQ_URL=amqp://catalogo:catalogo@localhost:5672
RABBITMQ_FILA_PRODUTOS=catalogo.produtos.normalizados
RABBITMQ_CONSUMER_TAG=servico-catalogo-node-produtos
```

Quando estiver rodando via Docker Compose, os hosts devem apontar para os nomes dos serviços:

```env
DATABASE_URL=postgresql://catalogo:catalogo@postgres:5432/catalogo_db
RABBITMQ_URL=amqp://catalogo:catalogo@rabbitmq:5672
```

---

## Como rodar com Docker

Na raiz do projeto principal, execute:

```bash
docker compose up --build
```

O serviço Node.js ficará disponível em:

```txt
http://localhost:3000

```

---

## Como rodar localmente

Entre na pasta do serviço:

```bash
cd servico-catalogo-node
```

Instale as dependências:

```bash
npm install
```

Suba em modo desenvolvimento:

```bash
npm run dev
```

Ou suba em modo simples/produção local:

```bash
npm start
```

---

## Observação sobre dependências externas

Para rodar localmente, é necessário que PostgreSQL e RabbitMQ estejam disponíveis.

Uma forma simples é subir apenas as dependências pela raiz do projeto:

```bash
docker compose up -d postgres rabbitmq
```

Depois rode o serviço Node.js localmente com:

```bash
npm run dev
```

---

## Inicialização das dependências

Em ambiente Docker, o PostgreSQL e o RabbitMQ podem levar alguns segundos para ficarem prontos, mesmo depois dos containers iniciarem.

Por isso, o serviço possui tentativa automática de inicialização das dependências.

Fluxo esperado:

```txt
Node sobe na porta 3000
↓
Tenta inicializar o banco
↓
Se o PostgreSQL ainda não estiver pronto, tenta novamente
↓
Depois inicia o consumer do RabbitMQ
↓
Se o RabbitMQ ainda não estiver pronto, tenta novamente
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
  "servico": "servico-catalogo-node"
}
```

---

### Health check do banco

```txt
GET /api/v1/banco/health
```

Exemplo de resposta:

```json
{
  "status": "online",
  "banco": "postgresql",
  "resultado": {
    "teste": 1
  }
}
```

---

## API de produtos

### Listar todos os produtos

```txt
GET /api/v1/produtos
```

Exemplo de resposta:

```json
{
  "quantidade": 1,
  "produtos": [
    {
      "id": "A-778",
      "sku": "NB-DELL-INS-15",
      "nome": "Notebook Dell Inspiron 15",
      "preco_lista": "3500.90",
      "preco_desconto": "3200.00",
      "categoria": "TI",
      "imagem_url": null,
      "atualizado_em": "2026-01-10T10:14:30.000Z",
      "criado_em": "2026-07-06T22:00:00.000Z"
    }
  ]
}
```

---

### Buscar produto por ID

```txt
GET /api/v1/produtos/:id
```

Exemplo:

```txt
GET /api/v1/produtos/A-778
```

---

### Filtrar por SKU

```txt
GET /api/v1/produtos?sku=NB-DELL-INS-15
```

---

### Filtrar por categoria

```txt
GET /api/v1/produtos?categoria=TI
```

---

## Regra de atualização dos produtos

Quando uma mensagem de produto chega pela fila, o serviço aplica a seguinte regra:

```txt
Se o produto não existir:
    cria o produto

Se o produto existir e a mensagem recebida for mais recente:
    atualiza o produto

Se o produto existir e a mensagem recebida for antiga ou igual:
    ignora a mensagem
```

Essa regra usa o campo `atualizado_em`.

Isso evita que mensagens duplicadas ou fora de ordem sobrescrevam dados mais recentes.

---

## Consumer RabbitMQ

O serviço consome mensagens da fila:

```txt
catalogo.produtos.normalizados
```

Cada mensagem deve conter um produto normalizado:

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

Quando o processamento ocorre com sucesso, a mensagem recebe `ack`.

Caso ocorra erro no processamento, a mensagem recebe `nack`.

---

## Painel de mídia

O painel de mídia permite vincular manualmente uma URL de imagem a um produto.

Acesse:

```txt
http://localhost:3000/api/v1/painel-midias
```

O formulário solicita:

```txt
ID do produto
URL da imagem
```

Ao enviar, o serviço atualiza o campo `imagem_url` na tabela `produtos`.

---

## Produtos sem imagem

Também existe uma tela simples para visualizar produtos que ainda não possuem imagem vinculada:

```txt
http://localhost:3000/api/v1/painel-midias/produtos-sem-imagem
```

Essa tela ajuda o usuário a saber quais produtos ainda precisam de imagem.

---

## Vincular imagem via API

Também é possível vincular imagem usando JSON:

```txt
POST /api/v1/produtos/imagem
```

Body:

```json
{
  "produto_id": "A-778",
  "imagem_url": "https://exemplo.com/notebook.jpg"
}
```

Exemplo de resposta:

```json
{
  "mensagem": "Imagem vinculada ao produto com sucesso.",
  "produto": {
    "id": "A-778",
    "sku": "NB-DELL-INS-15",
    "nome": "Notebook Dell Inspiron 15",
    "preco_lista": "3500.90",
    "preco_desconto": "3200.00",
    "categoria": "TI",
    "imagem_url": "https://exemplo.com/notebook.jpg",
    "atualizado_em": "2026-01-10T10:14:30.000Z",
    "criado_em": "2026-07-06T22:00:00.000Z"
  }
}
```

---

## Tabela produtos

A tabela `produtos` armazena o catálogo consolidado.

Campos principais:

```txt
id
sku
nome
preco_lista
preco_desconto
categoria
imagem_url
atualizado_em
criado_em
```

---

## Observação sobre criação de tabelas

Para simplificar a execução do teste técnico, a tabela `produtos` é criada automaticamente na inicialização do serviço.

Em um ambiente produtivo, o ideal seria utilizar migrations versionadas.

---
