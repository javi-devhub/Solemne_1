from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests
from datetime import datetime

app = FastAPI()


@app.get("/time")
def get_time():
    # Intento de scraping
    url = "https://www.horaoficial.cl/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    bloque = soup.find(string=lambda text: text and "CHILE CONTINENTAL" in text)

    if not bloque:
        # Fallback: usar hora local si no se encuentra el bloque
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {"time": now, "source": "local"}

    hora_texto = bloque.strip().replace("CHILE CONTINENTAL", "").strip()

    meses = {
        "ENERO": "01",
        "FEBRERO": "02",
        "MARZO": "03",
        "ABRIL": "04",
        "MAYO": "05",
        "JUNIO": "06",
        "JULIO": "07",
        "AGOSTO": "08",
        "SEPTIEMBRE": "09",
        "OCTUBRE": "10",
        "NOVIEMBRE": "11",
        "DICIEMBRE": "12",
    }

    try:
        partes = hora_texto.split()
        hora = partes[0]
        dia = partes[2]
        mes = meses[partes[3].upper()]
        año = partes[4].replace(",", "")

        fecha_hora = f"{año}-{mes}-{dia} {hora}"
        return {"time": fecha_hora, "source": "scraping"}

    except Exception as e:
        # Si falla el parsing, también usar hora local
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {"time": now, "source": "local", "error": str(e)}
