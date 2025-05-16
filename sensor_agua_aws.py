#!/usr/bin/env python3
# Simulador de sensor de agua para AWS IoT Core usando SDK v2

import json
import random
import time
from datetime import datetime
import sys
import threading
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import argparse

# Parsear argumentos de línea de comandos
parser = argparse.ArgumentParser()
parser.add_argument('--endpoint', required=True, help="El endpoint de AWS IoT")
parser.add_argument('--cert', required=True, help="Archivo de certificado del dispositivo")
parser.add_argument('--key', required=True, help="Archivo de clave privada")
parser.add_argument('--ca_file', required=True, help="Certificado de autoridad raíz")
parser.add_argument('--client_id', required=True, help="ID de cliente MQTT")
parser.add_argument('--topic', required=True, help="Tema MQTT para publicar")
parser.add_argument('--interval', type=float, default=5.0, help="Intervalo entre envíos en segundos")
args = parser.parse_args()

# Callback para confirmar la conexión
def on_connection_interrupted(connection, error, **kwargs):
    print(f"Conexión interrumpida. error: {error}")

def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print(f"Conexión reanudada. return_code: {return_code} session_present: {session_present}")

# Inicializar el evento para controlar la salida
received_all_event = threading.Event()

# Crear conexión MQTT
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=args.endpoint,
    cert_filepath=args.cert,
    pri_key_filepath=args.key,
    ca_filepath=args.ca_file,
    client_bootstrap=client_bootstrap,
    on_connection_interrupted=on_connection_interrupted,
    on_connection_resumed=on_connection_resumed,
    client_id=args.client_id,
    clean_session=False,
    keep_alive_secs=30)

print(f"Conectando a {args.endpoint} con ID de cliente {args.client_id}...")
connect_future = mqtt_connection.connect()

# Esperar a que se complete la conexión
connect_future.result()
print("¡Conectado!")

# Función para generar datos simulados del sensor de agua
def generar_datos_sensor():
    return {
        "timestamp": int(time.time()),
        "dispositivo": "SensorAgua001",
        "mediciones": {
            "nivel_agua": round(random.uniform(0, 100), 2),  # Nivel en porcentaje
            "ph": round(random.uniform(6.0, 8.5), 2),        # pH del agua
            "temperatura": round(random.uniform(15, 30), 2), # Temperatura en °C
            "conductividad": round(random.uniform(200, 800), 2), # µS/cm
            "turbidez": round(random.uniform(0, 10), 2)      # NTU
        },
        "alerta": False  # Se activará si algún valor está fuera de rango
    }

try:
    print(f"Publicando datos del sensor de agua en el tema '{args.topic}' cada {args.interval} segundos.")
    print("Presiona Ctrl+C para detener.")
    
    # Ciclo principal de simulación
    while True:
        datos = generar_datos_sensor()
        
        # Comprobar si algún valor está fuera de rango para activar alerta
        if (datos["mediciones"]["ph"] < 6.5 or 
            datos["mediciones"]["ph"] > 8.0 or 
            datos["mediciones"]["turbidez"] > 5.0):
            datos["alerta"] = True
        
        # Convertir datos a JSON
        mensaje_json = json.dumps(datos)
        
        # Publicar en AWS IoT Core
        mqtt_connection.publish(
            topic=args.topic,
            payload=mensaje_json,
            qos=mqtt.QoS.AT_LEAST_ONCE
        )
        
        # Mostrar datos enviados
        hora_actual = datetime.now().strftime("%H:%M:%S")
        print(f"[{hora_actual}] Datos enviados: Nivel: {datos['mediciones']['nivel_agua']}%, " +
              f"pH: {datos['mediciones']['ph']}, Temp: {datos['mediciones']['temperatura']}°C " +
              f"{'ALERTA!' if datos['alerta'] else ''}")
        
        # Esperar el intervalo especificado
        time.sleep(args.interval)

except KeyboardInterrupt:
    print("Simulación detenida por el usuario")
finally:
    print("Desconectando...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Desconectado")