# Sensor de Agua AWS IoT - Sistema de Monitoreo

Este proyecto implementa un sistema completo para monitorear un sensor de agua utilizando **AWS IoT Core**. El sistema consta de dos componentes principales:

1. **Simulador de Sensor**: Un script Python que envía datos a AWS IoT Core.  
2. **Dashboard de Visualización**: Una aplicación React que muestra los datos del sensor en tiempo real.

---

## 🛠️ Requisitos Previos

- Python 3.8 o superior  
- AWS CLI configurado  
- Node.js y npm  
- PowerShell (para Windows)  
- Certificados de AWS IoT Core:
  - `SensorAgua.cert.pem`
  - `SensorAgua.private.key`
  - `root-CA.crt`

---

## 📁 Estructura del Proyecto

```
sensor-agua-proyecto/
│
├── simulador/
│   ├── start.ps1                 # Script PowerShell para iniciar el simulador
│   ├── sensor_agua_aws.py        # Código del simulador
│   ├── SensorAgua.cert.pem       # Certificado de cliente
│   ├── SensorAgua.private.key    # Clave privada
│   └── root-CA.crt               # Certificado de CA raíz
│
└── dashboard/                    # Aplicación React
    ├── public/
    ├── src/
    ├── package.json
    └── ...
```

---

## ▶️ Ejecución del Simulador

### Paso 1: Navegar a la carpeta del simulador

```powershell
cd .\simulador\
```

### Paso 2: Ejecutar el script `start.ps1`

```powershell
.\start.ps1
```

### Si PowerShell muestra un error sobre la política de ejecución, intenta con:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\start.ps1
```

### O ejecuta el simulador directamente con:

```powershell
python sensor_agua_aws.py --endpoint a1ce9f01flw56-ats.iot.us-east-1.amazonaws.com `
--ca_file root-CA.crt `
--cert SensorAgua.cert.pem `
--key SensorAgua.private.key `
--client_id SensorAguaSimulador `
--topic sensores/agua/mediciones `
--interval 5
```

### 📝 Notas sobre el script `start.ps1`

El script automatiza los siguientes pasos:

- Verifica que Python esté instalado correctamente  
- Descarga el certificado raíz de AWS IoT si no existe  
- Clona el SDK de AWS IoT si es necesario  
- Instala las dependencias requeridas  
- Inicia el simulador con los parámetros correctos  

---

## 🖥️ Ejecución del Dashboard React

La aplicación de visualización está en la carpeta `dashboard`.

### Paso 1: Navegar a la carpeta del dashboard

```powershell
cd ..\dashboard\
```

### Paso 2: Instalar dependencias (si es la primera vez)

```powershell
npm install
```

### Paso 3: Iniciar la aplicación React

```powershell
npm start
```

La aplicación se abrirá automáticamente en tu navegador. Si no se abre, visita [http://localhost:3000](http://localhost:3000).

---

## ✅ Verificación del Sistema

- El simulador mostrará mensajes en consola cada 5 segundos con los datos enviados.  
- En el dashboard, los datos se actualizarán en tiempo real.  
- Opcionalmente, puedes verificar en la consola de **AWS IoT Core** que los mensajes están llegando correctamente.

---

## 💾 Visualización de Datos en DynamoDB

Los datos del sensor también se almacenan en una tabla DynamoDB llamada **`SensorAguaDatos`**. Puedes visualizarlos directamente desde la consola de AWS.

---

## 🛠️ Solución de Problemas

- **Error de certificados**: Verifica que los certificados estén en la carpeta correcta.  
- **Error de conexión**: Asegúrate de tener conexión a internet y permisos adecuados en AWS.  
- **Error en el dashboard**: Verifica que estás usando una versión compatible de Node.js (recomendado: v14+).  

---

## 📚 Recursos Adicionales

- [Documentación de AWS IoT Core](https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html)  
- [Guía de AWS IoT con Python](https://github.com/aws/aws-iot-device-sdk-python)  
- [Documentación de React](https://reactjs.org/)  

---

## 📬 Contacto

Para cualquier problema o pregunta, contacta al equipo de desarrollo.
