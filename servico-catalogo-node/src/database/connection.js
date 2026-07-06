const { Pool } = require("pg");

const env = require("../config/env");

const pool = new Pool({
  connectionString: env.databaseUrl,
});

async function executarConsulta(texto, parametros = []) {
  /**
   * Executa uma consulta no banco PostgreSQL.
   *
   * @param {string} texto - SQL que será executado
   * @param {Array} parametros - Parâmetros da consulta
   * @returns {Promise<object>} Resultado da consulta
   */

  return pool.query(texto, parametros);
}

module.exports = {
  pool,
  executarConsulta,
};