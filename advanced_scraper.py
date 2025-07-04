import asyncio
from playwright.async_api import async_playwright, TimeoutError
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente
load_dotenv()

# --- CONFIGURAÇÃO (PREENCHA ESTAS INFORMAÇÕES) ---
LOGIN_URL = 'https://br11.td.commpeak.com/search/lead'
# ATENÇÃO: Verifique se esta URL está correta. Geralmente é a URL completa da página após o login.
SEARCH_PAGE_URL = 'https://br11.td.commpeak.com/search/lead'

USERNAME = os.environ.get('SITE_USERNAME', 'SEU_USUARIO_AQUI')
PASSWORD = os.environ.get('SITE_PASSWORD', 'SUA_SENHA_AQUI')

# --- SELETORES CSS / XPATH (Use a ferramenta de inspecionar elemento) ---
USERNAME_SELECTOR = '#username'
PASSWORD_SELECTOR = '#password'
LOGIN_BUTTON_SELECTOR = '#submit'

SEARCH_INPUT_SELECTOR = '#lead_id'
SEARCH_BUTTON_SELECTOR = '#search > div.card-body > div > div.pull-left.float-start.text-start > input'

# Seletor para o botão de detalhes que abre o modal.
DETAILS_BUTTON_SELECTOR = 'a[onclick^="openDetailsWindow("]'

# Seletor para o contêiner do modal que aparece.
MODAL_SELECTOR = 'div.modal.fade.show'

# --- Seletores para as informações DENTRO do modal ---
# Usando XPath relativo para encontrar o texto da label e pegar o valor na célula seguinte.
ORIGINAL_IDENTIFIER_SELECTOR = '//td[normalize-space()="Original Identifier"]/following-sibling::td/span'
ADDRESS_1_SELECTOR = '//td[normalize-space()="Address 1"]/following-sibling::td/span'
ADDRESS_2_SELECTOR = '//td[normalize-space()="Address 2"]/following-sibling::td/span'
FIRST_NAME_SELECTOR = '//td[normalize-space()="First Name"]/following-sibling::td/span'
LAST_NAME_SELECTOR = '//td[normalize-space()="Last Name"]/following-sibling::td/span'

# Novo seletor para o Campaign Name na tabela de resultados
CAMPAIGN_NAME_SEARCH_RESULT_SELECTOR = 'td.lead-campaigns'

async def fetch_site_details(search_term: str) -> dict | str:
    """
    Automatiza o login, busca e extrai 6 campos (5 do modal, 1 da tabela) de um site.
    Retorna um dicionário com os dados ou uma string de erro.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            # --- ETAPA 1: LOGIN ---
            print(f"Acessando: {LOGIN_URL}")
            await page.goto(LOGIN_URL)
            await page.fill(USERNAME_SELECTOR, USERNAME)
            await page.fill(PASSWORD_SELECTOR, PASSWORD)
            await page.click(LOGIN_BUTTON_SELECTOR)
            await page.wait_for_url(SEARCH_PAGE_URL, timeout=15000)
            print("Login bem-sucedido.")

            # --- ETAPA 2: BUSCA ---
            print(f"Buscando por: '{search_term}'")
            await page.fill(SEARCH_INPUT_SELECTOR, search_term)
            await page.click(SEARCH_BUTTON_SELECTOR)
            await page.wait_for_selector(DETAILS_BUTTON_SELECTOR, timeout=10000)
            print("Resultados carregados.")

            # Extrair Campaign Name da tabela de resultados antes de clicar no modal
            campaign_name_element = await page.query_selector(CAMPAIGN_NAME_SEARCH_RESULT_SELECTOR)
            campaign_name = await campaign_name_element.inner_text() if campaign_name_element else "Não encontrado"
            print(f"Campaign Name (da tabela): {campaign_name}")

            # --- ETAPA 3: ABRIR MODAL ---
            await page.click(DETAILS_BUTTON_SELECTOR)
            print("Botão de detalhes clicado.")
            modal = await page.wait_for_selector(MODAL_SELECTOR, timeout=5000)
            print("Modal encontrado.")

            # --- ETAPA 4: EXTRAIR DADOS DO MODAL ---
            async def get_info(selector, name):
                element = await modal.query_selector(f"xpath={selector}")
                if not element:
                    print(f"AVISO: Elemento para '{name}' não encontrado com o seletor: {selector}")
                    return "Não encontrado"
                text = await element.inner_text()
                if not text.strip():
                    print(f"AVISO: Elemento para '{name}' encontrado, mas vazio com o seletor: {selector}")
                    return "Não encontrado"
                return text

            identifier = await get_info(ORIGINAL_IDENTIFIER_SELECTOR, "Original Identifier")
            addr1 = await get_info(ADDRESS_1_SELECTOR, "Address 1")
            addr2 = await get_info(ADDRESS_2_SELECTOR, "Address 2")
            first_name = await get_info(FIRST_NAME_SELECTOR, "First Name")
            last_name = await get_info(LAST_NAME_SELECTOR, "Last Name")

            result_data = {
                'original_identifier': identifier.strip(),
                'address_1': addr1.strip(),
                'address_2': addr2.strip(),
                'first_name': first_name.strip(),
                'last_name': last_name.strip(),
                'campaign_name': campaign_name.strip() # Adicionado Campaign Name aqui
            }
            
            await browser.close()
            return result_data

        except TimeoutError as e:
            error_message = f"Erro de timeout: um elemento demorou para aparecer. Verifique seus seletores e a velocidade do site. Detalhes: {e}"
            print(error_message)
            await page.screenshot(path='timeout_error.png')
            print("Screenshot 'timeout_error.png' salvo para depuração.")
            await browser.close()
            return error_message
        except Exception as e:
            error_message = f"Erro inesperado: {e}"
            print(error_message)
            await page.screenshot(path='error_screenshot.png')
            print("Screenshot 'error_screenshot.png' salvo para depuração.")
            await browser.close()
            return error_message

async def main():
    """Função para testar o script diretamente."""
    if any(val.startswith(('SUA', 'SELETOR', 'URL_')) for val in globals().values() if isinstance(val, str)):
        print("ERRO: Preencha todas as URLs e Seletores no topo do arquivo antes de executar.")
        return

    test_search_term = "23914" # Coloque um termo de teste válido
    result = await fetch_site_details(test_search_term)
    
    print("\n--- RESULTADO FINAL ---")
    if isinstance(result, dict):
        print(f"  Original Identifier: {result['original_identifier']}")
        print(f"  Address 1: {result['address_1']}")
        print(f"  Address 2: {result['address_2']}")
        print(f"  First Name: {result['first_name']}")
        print(f"  Last Name: {result['last_name']}")
        print(f"  Campaign Name: {result['campaign_name']}")
    else:
        print(f"  Erro: {result}")

if __name__ == '__main__':
    asyncio.run(main())