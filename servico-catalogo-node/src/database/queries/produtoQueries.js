const queryBuscarProdutoPorId = `
  SELECT
    id,
    sku,
    nome,
    preco_lista,
    preco_desconto,
    categoria,
    imagem_url,
    atualizado_em,
    criado_em
  FROM produtos
  WHERE id = $1;
`;

const queryInserirProduto = `
  INSERT INTO produtos (
    id,
    sku,
    nome,
    preco_lista,
    preco_desconto,
    categoria,
    atualizado_em
  )
  VALUES ($1, $2, $3, $4, $5, $6, $7);
`;

const queryAtualizarProduto = `
  UPDATE produtos
  SET
    sku = $2,
    nome = $3,
    preco_lista = $4,
    preco_desconto = $5,
    categoria = $6,
    atualizado_em = $7
  WHERE id = $1;
`;

const queryListarProdutos = `
  SELECT
    id,
    sku,
    nome,
    preco_lista,
    preco_desconto,
    categoria,
    imagem_url,
    atualizado_em,
    criado_em
  FROM produtos
  WHERE
    ($1::TEXT IS NULL OR sku = $1)
    AND ($2::TEXT IS NULL OR categoria = $2)
  ORDER BY nome ASC;
`;

const queryBuscarProdutoCompletoPorId = `
  SELECT
    id,
    sku,
    nome,
    preco_lista,
    preco_desconto,
    categoria,
    imagem_url,
    atualizado_em,
    criado_em
  FROM produtos
  WHERE id = $1;
`;

const queryAtualizarImagemProduto = `
  UPDATE produtos
  SET imagem_url = $2
  WHERE id = $1
  RETURNING
    id,
    sku,
    nome,
    preco_lista,
    preco_desconto,
    categoria,
    imagem_url,
    atualizado_em,
    criado_em;
`;

const queryListarProdutosSemImagem = `
  SELECT
    id,
    sku,
    nome,
    categoria,
    imagem_url
  FROM produtos
  WHERE imagem_url IS NULL OR imagem_url = ''
  ORDER BY nome ASC;
`;

module.exports = {
  queryBuscarProdutoPorId,
  queryInserirProduto,
  queryAtualizarProduto,
  queryListarProdutos,
  queryBuscarProdutoCompletoPorId,
  queryAtualizarImagemProduto,
  queryListarProdutosSemImagem
};