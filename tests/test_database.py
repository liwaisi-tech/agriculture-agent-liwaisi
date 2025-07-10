# Mock de datos para la tabla temp_humidity
mock_temp_humidity = [
    {
        "id": 1,
        "device_mac_address": "AA:BB:CC:DD:EE:01",
        "temperature": 28.5,
        "humidity": 75.2,
        "created_at": "2024-06-01T10:00:00Z"
    },
    {
        "id": 2,
        "device_mac_address": "AA:BB:CC:DD:EE:01",
        "temperature": 29.1,
        "humidity": 74.8,
        "created_at": "2024-06-01T11:00:00Z"
    },
    {
        "id": 3,
        "device_mac_address": "AA:BB:CC:DD:EE:02",
        "temperature": 27.9,
        "humidity": 80.0,
        "created_at": "2024-06-01T10:30:00Z"
    }
]

# Ejemplo de test usando el mock

def test_mock_temp_humidity_structure():
    for row in mock_temp_humidity:
        assert "id" in row
        assert "device_mac_address" in row
        assert "temperature" in row
        assert "humidity" in row
        assert "created_at" in row
        assert isinstance(row["temperature"], float)
        assert isinstance(row["humidity"], float)

def calcular_promedios_temp_humidity(rows):
    if not rows:
        return {"avg_temperature": None, "avg_humidity": None}
    avg_temp = sum(r["temperature"] for r in rows) / len(rows)
    avg_hum = sum(r["humidity"] for r in rows) / len(rows)
    return {"avg_temperature": avg_temp, "avg_humidity": avg_hum}

def test_calcular_promedios_temp_humidity():
    resultado = calcular_promedios_temp_humidity(mock_temp_humidity)
    assert abs(resultado["avg_temperature"] - ((28.5 + 29.1 + 27.9) / 3)) < 0.01
    assert abs(resultado["avg_humidity"] - ((75.2 + 74.8 + 80.0) / 3)) < 0.01
