const queryCriarTabelaProdutos = `
  CREATE TABLE IF NOT EXISTS produtos (
    id VARCHAR(100) PRIMARY KEY,
    sku VARCHAR(100) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    preco_lista NUMERIC(12, 2) NOT NULL,
    preco_desconto NUMERIC(12, 2) NOT NULL,
    categoria VARCHAR(150) NOT NULL,
    imagem_url TEXT,
    atualizado_em TIMESTAMP NOT NULL,
    criado_em TIMESTAMP NOT NULL DEFAULT NOW()
  );
`;

module.exports = {
  queryCriarTabelaProdutos,
};