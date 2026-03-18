require('dotenv').config(); // Завантажуємо змінні з .env
const mysql = require("mysql2");

const db = mysql.createPool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASS,
    database: process.env.DB_NAME,
    port: process.env.DB_PORT,
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0,
    // Додатковий захист від SQL ін'єкцій на рівні драйвера
    multipleStatements: false 
});

db.getConnection((err, connection) => {
    if (err) {
        console.error("❌ Помилка безпечного підключення до БД:", err.message);
    } else {
        console.log("✅ База даних підключена через захищені змінні оточення!");
        connection.release();
    }
});

module.exports = db;