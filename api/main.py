from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

try:
    model = joblib.load('modelo_riesgo.pkl')
    scaler = joblib.load('scaler.pkl')
    FEATURES = [
        'Hours Studied', 
        'Previous Scores', 
        'Sleep Hours', 
        'Sample Question Papers Practiced', 
        'Extracurricular_Binary'
    ]
    print(" Modelos cargados correctamente.")
except Exception as e:
    print(f" Error cargando modelos: {e}")
    model = None
    scaler = None

class Student(BaseModel):
    hours_studied: int
    previous_scores: int
    sleep_hours: int
    papers_practiced: int
    extracurricular_activities: str  

app = FastAPI(title="API Predicción Rendimiento Estudiantil")

fake_db = {}
id_counter = 0

def get_prediction(student: Student):
    if not model:
        raise HTTPException(status_code=500, detail="El modelo no está cargado.")

    if student.extracurricular_activities.lower() == 'yes':
        extra_binary = 1
    else:
        extra_binary = 0

    input_df = pd.DataFrame([[
        student.hours_studied,
        student.previous_scores,
        student.sleep_hours,
        student.papers_practiced,
        extra_binary
    ]], columns=FEATURES)

    input_scaled = scaler.transform(input_df)
    prediccion = model.predict(input_scaled)[0]
    return "ALTO RIESGO" if prediccion == 1 else "BAJO RIESGO"


@app.get("/")
def home():
    return {"mensaje": "API funcionando."}

@app.post("/predict")
def predict_student(student: Student):
    global id_counter
    
    resultado_texto = get_prediction(student)

    id_counter += 1
    respuesta = {
        "id": id_counter,
        "input": student,
        "prediction": resultado_texto
    }
    fake_db[id_counter] = respuesta
    return respuesta

@app.get("/predictions")
def get_history():
    return list(fake_db.values())

@app.get("/predictions/{id}")
def get_prediction_by_id(id: int):
    if id not in fake_db:
        raise HTTPException(status_code=404, detail="Predicción no encontrada")
    return fake_db[id]

@app.put("/predictions/{id}")
def update_prediction(id: int, student: Student):
    if id not in fake_db:
        raise HTTPException(status_code=404, detail="Predicción no encontrada")
    
    nuevo_resultado = get_prediction(student)
    
    fake_db[id]["input"] = student
    fake_db[id]["prediction"] = nuevo_resultado
    
    return {"mensaje": "Actualizado", "data": fake_db[id]}

@app.delete("/predictions/{id}")
def delete_prediction(id: int):
    if id not in fake_db:
        raise HTTPException(status_code=404, detail="Predicción no encontrada")
    
    del fake_db[id]
    return {"mensaje": f"Predicción {id} eliminada correctamente"}