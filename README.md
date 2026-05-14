# 🏊 Cobaj Sports Rendiment

<img width="1181" height="912" alt="image" src="https://github.com/user-attachments/assets/0240775d-2399-4d2b-be8a-cb16c34ac7e0" />

Sistema de escritorio para la gestión integral del rendimiento deportivo de nadadores. Permite al entrenador registrar y monitorear sesiones de entrenamiento, métricas de rendimiento, lesiones y terapias de recuperación de cada deportista bajo su supervisión.

---

## 🚀 Instalación

### Requisitos previos

- Python 3.12+
- PostgreSQL 14+
- pip

### 1. Clonar el repositorio

```bash
git clone https://github.com/Lancercrack25/Cobaj-swimmers-rendiment.git
```

### 2. Instalar dependencias

```bash
pip install customtkinter psycopg2-binary pillow pyttsx3 speechrecognition matplotlib pandas dotoenv
```

### 3. Configurar la base de datos

Crea un archivo `.env` en la carpeta `Backend` con las siguientes variables:

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=tu_password
DB_NAME=cobaj_sports
```

### 4. Ejecutar el sistema

```bash
python main.py

```
Las tablas y la base de datos se crean automáticamente al iniciar por primera vez.
---

## 🗂️ Estructura del Proyecto

```
cobaj-sports-rendiment/
├── main.py                          # Punto de entrada principal
├── Backgrounds/                     # Imágenes de fondo de las interfaces
├── Backend/
│   ├── coneccion_database.py        # Conexion a PostgreSQL
│   ├── database.py                  # Inicializacion del sistema
│   ├── tablas_creacion.py           # Creacion automatica de tablas
│   └── funcionamiento_logica_modulos/
│       ├── entrenadores.py          # Logica de entrenadores
│       ├── nadadores.py             # Logica de nadadores
│       ├── sesiones.py              # Logica de sesiones
│       ├── metricas.py              # Logica de metricas y rendimiento
│       ├── lesiones.py              # Logica de lesiones
│       └── terapias_rehabilitacion.py
└── archivos/
    ├── main.py                      # Interfaz principal de login
    ├── Animaciones/                 # Splash screen 
    ├── Asistente_voz/               # Modulo de voz con pyttsx3
    ├── Entrenador/                  # Interfaces del entrenador
    ├── Nadadores/                   # Interfaces del nadador
    ├── Lesion/                      # Interfaces de lesiones
    ├── Terapias_reabilitacion/      # Interfaces de terapias
    ├── metricas_rendimiento/        # Interfaces de estadisticas
    └── rendimiento_seciones/        # Interfaces de registro de sesiones
```

---

## 🗄️ Base de Datos

| Tabla | Descripción |
|-------|-------------|
| `entrenadores` | Entrenadores registrados en el sistema |
| `nadadores` | Deportistas asignados a un entrenador |
| `sesiones_entrenamiento` | Sesiones creadas por el entrenador |
| `rendimiento_nadador` | Métricas de distancia, tiempo y ritmo por sesión |
| `lesiones` | Lesiones activas e historial de cada nadador |
| `rehabilitaciones` | Terapias asignadas a lesiones activas |

---

## 👤 Modo Entrenador

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/0000b4f7-d3d2-4914-9159-fd91e008763e" />

### Acceso
Login con nombre de usuario y contraseña. El entrenador puede registrarse desde la pantalla principal.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/b0090ca2-5698-4914-a47b-36aad06cad4a" />

### Funcionalidades
- **Registrar nadador** — Alta de nuevos deportistas con datos físicos
- **Mis nadadores** — Lista de todos los nadadores bajo su supervisión
- **Ver estadísticas** — Estadísticas individuales y globales con gráficas comparativas
- **Eliminar nadador** — Baja de deportistas del sistema
- **Registro de sesión** — Registra distancia y tiempo de un nadador verificando que no tenga lesión activa
- **Registrar nadador lesionado** — Flujo de registro de lesión con redirección automática a terapias si la gravedad es media o grave
- **Salir** — Cierra sesión

---

## 🏊 Modo Nadador

### Acceso
Login con código de acceso y contraseña asignados por el entrenador.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/d4717e9d-07c2-4352-b4d8-25d923a8e84e" />

### Funcionalidades

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c15823b8-9733-4b90-8cb3-3f85d134dfc3" />

- **Mi perfil** — Visualización de datos personales
- **Mis estadísticas** — Historial de rendimiento personal
- **lesiones y Terapias** — Aqui el nadador podra consualr su historial de lesiones, el de terapias ademas de que podra registrar una lesion

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3cd83425-8d72-44df-b530-57e7af8e39a9" />

---

## 📊 Estadísticas y Métricas

### Individuales

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/b2df29bd-c85d-4715-b462-5ee8e2412235" />

Historial cronológico con distancia, tiempo, ritmo y fecha de cada sesión.

### Globales
Resumen del equipo completo:

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/551b3518-00e7-45f5-94e8-eedb5e6050cf" />

- Total de sesiones y nadadores activos
- Promedios de distancia, tiempo y ritmo
- Gráfica comparativa de líneas por nadador

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/53909ee6-96f4-4a8d-9f16-34120b29c391" />

---

## 🩹 Lesiones y Terapias

### Flujo automático
1. Se registra la lesión con tipo, gravedad y fecha
2. Si la gravedad es **media** o **grave** → redirige automáticamente al registro de terapia
3. Si es **leve** → termina el flujo

### Regla crítica
Un nadador con lesión activa **no puede registrar rendimiento**. La función `puede_entrenar()` bloquea el registro antes de cualquier operación en la base de datos.

### Historial de terapias
Muestra estado (en curso / finalizada) con opción de marcar como finalizada desde la interfaz.

---

## 🎤 Asistente de Voz

Acompaña las acciones principales del sistema con mensajes de voz usando `pyttsx3` con motor SAPI5. Detecta automáticamente voces en español si están disponibles en el sistema.

---

## 🏗️ Arquitectura MVC

| Capa | Carpeta | Responsabilidad |
|------|---------|-----------------|
| Vista | `archivos/` | Interfaces gráficas con CustomTkinter |
| Controlador | `Backend/funcionamiento_logica_modulos/` | Lógica de negocio y validaciones |
| Modelo | `Backend/coneccion_database.py` | Acceso a PostgreSQL con psycopg2 |

---

## 🛠️ Tecnologías

| Área | Tecnología |
|------|-----------|
| Interfaz gráfica | CustomTkinter |
| Base de datos | PostgreSQL |
| Conector BD | psycopg2 |
| Gráficas | Matplotlib |
| Análisis de datos | Pandas |
| Asistente de voz | pyttsx3 + SpeechRecognition |
| Imágenes | Pillow |

---

## ⚠️ Notas importantes

- El archivo `.env` nunca debe subirse al repositorio
- Las tablas se crean automáticamente al iniciar con `CREATE TABLE IF NOT EXISTS`
- Los códigos de acceso de nadadores se manejan como texto para preservar ceros iniciales
