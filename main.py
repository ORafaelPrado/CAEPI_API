from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/consulta-ca/{numero_ca}")
def consulta_ca(numero_ca: str):
    url = f"https://consultaca.com/{numero_ca}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Erro ao acessar o site: {str(e)}")

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        dados = {
            "Validade": soup.find("td", string="Validade").find_next_sibling("td").get_text(strip=True),
            "Situação": soup.find("td", string="Situação").find_next_sibling("td").get_text(strip=True),
            "Nome": soup.find("td", string="Nome").find_next_sibling("td").get_text(strip=True),
            "Fabricante": soup.find("td", string="Fabricante").find_next_sibling("td").get_text(strip=True)
        }
        return dados
    except AttributeError:
        raise HTTPException(status_code=404, detail="CA não encontrado ou layout da página mudou.")
