# Script para Buscar una Dirección MAC en una Red de Switches Cisco

Este script utiliza Python y la biblioteca `netmiko` para buscar una dirección MAC en la tabla de direcciones MAC de un switch Cisco. Si la dirección MAC no se encuentra en el switch actual, el script utiliza información de vecinos (CDP) para conectarse al siguiente switch y continuar la búsqueda.

## Requisitos Previos

1. **Entorno de Python Configurado**:
   - Asegúrate de tener Python 3.6 o superior instalado.
   - Instala la biblioteca `netmiko` con:
     ```bash
     pip install netmiko
     ```

2. **Acceso a la Red**:
   - Los switches deben ser accesibles desde el dispositivo donde ejecutas el script.
   - CDP (Cisco Discovery Protocol) debe estar habilitado en los switches.

3. **Credenciales**:
   - Necesitas un nombre de usuario y contraseña válidos para acceder a los switches Cisco.

4. **Configuración Inicial**:
   - Actualiza la dirección IP, el nombre de usuario y la contraseña en la variable `SWITCH_MAIN` del script.

## Instrucciones de Uso

1. **Prepara el Script**:
   - Descarga o copia el código en un archivo Python, por ejemplo, `buscar_mac.py`.

2. **Configura las Credenciales**:
   - Modifica la variable `SWITCH_MAIN` en el script con los datos del primer switch al que deseas conectarte:
     ```python
     SWITCH_MAIN = {
         "device_type": "cisco_ios",
         "host": "IP_DEL_SWITCH",
         "username": "USUARIO",
         "password": "CONTRASEÑA",
     }
     ```

3. **Ejecuta el Script**:
   - Desde la terminal, ejecuta el archivo con:
     ```bash
     python buscar_mac.py
     ```

4. **Ingresa la Dirección MAC**:
   - El script solicitará que introduzcas la dirección MAC que deseas buscar. Ingrésala en el formato estándar, por ejemplo:
     ```
     00:1A:2B:3C:4D:5E
     ```

5. **Sigue el Proceso**:
   - El script intentará localizar la dirección MAC en el switch actual.
   - Si la MAC no se encuentra, utilizará CDP para buscar dispositivos vecinos y continuará buscando en ellos hasta localizarla o agotar las opciones.

6. **Resultados**:
   - Si la MAC es encontrada, el script mostrará el puerto y el nombre del switch donde está conectada.
   - Si no se encuentra, se notificará que no fue localizada.

## Notas Importantes

- **Privilegios Necesarios**:
  - Asegúrate de que la cuenta utilizada tenga permisos para ejecutar los comandos `show mac address-table`, `show interface`, y `show cdp neighbors detail`.

- **Formato de la Dirección MAC**:
  - Ingresa la dirección MAC en un formato compatible con los switches Cisco. Si es necesario, consulta la documentación del equipo.

- **Errores Comunes**:
  - Si no puedes conectarte a un switch, verifica:
    - La dirección IP.
    - Las credenciales.
    - Que el switch esté accesible por la red.
    - Que los comandos requeridos estén habilitados.
