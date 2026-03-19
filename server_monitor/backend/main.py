

from datetime import datetime
import re
import httpx
import psutil

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator

#  Налаштування LHM 
LHM_URL = "http://localhost:8085/data.json"


#  Парсер data.json 
def _parse_value(raw: str) -> float | None:
    """
    Перетворює рядок LHM типу "42,8 °C" або "2,0 %" у float.
    LHM використовує кому як десятковий роздільник (локаль Windows).
    """
    if not raw or raw.strip() in ("", "-", "NaN °C"):
        return None
    # Залишаємо лише цифри, крапку/кому і мінус
    cleaned = re.sub(r"[^\d,.\-]", "", raw).replace(",", ".")
    try:
        return float(cleaned)
    except ValueError:
        return None


def _walk(node: dict, callback):
    """Рекурсивно обходить дерево LHM і викликає callback для кожного вузла."""
    callback(node)
    for child in node.get("Children", []):
        _walk(child, callback)


async def _fetch_lhm() -> dict:
    """
    Отримує data.json від LHM і витягує потрібні сенсори.

    Структура дерева LHM:
      Computer → Hardware → Category (Temperatures/Load/Data) → Sensor

    SensorId для Ryzen 5 3600:
      /amdcpu/0/temperature/2  → Core (Tctl/Tdie)
      /amdcpu/0/load/0         → CPU Total

    SensorId для RX 5700:
      /gpu-amd/0/load/0        → GPU Core
      /gpu-amd/0/temperature/0 → GPU Core temp
      /gpu-amd/0/temperature/1 → GPU Memory temp
      /gpu-amd/0/smalldata/0   → GPU Memory Used (MB)
      /gpu-amd/0/smalldata/2   → GPU Memory Total (MB)
    """
    result = {
        "lhm_active":    False,
        "cpu_name":      "AMD Ryzen 5 3600",
        "gpu_name":      "AMD Radeon RX 5700",
        "cpu_temp":      None,
        "cpu_load":      None,
        "gpu_load":      None,
        "gpu_temp":      None,
        "gpu_mem_temp":  None,
        "gpu_mem_used":  None,   # MB
        "gpu_mem_total": None,   # MB
    }

    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            r = await client.get(LHM_URL)
            r.raise_for_status()
            data = r.json()
        result["lhm_active"] = True
    except Exception:
        return result

    # Збираємо назви Hardware
    def collect_names(node: dict):
        sid = node.get("SensorId", "")
        text = node.get("Text", "")
        if sid == "" and "/amdcpu/0" == node.get("HardwareId", ""):
            result["cpu_name"] = text
        if sid == "" and "/gpu-amd/0" == node.get("HardwareId", ""):
            result["gpu_name"] = text

    # Збираємо значення сенсорів за SensorId
    TARGET_SENSORS = {
        "/amdcpu/0/temperature/2": "cpu_temp",
        "/amdcpu/0/load/0":        "cpu_load",
        "/gpu-amd/0/load/0":       "gpu_load",
        "/gpu-amd/0/temperature/0":"gpu_temp",
        "/gpu-amd/0/temperature/1":"gpu_mem_temp",
        "/gpu-amd/0/smalldata/0":  "gpu_mem_used",
        "/gpu-amd/0/smalldata/2":  "gpu_mem_total",
    }

    def collect_sensors(node: dict):
        collect_names(node)
        sid = node.get("SensorId", "")
        if sid in TARGET_SENSORS:
            val = _parse_value(node.get("RawValue", ""))
            if val is not None:
                result[TARGET_SENSORS[sid]] = round(val, 1)

    _walk(data, collect_sensors)
    return result


# App
app = FastAPI(title="AMD Ryzen 5 3600 + RX 5700 Monitor", version="5.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse("../frontend/index.html")


#  In-memory state 
_state = {
    "server_name":   "DESKTOP-RH8T79Q",
    "cpu_threshold": 75,
    "poll_interval": 2,
}

_metrics_history: list[dict] = []


# Збір метрик 
async def _get_metrics() -> dict:
    # RAM через psutil (LHM теж є, але psutil надійніший)
    ram       = psutil.virtual_memory()
    ram_pct   = round(ram.percent, 1)
    ram_used  = round(ram.used  / (1024 ** 3), 2)
    ram_total = round(ram.total / (1024 ** 3), 2)

    lhm = await _fetch_lhm()

    # CPU load: LHM точніший на Windows, psutil як запасний варіант
    cpu_load = lhm["cpu_load"]
    if cpu_load is None:
        cpu_load = round(psutil.cpu_percent(interval=0.1), 1)

    # VRAM %
    gpu_mem_pct: float | None = None
    if lhm["gpu_mem_used"] and lhm["gpu_mem_total"] and lhm["gpu_mem_total"] > 0:
        gpu_mem_pct = round(lhm["gpu_mem_used"] / lhm["gpu_mem_total"] * 100, 1)

    index = _metrics_history[-1]["index"] + 1 if _metrics_history else 0

    return {
        "index":         index,
        "timestamp":     datetime.now().strftime("%H:%M:%S"),
        # CPU
        "cpu":           cpu_load,
        "cpu_name":      lhm["cpu_name"],
        "cpu_temp":      lhm["cpu_temp"],
        # RAM
        "ram":           ram_pct,
        "ram_used_gb":   ram_used,
        "ram_total_gb":  ram_total,
        # GPU
        "gpu":           lhm["gpu_load"],
        "gpu_temp":      lhm["gpu_temp"],
        "gpu_mem_temp":  lhm["gpu_mem_temp"],
        "gpu_mem":       gpu_mem_pct,
        "gpu_mem_used":  lhm["gpu_mem_used"],
        "gpu_mem_total": lhm["gpu_mem_total"],
        "gpu_name":      lhm["gpu_name"],
        "gpu_available": lhm["lhm_active"] and lhm["gpu_load"] is not None,
        "lhm_active":    lhm["lhm_active"],
    }


# Pydantic 
class StateUpdate(BaseModel):
    server_name:   str = Field(..., min_length=1, max_length=64)
    cpu_threshold: int = Field(..., ge=0, le=100)
    poll_interval: int = Field(..., ge=1, le=60)

    @field_validator("server_name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Назва сервера не може бути порожньою")
        return v.strip()

    @field_validator("cpu_threshold")
    @classmethod
    def threshold_range(cls, v: int) -> int:
        if not (0 <= v <= 100):
            raise ValueError("Поріг CPU має бути 0–100")
        return v

    @field_validator("poll_interval")
    @classmethod
    def interval_range(cls, v: int) -> int:
        if not (1 <= v <= 60):
            raise ValueError("Інтервал має бути 1–60 секунд")
        return v


# Endpoints 
@app.get("/api/state")
async def get_state():
    return {"status": "ok", "data": _state}


@app.post("/api/state")
async def post_state(body: StateUpdate):
    global _state
    _state = body.model_dump()
    return {"status": "ok", "data": _state, "message": "Налаштування збережено"}


@app.get("/api/metrics")
async def get_metrics():
    point = await _get_metrics()
    _metrics_history.append(point)
    if len(_metrics_history) > 50:
        _metrics_history.pop(0)
    return {
        "status":        "ok",
        "threshold":     _state["cpu_threshold"],
        "gpu_available": point["gpu_available"],
        "lhm_active":    point["lhm_active"],
        "cpu_name":      point["cpu_name"],
        "data":          _metrics_history[-30:],
    }


@app.get("/api/info")
async def get_info():
    """Діагностика: перевір що LHM підключений і сенсори читаються."""
    lhm = await _fetch_lhm()
    return {
        "lhm_active":   lhm["lhm_active"],
        "lhm_url":      LHM_URL,
        "cpu_name":     lhm["cpu_name"],
        "cpu_temp":     lhm["cpu_temp"],
        "cpu_load":     lhm["cpu_load"],
        "gpu_name":     lhm["gpu_name"],
        "gpu_load":     lhm["gpu_load"],
        "gpu_temp":     lhm["gpu_temp"],
        "gpu_mem_used": lhm["gpu_mem_used"],
        "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 1),
        "cpu_threads":  psutil.cpu_count(logical=True),
    }
