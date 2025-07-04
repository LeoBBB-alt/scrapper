@echo off

REM Cria e ativa o ambiente virtual
python -m venv venv
call venv\Scripts\activate

REM Instala as dependências do Python
pip install -r requirements.txt

REM Instala os navegadores do Playwright
python -m playwright install

echo.
echo Instalação concluída! Para ativar o ambiente virtual, execute:
echo call venv\Scripts\activate
echo.
echo Para rodar o bot, execute:
echo py bot.py

pause
