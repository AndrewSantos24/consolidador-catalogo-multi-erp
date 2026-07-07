const express = require("express");

const router = express.Router();

router.get("/health", (req, res) => {
  return res.json({
    status: "online",
    servico: "servico-catalogo-node",
  });
});

module.exports = router;