from fastapi import FastAPI
from fastapi.responses import FileResponse
import edge_tts
import uuid

app = FastAPI(title="TTS API by Idrobo9821")

@app.get("/")
def healthcheck():
    return {
        "status": "ok", 
        "dev": "Idrobo9821",
        "ciudad": "Cali",
        "msg": "API de voz funcionando"
    }

@app.get("/hablar")
async def hablar(texto: str, voz: str = "es-CO-GonzaloNeural"):
    """Convierte texto a voz. Voces: es-CO-GonzaloNeural, es-CO-SalomeNeural"""
    nombre_archivo = f"audio_{uuid.uuid4()}.mp3"
    
    communicate = edge_tts.Communicate(texto, voz)
    await communicate.save(nombre_archivo)
    
    return FileResponse(nombre_archivo, media_type="audio/mpeg", filename=nombre_archivo)