
import requests
from bs4 import BeautifulSoup

def scrape_quotes():
    """
    Acessa o site quotes.toscrape.com e extrai as citações,
    autores e tags da primeira página.
    """
    url = 'http://quotes.toscrape.com'
    try:
        response = requests.get(url)
        # Gera um erro se a requisição não for bem-sucedida (código de status diferente de 2xx)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a página: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontra todos os contêineres de citação
    quotes_divs = soup.find_all('div', class_='quote')

    scraped_data = []
    for quote_div in quotes_divs:
        # Extrai o texto da citação
        text = quote_div.find('span', class_='text').get_text(strip=True)
        
        # Extrai o autor
        author = quote_div.find('small', class_='author').get_text(strip=True)
        
        # Extrai as tags
        tags_div = quote_div.find('div', class_='tags')
        tags = [tag.get_text(strip=True) for tag in tags_div.find_all('a', class_='tag')]
        
        scraped_data.append({
            'text': text,
            'author': author,
            'tags': tags
        })
        
    return scraped_data

if __name__ == '__main__':
    quotes = scrape_quotes()
    if quotes:
        for q in quotes:
            print(f"Citação: {q['text']}")
            print(f"Autor: {q['author']}")
            print(f"Tags: {', '.join(q['tags'])}")
            print("-" * 20)
