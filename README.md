# Web Scraper e Bot do Telegram

Este projeto consiste em um web scraper que automatiza a extração de informações de um site específico (requer login) e um bot do Telegram para interagir com esse scraper.

## Funcionalidades

- **Web Scraper (`advanced_scraper.py`):**
  - Realiza login em um site.
  - Busca informações com base em um termo fornecido.
  - Extrai dados como Original Identifier, Nome, Sobrenome, Endereço 1, Endereço 2 e Nome da Campanha.
  - Lida com campos vazios ou ausentes.
- **Bot do Telegram (`bot.py`):**
  - Permite que usuários busquem informações no site através de comandos do Telegram.
  - Formata os resultados de forma amigável.
  - Possui um menu de comandos para facilitar a interação.

## Configuração do Ambiente

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd scrapper
    ```

2.  **Execute o script de instalação:**
    Este script irá criar um ambiente virtual, instalar todas as dependências Python e baixar os navegadores necessários para o Playwright.

    **Para Windows:**
    ```bash
    install.bat
    ```
    **Para Linux/macOS:**
    ```bash
    chmod +x install.sh
    ./install.sh
    ```

3.  **Crie o arquivo `.env`:**
    Na raiz do projeto, crie um arquivo chamado `.env` e adicione suas credenciais do site:
    ```
    SITE_USERNAME="seu_usuario_do_site"
    SITE_PASSWORD="sua_senha_do_site"
    ```
    **Importante:** Este arquivo `.env` já está configurado para ser ignorado pelo Git (`.gitignore`), garantindo que suas credenciais não sejam versionadas.

4.  **Obtenha o Token do Bot do Telegram:**
    - Abra o Telegram e procure por `@BotFather`.
    - Envie o comando `/newbot` e siga as instruções para criar seu bot.
    - O BotFather lhe fornecerá um `token de API` (ex: `1234567890:ABCdEfGhIjKlMnOpQrStUvWxYz-123456`).

5.  **Configure o `bot.py`:**
    - Abra o arquivo `bot.py`.
    - Substitua `TELEGRAM_TOKEN = 'SEU_TOKEN_AQUI'` pelo token que você recebeu do BotFather.

## Configuração do Scraper (`advanced_scraper.py`)

Abra o arquivo `advanced_scraper.py` e preencha as seguintes variáveis com os seletores e URLs corretos do site alvo. Use as ferramentas de desenvolvedor do seu navegador (F12) para inspecionar os elementos e obter os seletores CSS ou XPath.

- `LOGIN_URL`: URL da página de login.
- `SEARCH_PAGE_URL`: URL da página de pesquisa após o login.
- `USERNAME_SELECTOR`: Seletor CSS/XPath para o campo de usuário.
- `PASSWORD_SELECTOR`: Seletor CSS/XPath para o campo de senha.
- `LOGIN_BUTTON_SELECTOR`: Seletor CSS/XPath para o botão de login.
- `SEARCH_INPUT_SELECTOR`: Seletor CSS/XPath para o campo de busca.
- `SEARCH_BUTTON_SELECTOR`: Seletor CSS/XPath para o botão de busca.
- `DETAILS_BUTTON_SELECTOR`: Seletor CSS/XPath para o botão de detalhes na tabela de resultados.
- `MODAL_SELECTOR`: Seletor CSS/XPath para o contêiner do modal de detalhes.
- `ORIGINAL_IDENTIFIER_SELECTOR`: Seletor XPath para o campo 'Original Identifier' dentro do modal.
- `ADDRESS_1_SELECTOR`: Seletor XPath para o campo 'Address 1' dentro do modal.
- `ADDRESS_2_SELECTOR`: Seletor XPath para o campo 'Address 2' dentro do modal.
- `FIRST_NAME_SELECTOR`: Seletor XPath para o campo 'First Name' dentro do modal.
- `LAST_NAME_SELECTOR`: Seletor XPath para o campo 'Last Name' dentro do modal.
- `CAMPAIGN_NAME_SEARCH_RESULT_SELECTOR`: Seletor CSS para o campo 'Campaign Name' na tabela de resultados (antes de abrir o modal).

## Como Executar

1.  **Ative o ambiente virtual:**

    **Para Windows:**
    ```bash
    call venv\Scripts\activate
    ```
    **Para Linux/macOS:**
    ```bash
    source venv/bin/activate
    ```

2.  **Inicie o bot do Telegram:**
    ```bash
    python bot.py
    ```
    O bot ficará rodando e aguardando comandos.

3.  **Interaja com o bot no Telegram:**
    - Envie `/start` para uma mensagem de boas-vindas.
    - Envie `/buscar <termo_de_busca>` (ex: `/buscar 12313`) para que o bot execute o scraper e retorne as informações.

## Depuração

Se o scraper não estiver funcionando como esperado, você pode executar o `advanced_scraper.py` diretamente para depurar:

```bash
# Ative o ambiente virtual primeiro (veja acima)
python advanced_scraper.py
```

O script está configurado com `headless=False` para que você possa ver o navegador automatizado em ação. Em caso de erros, ele tentará salvar screenshots (`timeout_error.png`, `error_screenshot.png`) para ajudar na depuração.
