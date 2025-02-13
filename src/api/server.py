from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from PIL import Image
import logging

from src.inference.predict import predict_image  # Використовуємо нашу оновлену функцію

# Налаштовуємо логування
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Додаємо CORS Middleware (для кросдоменного доступу)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # У production краще вказати конкретний домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
