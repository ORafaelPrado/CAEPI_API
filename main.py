from fastapi import FastAPI, HTTPException
from ftp_utils import get_ca_info

app = FastAPI()

@app.get("/ca/{ca_number}")
def consultar_ca(ca_number: str):
    data = get_ca_info(ca_number)
    if data:
        return data
    raise HTTPException(status_code=404, detail="CA não encontrado")