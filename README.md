# MCP Portainer API

API para gerenciar o Portainer CE.

## Configuração

1.  Crie um arquivo `.env` na raiz do projeto, baseado no `.env.example`.
2.  Preencha as variáveis de ambiente no arquivo `.env`:
    *   `PORTAINER_URL`: URL da sua instância do Portainer (ex: `http://localhost:9000`)
    *   `PORTAINER_API_KEY`: Chave de API do Portainer.

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000` e a documentação interativa em `http://127.0.0.1:8000/docs`.
# mcp-portainer
# mcp-portainer
# mcp-portainer
