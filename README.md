# Sistema de Triage y Flujo de Sala de Urgencias

Sistema hospitalario que utiliza estructuras de datos clasicas (Arrays, Queues, Stacks, Lists, Singly Linked Lists) con frontend en Streamlit.

## Estructura del Proyecto

```
Citasmedicas/
├── backend/                  # Logica y estructuras de datos (Python)
│   ├── __init__.py
│   ├── camas_uci.py          # Arrays - Camas UCI
│   ├── cola_espera.py        # Queue - Sala de espera
│   ├── pila_deshacer.py      # Stack - Sistema deshacer
│   ├── directorio_medico.py  # List - Directorio medico
│   ├── historial_intervenciones.py  # Singly Linked List - Historial
│   └── hospital_manager.py   # Gestor central
├── frontend/                 # Interfaz grafica (Streamlit)
│   └── app.py
├── requirements.txt
└── README.md
```

## Como ejecutar

1. Crear entorno virtual:
```bash
python -m venv .venv
```

2. Activar entorno virtual:
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecutar la aplicacion:
```bash
streamlit run frontend/app.py
```

5. Abrir en el navegador: http://localhost:8501
