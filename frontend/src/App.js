import React, { useState } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";
import { motion } from "framer-motion";

const App = () => {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(true);

  const { getRootProps, getInputProps } = useDropzone({
    accept: "image/*",
    onDrop: (acceptedFiles) => {
      const file = acceptedFiles[0];
      setImage(file);
      setPreview(URL.createObjectURL(file));
      setLogs((prev) => [...prev, "📤 Фото вибрано"]);
    },
  });

  const handleUpload = async () => {
    if (!image) {
      alert("❌ Виберіть зображення!");
      return;
    }

    setLoading(true);
    setLogs((prev) => [...prev, "📡 Відправка фото..."]);

    const formData = new FormData();
    formData.append("file", image);

    try {
      const response = await axios.post("http://127.0.0.1:8000/predict/", formData);
      setLogs((prev) => [...prev, `✅ Результат: ${response.data.prediction} (${response.data.confidence})`]);
    } catch (error) {
      setLogs((prev) => [...prev, "❌ Помилка при відправці"]);
      alert("❌ Сталася помилка! Переконайтеся, що сервер запущений.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`min-h-screen flex flex-col items-center justify-center ${darkMode ? "bg-gray-900 text-white" : "bg-white text-gray-900"}`}>
      {/* Тема */}
      <button
        onClick={() => setDarkMode(!darkMode)}
        className="absolute top-4 right-4 bg-blue-500 px-4 py-2 text-white rounded hover:bg-blue-600"
      >
        {darkMode ? "☀ Світла тема" : "🌙 Темна тема"}
      </button>

      <h1 className="text-3xl font-bold mb-6">Класифікація зображень</h1>

      {/* Dropzone */}
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

      {/* Кнопка відправки */}
      <button
        onClick={handleUpload}
        className={`mt-4 px-6 py-3 text-white rounded transition ${
          loading ? "bg-gray-600 cursor-not-allowed" : "bg-green-500 hover:bg-green-600"
        }`}
        disabled={loading}
      >
        {loading ? "⏳ Обробка..." : "🚀 Відправити"}
      </button>

      {/* Логи */}
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
      </div>
    </div>
  );
};

export default App;
