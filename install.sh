#!/bin/bash

# Cria e ativa o ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instala as dependências do Python
pip install -r requirements.txt

# Instala os navegadores do Playwright
python3 -m playwright install

echo ""
echo "Instalação concluída! Para ativar o ambiente virtual, execute:"
echo "source venv/bin/activate"
echo ""
echo "Para rodar o bot, execute:"
echo "python3 bot.py"
echo ""
