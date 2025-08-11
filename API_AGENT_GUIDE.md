# Guia da API para Agentes Automatizados

Este documento fornece as instruções para interagir com a API de gerenciamento do Portainer (MCP - Portainer API).

## Fonte da Verdade da API

A definição completa e autoritativa da API está disponível no esquema OpenAPI.

**URL do Esquema OpenAPI:** `http://127.0.0.1:8000/openapi.json`

Para entender como usar a API, você deve primeiro fazer uma requisição `GET` para esta URL. O JSON retornado descreve todos os recursos disponíveis, endpoints, parâmetros necessários e modelos de dados.

## Instruções de Interação

1.  **Obtenha a Especificação da API:**
    *   Faça uma requisição `GET` para `http://127.0.0.1:8000/openapi.json`.
    *   Analise o JSON para identificar os `paths` (endpoints), os métodos HTTP (`get`, `post`), e os `parameters` necessários para cada operação.

2.  **Construa suas Requisições:**
    *   Com base na especificação, construa as requisições HTTP para o endpoint desejado.
    *   Preste atenção especial aos parâmetros obrigatórios (na URL ou no corpo da requisição) e aos seus tipos de dados.

3.  **Autenticação:**
    *   Esta API atua como um wrapper para a API do Portainer. A autenticação com o Portainer (usando a `X-API-Key`) é gerenciada no lado do servidor e é transparente para você. Você não precisa enviar nenhuma chave de API.

## Endpoints Principais

Abaixo está um resumo dos principais endpoints que você encontrará na especificação. Sempre consulte o `openapi.json` para obter os detalhes mais recentes.

### Health Check
*   `GET /api/v1/health`: Verifica se a API está em execução.

### Endpoints do Portainer
*   `GET /api/v1/endpoints`: Lista os ambientes (endpoints) gerenciados pelo Portainer.

### Stacks
*   `GET /api/v1/stacks`: Lista todos os stacks.

### Contêineres
*   `GET /api/v1/containers`: Lista todos os contêineres em um endpoint específico.
    *   **Parâmetro:** `endpoint_id` (padrão: `1`)
*   `POST /api/v1/containers/{container_id}/start`: Inicia um contêiner.
*   `POST /api/v1/containers/{container_id}/stop`: Para um contêiner.
*   `POST /api/v1/containers/{container_id}/restart`: Reinicia um contêiner.

## Exemplo de Fluxo de Trabalho (Agente)

1.  **Objetivo:** Reiniciar o contêiner com ID `abc123`.
2.  **Ação 1:** `GET http://127.0.0.1:8000/openapi.json`.
3.  **Ação 2:** Analisar o JSON e encontrar o path `/api/v1/containers/{container_id}/restart` com o método `POST`.
4.  **Ação 3:** Identificar que `container_id` é um parâmetro de caminho (`in: path`).
5.  **Ação 4:** Construir e executar a requisição: `POST http://127.0.0.1:8000/api/v1/containers/abc123/restart`.
