from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io
from src.inference.predict import predict_image  # Використовуємо нашу оновлену функцію

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Додаємо роздачу статичних файлів (CSS, JS, фронтенд)
app.mount("/frontend", StaticFiles(directory="/app/src/frontend"), name="frontend")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("/app/src/frontend/index.html", "r") as f:
        return f.read()

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        # Завантажуємо зображення у форматі PIL
        image = Image.open(io.BytesIO(await file.read()))

        # Викликаємо функцію передбачення
        predicted_class, confidence = predict_image(image)

        return {
            "filename": file.filename,
            "prediction": predicted_class,
            "confidence": f"{confidence:.2f}%"  # Відображаємо впевненість
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
