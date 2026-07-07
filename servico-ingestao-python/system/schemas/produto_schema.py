from datetime import datetime

from pydantic import BaseModel, Field


class ProdutoNormalizado(BaseModel):
    """Representa um produto no formato padrão da aplicação."""

    id: str = Field(..., description="Identificador único do produto")
    sku: str = Field(..., description="Código SKU do produto")
    nome: str = Field(..., description="Nome do produto")
    preco_lista: float = Field(..., description="Preço original/lista do produto")
    preco_desconto: float = Field(..., description="Preço com desconto do produto")
    categoria: str = Field(..., description="Categoria do produto")
    atualizado_em: datetime = Field(..., description="Data da última atualização do produto")