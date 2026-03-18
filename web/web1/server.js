const express = require("express");
const bodyParser = require("body-parser");
const session = require("express-session");
const bcrypt = require("bcrypt");
const csrf = require("csurf");
const helmet = require("helmet");
const xss = require("xss");
const cookieParser = require("cookie-parser");
const db = require("./database/db");
const https = require("https");

const app = express();

app.use(helmet({ contentSecurityPolicy: false }));
app.use(express.static("public"));
app.use(cookieParser());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.use(session({
    secret: "secure_delivery_session_67890",
    resave: false,
    saveUninitialized: true,
    cookie: { httpOnly: true, secure: false }
}));

const csrfProtection = csrf({ cookie: true });

// ─── Розрахунок часу маршруту через OSRM ─────────────────────────────────────
function getRouteDurationMs(fromLat, fromLng, toLat, toLng) {
    return new Promise((resolve) => {
        const url = `https://router.project-osrm.org/route/v1/driving/${fromLng},${fromLat};${toLng},${toLat}?overview=false`;
        https.get(url, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try { resolve(JSON.parse(data).routes[0].duration * 1000); }
                catch { resolve(null); }
            });
        }).on('error', () => resolve(null));
    });
}

// ─── CSRF ─────────────────────────────────────────────────────────────────────
app.get("/api/get-token", csrfProtection, (req, res) => {
    res.json({ csrfToken: req.csrfToken() });
});

// ─── АВТЕНТИФІКАЦІЯ ───────────────────────────────────────────────────────────
app.post("/register", async (req, res) => {
    const username = xss(req.body.username);
    const email    = xss(req.body.email);
    const password = await bcrypt.hash(req.body.password, 10);
    db.query("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", [username, email, password], (err) => {
        if (err) return res.status(500).send("Помилка реєстрації: " + err.message);
        res.redirect("/login.html");
    });
});

app.post("/login", (req, res) => {
    const username = xss(req.body.username);
    db.query("SELECT * FROM users WHERE username = ?", [username], async (err, results) => {
        if (err || results.length === 0) return res.send("Невірні дані");
        const match = await bcrypt.compare(req.body.password, results[0].password);
        if (match) { req.session.user = username; res.redirect("/map.html"); }
        else res.send("Невірні дані");
    });
});

// ─── ВОДІЇ ────────────────────────────────────────────────────────────────────
app.get("/api/drivers", (req, res) => {
    db.query("SELECT * FROM drivers", (err, results) => {
        if (err) return res.status(500).json({ error: "DB Error" });
        res.json(results || []);
    });
});

app.post("/api/drivers", csrfProtection, (req, res) => {
    const name = xss(req.body.name || '').trim();
    const lat  = req.body.lat ? parseFloat(req.body.lat) : null;
    const lng  = req.body.lng ? parseFloat(req.body.lng) : null;
    if (!name) return res.status(400).json({ error: "Ім'я обов'язкове" });
    db.query("INSERT INTO drivers (name, status, lat, lng) VALUES (?, 'idle', ?, ?)", [name, lat, lng], (err, result) => {
        if (err) return res.status(500).json({ error: err.message });
        res.json({ id: result.insertId, name, status: 'idle', lat, lng });
    });
});

app.post("/api/drivers/:id/position", (req, res) => {
    const { lat, lng } = req.body;
    db.query("UPDATE drivers SET lat = ?, lng = ? WHERE id = ?", [lat, lng, req.params.id], (err) => {
        if (err) return res.status(500).json({ error: err.message });
        res.sendStatus(200);
    });
});

// ─── ДОСТАВКИ (активні) ───────────────────────────────────────────────────────
app.get("/api/deliveries", (req, res) => {
    const sql = `
        SELECT d.*, dr.name as driver_name
        FROM deliveries d
        LEFT JOIN drivers dr ON d.driver_id = dr.id
        WHERE d.status != 'delivered'
        ORDER BY d.id DESC
    `;
    db.query(sql, (err, results) => {
        if (err) return res.status(500).json({ error: "DB Error" });
        res.json(results || []);
    });
});

app.post("/api/deliveries", csrfProtection, (req, res) => {
    const s_name  = xss(req.body.sender_name);
    const s_phone = xss(req.body.sender_phone);
    const p_addr  = xss(req.body.pickup_address);
    const r_name  = xss(req.body.receiver_name);
    const r_phone = xss(req.body.receiver_phone);
    const d_addr  = xss(req.body.dropoff_address);
    const p_lat   = req.body.pickup_lat  ? parseFloat(req.body.pickup_lat)  : null;
    const p_lng   = req.body.pickup_lng  ? parseFloat(req.body.pickup_lng)  : null;
    const d_lat   = req.body.dropoff_lat ? parseFloat(req.body.dropoff_lat) : null;
    const d_lng   = req.body.dropoff_lng ? parseFloat(req.body.dropoff_lng) : null;

    const sql = `INSERT INTO deliveries
        (sender_name, sender_phone, pickup_address, receiver_name, receiver_phone, dropoff_address,
         pickup_lat, pickup_lng, dropoff_lat, dropoff_lng, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')`;

    db.query(sql, [s_name, s_phone, p_addr, r_name, r_phone, d_addr, p_lat, p_lng, d_lat, d_lng], (err, result) => {
        if (err) return res.status(500).json({ error: "DB Error" });
        res.json({ id: result.insertId });
    });
});

// ─── АРХІВ ────────────────────────────────────────────────────────────────────
app.get("/api/archive", (req, res) => {
    const sql = `
        SELECT d.*, dr.name as driver_name
        FROM deliveries d
        LEFT JOIN drivers dr ON d.driver_id = dr.id
        WHERE d.status = 'delivered'
        ORDER BY d.id DESC
        LIMIT 100
    `;
    db.query(sql, (err, results) => {
        if (err) return res.status(500).json({ error: "DB Error" });
        res.json(results || []);
    });
});

// Перевести конкретне замовлення в архів вручну
app.post("/api/deliveries/:id/archive", csrfProtection, (req, res) => {
    const id = parseInt(req.params.id);
    db.query("UPDATE deliveries SET status = 'delivered' WHERE id = ?", [id], (err) => {
        if (err) return res.status(500).json({ error: err.message });
        // Звільнити водія якщо був призначений
        db.query("SELECT driver_id FROM deliveries WHERE id = ?", [id], (e2, rows) => {
            if (!e2 && rows.length && rows[0].driver_id) {
                db.query("UPDATE drivers SET status = 'idle' WHERE id = ?", [rows[0].driver_id]);
            }
        });
        res.json({ success: true });
    });
});

// ─── ПРИЗНАЧЕННЯ ВОДІЯ + ETA + АВТОАРХІВ ─────────────────────────────────────
app.post("/api/deliveries/:id/assign", csrfProtection, async (req, res) => {
    const deliveryId = parseInt(req.params.id);
    const driverId   = parseInt(req.body.driver_id);
    if (!driverId) return res.status(400).json({ error: "Не вказано водія" });

    db.query(
        `SELECT d.pickup_lat, d.pickup_lng, d.dropoff_lat, d.dropoff_lng,
                dr.lat as driver_lat, dr.lng as driver_lng
         FROM deliveries d JOIN drivers dr ON dr.id = ?
         WHERE d.id = ?`,
        [driverId, deliveryId],
        async (err, rows) => {
            if (err || !rows.length) return res.status(500).json({ error: "Не знайдено" });
            const row = rows[0];

            db.query("UPDATE deliveries SET driver_id = ?, status = 'assigned' WHERE id = ?", [driverId, deliveryId]);
            db.query("UPDATE drivers SET status = 'delivering' WHERE id = ?", [driverId]);

            let etaText = null;
            let totalMs = null;

            if (row.driver_lat && row.driver_lng && row.pickup_lat && row.dropoff_lat) {
                const ms1 = await getRouteDurationMs(row.driver_lat, row.driver_lng, row.pickup_lat,  row.pickup_lng);
                const ms2 = await getRouteDurationMs(row.pickup_lat, row.pickup_lng, row.dropoff_lat, row.dropoff_lng);

                if (ms1 !== null && ms2 !== null) {
                    totalMs  = ms1 + ms2;
                    etaText  = `${Math.round(totalMs / 60000)} хв`;
                    console.log(`🚗 Доставка #${deliveryId}: ${Math.round(ms1/60000)} хв до забору + ${Math.round(ms2/60000)} хв до доставки = ${Math.round(totalMs/60000)} хв`);

                    // Автоархів після завершення маршруту
                    setTimeout(() => {
                        db.query("UPDATE drivers    SET status = 'idle'      WHERE id = ?", [driverId]);
                        db.query("UPDATE deliveries SET status = 'delivered' WHERE id = ?", [deliveryId]);
                        console.log(`✅ Доставка #${deliveryId} → архів, водій #${driverId} звільнений`);
                    }, totalMs);
                } else {
                    // Координати є, але OSRM не відповів — архівуємо через 2 години як fallback
                    totalMs = null;
                    scheduleAutoArchive(deliveryId, driverId, 2 * 60 * 60 * 1000);
                }
            } else {
                // Немає координат — архівуємо через 2 години
                scheduleAutoArchive(deliveryId, driverId, 2 * 60 * 60 * 1000);
            }

            res.json({ success: true, eta: etaText, totalMs });
        }
    );
});

function scheduleAutoArchive(deliveryId, driverId, delayMs) {
    console.log(`⏰ Доставка #${deliveryId}: автоархів через ${Math.round(delayMs/60000)} хв (немає координат)`);
    setTimeout(() => {
        db.query("UPDATE drivers    SET status = 'idle'      WHERE id = ?", [driverId]);
        db.query("UPDATE deliveries SET status = 'delivered' WHERE id = ?", [deliveryId]);
    }, delayMs);
}

// ─── Фоновий процес: кожні 10 хв архівує assigned-замовлення без таймера ─────
// (на випадок якщо сервер перезапустився і setTimeout загубився)
setInterval(() => {
    const sql = `
        SELECT id, driver_id FROM deliveries
        WHERE status = 'assigned'
        AND updated_at < DATE_SUB(NOW(), INTERVAL 3 HOUR)
    `;
    db.query(sql, (err, rows) => {
        if (err || !rows.length) return;
        rows.forEach(row => {
            db.query("UPDATE deliveries SET status = 'delivered' WHERE id = ?", [row.id]);
            if (row.driver_id) db.query("UPDATE drivers SET status = 'idle' WHERE id = ?", [row.driver_id]);
            console.log(`🔄 Авто-архів (timeout): доставка #${row.id}`);
        });
    });
}, 10 * 60 * 1000);

const port = 3000;
app.listen(port, () => console.log(`🛡️ Secure server: http://localhost:${port}`));