from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from PIL import Image
import logging

from src.inference.predict import predict_image  # Використовуємо нашу оновлену функцію

# Налаштовуємо логування
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# Додаємо CORS Middleware (для кросдоменного доступу)
origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://61ca-178-158-205-89.ngrok-free.app",  # Якщо використовуєш ngrok
    "*",  # Тимчасово можна залишити "*", щоб перевірити, але краще явно вказувати фронтенд URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Можна додати PUT, DELETE, якщо треба
    allow_headers=["Content-Type", "Authorization"],
)

# Додаємо обробку OPTIONS-запитів для CORS
@app.options("/predict/")
async def preflight():
    return JSONResponse(content={"message": "CORS preflight OK"}, status_code=200)

# Папка фронтенду
FRONTEND_PATH = Path("/app/src/frontend")

# Додаємо роздачу статичних файлів (CSS, JS)
app.mount("/frontend", StaticFiles(directory=FRONTEND_PATH), name="frontend")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    index_file = FRONTEND_PATH / "index.html"
    if index_file.exists():
        return index_file.read_text()
    return HTMLResponse("<h1>Frontend not found</h1>", status_code=404)

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        image = Image.open(file.file)
        predicted_class, confidence = predict_image(image)

        logging.info(f"Processed image: {file.filename}, Prediction: {predicted_class}, Confidence: {confidence:.2f}%")

        return JSONResponse({
            "filename": file.filename,
            "prediction": predicted_class,
            "confidence": f"{confidence:.2f}%"
        })
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

# Якщо запускаєш сервер у локальному середовищі
# Використовуй `uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload`
