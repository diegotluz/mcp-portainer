from app.config import settings

print("--- Teste de Variáveis de Ambiente ---")
print(f"URL do Portainer: '{settings.portainer_url}'")
print(f"Chave da API: '{settings.portainer_api_key[:4]}... (primeiros 4 caracteres)'")
print("-------------------------------------")
