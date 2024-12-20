from fastapi import FastAPI, HTTPException
import pandas as pd

# Crear instancia de la aplicación
app = FastAPI(title="API de Vacunación contra el Sarampión en Panamá")

# Cargar los datos
data_file = "vacunacion_panama.csv"  # Archivo con datos descargados
data = pd.read_csv(data_file)

# Transformar datos a una lista de diccionarios
data_records = data.to_dict(orient="records")

@app.get("/")
def home():
    return {
        "message": "API de Vacunación contra el Sarampión en Panamá",
        "endpoints": {
            "/data": "Devuelve todos los datos de vacunación",
            "/data/year/{year}": "Devuelve los datos de un año específico",
            "/data/range?start={start_year}&end={end_year}": "Devuelve los datos dentro de un rango de años",
            "/data/stats": "Devuelve estadísticas básicas de los datos",
        }
    }

@app.get("/data")
def get_all_data():
    return data_records

@app.get("/data/year/{year}")
def get_data_by_year(year: int):
    filtered_data = [record for record in data_records if record["Year"] == year]
    if not filtered_data:
        raise HTTPException(status_code=404, detail="Datos no encontrados para el año solicitado.")
    return filtered_data

@app.get("/data/range")
def get_data_in_range(start: int, end: int):
    filtered_data = [record for record in data_records if start <= record["Year"] <= end]
    if not filtered_data:
        raise HTTPException(status_code=404, detail="No se encontraron datos para el rango solicitado.")
    return filtered_data

@app.get("/data/stats")
def get_stats():
    avg_vaccination = data["Vaccination Rate"].mean()
    min_vaccination = data["Vaccination Rate"].min()
    max_vaccination = data["Vaccination Rate"].max()
    return {
        "average_vaccination_rate": avg_vaccination,
        "min_vaccination_rate": min_vaccination,
        "max_vaccination_rate": max_vaccination
    }
