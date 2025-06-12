from fastapi import FastAPI, HTTPException
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/consulta-ca/{numero_ca}")
def consulta_ca(numero_ca: str):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://consultaca.com", wait_until="networkidle")
            
            # Ajuste esses seletores se necessário
            page.fill("input#ca-number", numero_ca)
            page.click("button[type='submit']")
            page.wait_for_selector("#consultaca-container table", timeout=7000)
            
            html = page.content()
            browser.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar dados: {e}")
    
    soup = BeautifulSoup(html, "html.parser")
    tabela = soup.select_one("#consultaca-container table")
    if not tabela:
        raise HTTPException(status_code=404, detail="CA não encontrado ou layout mudou")
    
    resultado = {}
    for tr in tabela.select("tr"):
        tds = tr.select("td")
        if len(tds) == 2:
            chave = tds[0].get_text(strip=True)
            valor = tds[1].get_text(strip=True)
            resultado[chave] = valor
    
    return resultado
