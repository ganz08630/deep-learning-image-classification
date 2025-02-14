import React, { useState, useEffect } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";
import { motion } from "framer-motion";

const App = () => {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [logs, setLogs] = useState(() => JSON.parse(localStorage.getItem("logs")) || []);
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(true);

  useEffect(() => {
    localStorage.setItem("logs", JSON.stringify(logs));
  }, [logs]);

  const logMessage = (message) => {
    const timestamp = new Date().toLocaleTimeString();
    const newLog = `${timestamp} - ${message}`;
    setLogs((prev) => [...prev, newLog]);
    console.log(newLog);
    sendLogToServer(newLog);
  };

  const sendLogToServer = async (log) => {
    try {
      await axios.post("http://127.0.0.1:8000/logs/", { log });
    } catch (error) {
      console.error("Не вдалося відправити лог на сервер");
    }
  };

  const clearLogs = () => {
    setLogs([]);
    localStorage.removeItem("logs");
    logMessage("🗑 Логи очищено");
  };

  const { getRootProps, getInputProps } = useDropzone({
    accept: "image/*",
    onDrop: (acceptedFiles) => {
      const file = acceptedFiles[0];
      setImage(file);
      setPreview(URL.createObjectURL(file));
      logMessage("📤 Фото вибрано");
    },
  });

  const handleUpload = async () => {
    if (!image) {
      alert("❌ Виберіть зображення!");
      return;
    }

    setLoading(true);
    logMessage("📡 Відправка фото...");

    const formData = new FormData();
    formData.append("file", image);

    try {
      const response = await axios.post("http://127.0.0.1:8000/predict/", formData);
      logMessage(`✅ Результат: ${response.data.prediction} (${response.data.confidence})`);
    } catch (error) {
      if (error.response) {
        logMessage(`❌ Серверна помилка (${error.response.status}): ${error.response.data.error || "Невідома помилка"}`);
        alert(`❌ Серверна помилка (${error.response.status}): ${error.response.data.error || "Невідома помилка"}`);
      } else if (error.request) {
        logMessage("❌ Сервер не відповідає. Перевірте, чи він запущений.");
        alert("❌ Сервер не відповідає. Переконайтеся, що він запущений і доступний.");
      } else {
        logMessage(`❌ Помилка налаштування запиту: ${error.message}`);
        alert(`❌ Помилка запиту: ${error.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`min-h-screen flex flex-col items-center justify-center ${darkMode ? "bg-gray-900 text-white" : "bg-white text-gray-900"}`}>
      <button
        onClick={() => setDarkMode(!darkMode)}
        className="absolute top-4 right-4 bg-blue-500 px-4 py-2 text-white rounded hover:bg-blue-600"
      >
        {darkMode ? "☀ Світла тема" : "🌙 Темна тема"}
      </button>

      <h1 className="text-3xl font-bold mb-6">Класифікація зображень</h1>

      <motion.div
        {...getRootProps()}
        className="border-2 border-dashed border-gray-500 p-8 rounded-lg flex flex-col items-center justify-center cursor-pointer hover:bg-gray-700 transition w-80"
        whileHover={{ scale: 1.05 }}
      >
        <input {...getInputProps()} />
        {preview ? (
          <img src={preview} alt="preview" className="w-40 mt-2 rounded-lg shadow-lg" />
        ) : (
          <p className="text-lg">Перетягніть фото сюди або натисніть</p>
        )}
      </motion.div>

      <button
        onClick={handleUpload}
        className={`mt-4 px-6 py-3 text-white rounded transition ${
          loading ? "bg-gray-600 cursor-not-allowed" : "bg-green-500 hover:bg-green-600"
        }`}
        disabled={loading}
      >
        {loading ? "⏳ Обробка..." : "🚀 Відправити"}
      </button>

      <div className="mt-6 w-80">
        <h2 className="text-xl font-semibold mb-2">📜 Логи</h2>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="p-4 bg-gray-800 text-white rounded shadow-lg"
        >
          {logs.map((log, index) => (
            <motion.p
              key={index}
              className="py-1"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.2 }}
            >
              {log}
            </motion.p>
          ))}
        </motion.div>
        <button
          onClick={clearLogs}
          className="mt-4 bg-red-500 px-4 py-2 text-white rounded hover:bg-red-600 w-full"
        >
          🗑 Очистити логи
        </button>
      </div>
    </div>
  );
};

export default App;
