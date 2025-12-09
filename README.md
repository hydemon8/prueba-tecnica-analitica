# Prueba técnica

Este repositorio contiene la solución a los dos casos prácticos planteados, abarcando desde el análisis exploratorio de datos (EDA) hasta la implementación de una API productiva con Docker.

---

##  Estructura del Proyecto

El proyecto se divide en análisis y despliegue:

```text
├── casos/                #  SOLUCIÓN A LOS 2 CASOS (Notebooks)
│   ├── caso1.ipynb       # Análisis Caso 1 (Ej: Mundial/Partidos)
│   └── caso2.ipynb       # Análisis Caso 2 (Ej: Rendimiento Estudiantes)
│
├── api/                  #  IMPLEMENTACIÓN TÉCNICA (Python Script + Docker)
│   ├── main.py           # API FastAPI con CRUD completo
│   ├── Dockerfile        # Contenedor para despliegue
│   ├── requirements.txt  # Librerías necesarias
│   └── *.pkl             # Modelos entrenados
│
├── data/                 # Archivos de apoyo (Datasets originales)
└── README.md             # Esta documentación
```

##  Descripción de los Casos

### Caso 1: Análisis de resultados mundiales de fútbol femenino

Ubicación: `casos/caso1.ipynb`

  * Transformación de datos y limpieza.
  * Análisis exploratorio y visualización de tendencias.

### Caso 2: Predicción de Rendimiento Estudiantil en el área de matemáticas

Ubicación: `casos/caso2.ipynb` y carpeta `api/`

  * Entrenamiento de modelos (Clustering + Clasificación).
  * **Despliegue:** Se creó una API RESTful para poner en producción este modelo.


##  Ejecución Rápida con Docker

Asegura la reproducibilidad del entorno sin conflictos de dependencias.

1. **Ir a la carpeta de la API**

```bash
cd api
```

2. **Construir la imagen**

```bash
docker build -t prediccion-estudiantes .
```

3. **Ejecutar el contenedor**

```bash
docker run -p 8000:8000 prediccion-estudiantes
```

4. **Acceder a la documentación interactiva**

[http://localhost:8000/docs](http://localhost:8000/docs)


##  Uso de la API 
La API cuenta con Swagger UI.

Muestras utilizadas para el funcionamiento de la API:

```bash
{
  "hours_studied": 2,
  "previous_scores": 50,
  "sleep_hours": 5,
  "papers_practiced": 0,
  "extracurricular_activities": "No"
}
```

```bash
{
  "hours_studied": 8,
  "previous_scores": 85,
  "sleep_hours": 7,
  "papers_practiced": 5,
  "extracurricular_activities": "Yes"
}
```


###  Predicción 

* **POST** `/predict`
  Recibe datos del estudiante y devuelve si tiene **"ALTO RIESGO"** o **"BAJO RIESGO"** de tener un mal desempeño en matemáticas.

###  Gestión de Historial (CRUD)

* **GET** `/predictions` — Lista histórico de predicciones.
* **GET** `/predictions/{id}` — Consulta un registro específico.
* **PUT** `/predictions/{id}` — Actualiza datos y recalcula predicción.
* **DELETE** `/predictions/{id}` — Elimina un registro.





