const express = require("express");

const env = require("./config/env");
const healthRoutes = require("./routes/healthRoutes");
const bancoRoutes = require("./routes/bancoRoutes");

const app = express();

app.use(express.json());

app.use("/api/v1", healthRoutes);
app.use("/api/v1", bancoRoutes);

app.listen(env.porta, () => {
  console.log(`${env.nomeServico} rodando na porta ${env.porta}`);
});