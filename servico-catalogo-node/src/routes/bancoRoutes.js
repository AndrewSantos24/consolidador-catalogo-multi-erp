const express = require("express");

const { executarConsulta } = require("../database/connection");

const router = express.Router();

router.get("/banco/health", async (req, res) => {
  /**
   * Verifica se a conexão com o banco PostgreSQL está funcionando.
   */

  try {
    const resultado = await executarConsulta("SELECT 1 AS teste");

    return res.json({
      status: "online",
      banco: "postgresql",
      resultado: resultado.rows[0],
    });
  } catch (erro) {
    return res.status(503).json({
      status: "indisponivel",
      banco: "postgresql",
      erro: erro.message,
    });
  }
});

module.exports = router;