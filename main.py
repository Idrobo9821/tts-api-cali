from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
import edge_tts
import uuid

app = FastAPI(title="TTS API by Idrobo9821")

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>TTS Cali by Idrobo9821</title>
            <style>
                body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; background: #0d1117; color: #fff; }
                h1 { color: #58a6ff; }
                input, select, button { width: 100%; padding: 12px; margin: 8px 0; font-size: 16px; border-radius: 6px; border: 1px solid #30363d; background: #161b22; color: #fff; }
                button { background: #238636; cursor: pointer; font-weight: bold; }
                button:hover { background: #2ea043; }
            </style>
        </head>
        <body>
            <h1>TTS desde Cali 🫴🏻</h1>
            <p>Escribe algo y te lo convierto en audio con voz colombiana</p>
            <input type="text" id="texto" placeholder="Ej: Idrobo conquistó el mundo">
            <select id="voz">
                <option value="es-CO-GonzaloNeural">Gonzalo - Hombre</option>
                <option value="es-CO-SalomeNeural">Salomé - Mujer</option>
            </select>
            <button onclick="generarAudio()">Generar Audio</button>
            <p id="status"></p>
            <script>
                async function generarAudio() {
                    const texto = document.getElementById('texto').value;
                    const voz = document.getElementById('voz').value;
                    if (!texto) { alert('Escribe algo primero'); return; }
                    document.getElementById('status').innerText = 'Generando audio...';
                    window.location.href = /hablar?texto=${encodeURIComponent(texto)}&voz=${voz};
                }
            </script>
        </body>
    </html>
    """

@app.get("/hablar")
async def hablar(texto: str, voz: str = "es-CO-GonzaloNeural"):
    nombre_archivo = f"audio_{uuid.uuid4()}.mp3"
    communicate = edge_tts.Communicate(texto, voz)
    await communicate.save(nombre_archivo)
    return FileResponse(nombre_archivo, media_type="audio/mpeg", filename=nombre_archivo)