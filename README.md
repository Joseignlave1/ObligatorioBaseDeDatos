# ObligatorioBaseDeDatos

## Instructivo para correr la aplicación

### Paso 1: Descargar el repositorio
Clona o descarga el repositorio en tu máquina local.

---

### Paso 2: Configurar e instalar dependencias

1. **Instalar los requerimientos del backend:**
   - Ubícate en la raíz del proyecto y ejecuta el comando:
     ```bash
     pip install -r requirements.txt
     ```

2. **Levantar la base de datos:**
   - Dirígete al directorio `DB`.
   - Levanta la base de datos usando Docker con el siguiente comando:
     ```bash
     docker-compose up
     ```
   - Abre la base de datos en un gestor como DataGrip y ejecuta las queries del archivo `init.sql` para crear la base de datos y sus tablas.

---

### Paso 3: Levantar el frontend

1. Ubícate en la carpeta /frontend del proyecto.
2. 
3. Ejecuta el comando:
   ```bash
   npm install
4. Para iniciar el proyecto ejecuta el siguiente comando:
   ```bash
   npm start
