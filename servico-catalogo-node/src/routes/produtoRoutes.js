const express = require("express");

const {
  consultarProdutoPorId,
  consultarProdutos,
} = require("../services/produtoService");

const router = express.Router();

router.get("/produtos", async (req, res) => {
  /**
   * Lista produtos do catálogo consolidado.
   *
   * Filtros opcionais:
   * - sku
   * - categoria
   */

  try {
    const filtros = {
      sku: req.query.sku,
      categoria: req.query.categoria,
    };

    const produtos = await consultarProdutos(filtros);

    return res.json({
      quantidade: produtos.length,
      produtos,
    });
  } catch (erro) {
    return res.status(500).json({
      mensagem: "Erro ao consultar produtos.",
      erro: erro.message,
    });
  }
});

router.get("/produtos/:id", async (req, res) => {
  /**
   * Consulta um produto específico pelo ID.
   */

  try {
    const produto = await consultarProdutoPorId(req.params.id);

    if (!produto) {
      return res.status(404).json({
        mensagem: "Produto não encontrado.",
      });
    }

    return res.json(produto);
  } catch (erro) {
    return res.status(500).json({
      mensagem: "Erro ao consultar produto.",
      erro: erro.message,
    });
  }
});

module.exports = router;