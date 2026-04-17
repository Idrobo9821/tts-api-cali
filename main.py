from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response
import edge_tts

app = FastAPI(title="TTS API by Idrobo9821")

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>TTS Cali by Idrobo9821</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; background: #0d1117; color: #fff; }
                h1 { color: #58a6ff; font-size: 32px; }
                p { color: #8b949e; font-size: 18px; }
                input, select { width: 100%; padding: 14px; margin: 10px 0; font-size: 18px; border-radius: 8px; border: 1px solid #30363d; background: #161b22; color: #fff; box-sizing: border-box; }
                button { 
                    width: 100%; 
                    padding: 24px; 
                    margin: 16px 0; 
                    font-size: 28px; 
                    font-weight: 900;
                    border-radius: 12px; 
                    border: none;
                    background: #238636; 
                    color: #fff;
                    cursor: pointer; 
                    text-transform: uppercase;
                }
                button:hover { background: #2ea043; transform: scale(1.02); }
                button:disabled { background: #484f58; cursor: not-allowed; transform: scale(1); }
                #audio-player { width: 100%; margin-top: 20px; }
                #status { font-size: 16px; color: #58a6ff; min-height: 24px; }
            </style>
        </head>
        <body>
            <h1>TTS desde Cali 🫴🏻</h1>
            <p>Escribe tu frase y la convierto en audio con voz colombiana</p>
            <input type="text" id="texto" placeholder="Ej: parce, esto quedó brutal" value="vamos pibeee">
            <select id="voz">
                <option value="es-CO-GonzaloNeural">Gonzalo - Hombre</option>
                <option value="es-CO-SalomeNeural">Salomé - Mujer</option>
            </select>
            <button id="btn" onclick="generarAudio()">CREAR MI AUDIO YA</button>
            <p id="status"></p>
            <audio id="audio-player" controls style="display:none;"></audio>
            
            <script>
                async function generarAudio() {
                    const texto = document.getElementById('texto').value;
                    const voz = document.getElementById('voz').value;
                    const btn = document.getElementById('btn');
                    const status = document.getElementById('status');
                    const player = document.getElementById('audio-player');
                    
                    if (!texto) { alert('Escribe algo primero'); return; }
                    
                    btn.disabled = true;
                    btn.innerText = 'GENERANDO...';
                    status.innerText = 'Despertando servidor... si estaba dormido tarda 50 seg 🫴🏻';
                    player.style.display = 'none';
                    
                    try {
                        const response = await fetch(`/hablar?texto=${encodeURIComponent(texto)}&voz=${voz}`);
                        if (!response.ok) throw new Error('Error del servidor');
                        
                        const blob = await response.blob();
                        const url = URL.createObjectURL(blob);
                        player.src = url;
                        player.style.display = 'block';
                        player.play();
                        status.innerText = '¡Melo! Audio listo. Dale play 🔊';
                    } catch (error) {
                        status.innerText = 'Error: ' + error.message + '. Refresca e intenta de nuevo.';
                    } finally {
                        btn.disabled = false;
                        btn.innerText = 'CREAR MI AUDIO YA';
                    }
                }
            </script>
        </body>
    </html>
    """

@app.get("/hablar")
async def hablar(texto: str, voz: str = "es-CO-GonzaloNeural"):
    communicate = edge_tts.Communicate(texto, voz)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return Response(content=audio_data, media_type="audio/mpeg")