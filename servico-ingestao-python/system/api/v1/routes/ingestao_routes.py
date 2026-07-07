from sqlalchemy.orm import Session
from fastapi import APIRouter, Body, Depends, HTTPException
from system.core.errors import AppError

from system.services.servico_ingestao_service import (
    processar_ingestao_json,
    processar_ingestao_txt,
    processar_ingestao_xml,
)
from system.database.connection import obter_sessao


router = APIRouter(prefix="/ingestao", tags=["Ingestão"])


@router.post("/json")
def receber_produtos_json(payload: dict = Body(...),sessao: Session = Depends(obter_sessao)) -> dict:
    """Recebe produtos em JSON e retorna os produtos normalizados.

    Exemplo de payload recebido:

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

    :param dict payload: Payload JSON enviado pelo ERP
    :param Session sessao: Sessão ativa do banco de dados
    :return: Quantidade e lista de produtos normalizados
    """
    try:
        return processar_ingestao_json(payload,sessao)
    except AppError as erro:
        raise HTTPException(
            status_code=erro.status_code,
            detail=erro.mensagem,
        ) from erro


@router.post("/xml")
def receber_produtos_xml(payload_xml: str = Body(..., media_type="application/xml"),sessao: Session = Depends(obter_sessao)) -> dict:
    """Recebe produtos em XML e retorna os produtos normalizados.

    Exemplo de payload recebido:


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
    

    :param str payload_xml: Payload XML enviado pelo ERP
    :param Session sessao: Sessão ativa do banco de dados
    :return: Quantidade e lista de produtos normalizados
    """
    try:
        return processar_ingestao_xml(payload_xml,sessao)
    except AppError as erro:
        raise HTTPException(
            status_code=erro.status_code,
            detail=erro.mensagem,
        ) from erro


@router.post("/txt")
def receber_produtos_txt(payload_txt: str = Body(..., media_type="text/plain"),sessao: Session = Depends(obter_sessao)) -> dict:
    """Recebe produtos em TXT e retorna os produtos normalizados.

    Exemplo de payload recebido:

    0000001001NB-DELL-INS-15Notebook Dell Inspiron 15        00003500900000320000INFORMATICA       20260110101500

    Layout esperado:

    - ID no início da linha
    - SKU e nome no trecho inicial
    - preço lista com 10 dígitos
    - preço desconto com 10 dígitos
    - categoria em texto
    - data final no formato YYYYMMDDHHMMSS

    :param str payload_txt: Payload TXT enviado pelo ERP
    :param Session sessao: Sessão ativa do banco de dados
    :return: Quantidade e lista de produtos normalizados
    """
    try:
        return processar_ingestao_txt(payload_txt,sessao)
    except AppError as erro:
        raise HTTPException(
            status_code=erro.status_code,
            detail=erro.mensagem,
        ) from erro