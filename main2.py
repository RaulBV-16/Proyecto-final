from netmiko import ConnectHandler

SWITCH_MAIN = {
    "device_type": "cisco_ios",
    "host": "192.168.1.1",
    "username": "cisco",
    "password": "cisco",
}

mac_address = input("Ingrese la dirección MAC que desea buscar: ").strip()


def show_mac_address_table(connection, mac):
    """Busca la dirección MAC en la tabla de direcciones MAC."""
    try:
        salida = connection.send_command("show mac address-table")
        hostname = connection.send_command("show running-config | include hostname").strip()

        buscar = salida.find(mac)
        if buscar != -1:
            puerto = salida.split(mac)[1].split()[1]
            print(f"\nLa MAC: {mac} se encuentra en el puerto {puerto} del dispositivo {hostname.split()[-1]}")
            return puerto
        else:
            print(f"\nLa MAC {mac} no fue encontrada en este switch.")
            return -1
    except Exception as e:
        print(f"Error al buscar la tabla de direcciones MAC: {e}")
        return -1


def show_interface(connection, port):
    """Obtiene información sobre la interfaz donde se detectó la MAC."""
    try:
        comando = f"show interface {port}"
        salida = connection.send_command(comando)
        interface = salida.split()[0]
        return interface
    except Exception as e:
        print(f"Error al obtener información de la interfaz: {e}")
        return None


def cdp_neighbor_details(connection, interface):
    """Busca información sobre dispositivos vecinos conectados a la interfaz."""
    try:
        salida = connection.send_command("show cdp neighbors detail")
        texto = f"Interface: {interface}"
        dispositivos = salida.split("-------------------------")
        for dispositivo in dispositivos:
            if texto in dispositivo:
                ip_address = dispositivo.split("IP address: ")[1].split()[0]
                print(f"Vecino encontrado en {texto}. IP del vecino: {ip_address}")
                return ip_address
        print(f"No se encontraron vecinos conectados a la interfaz {interface}.")
        return -1
    except Exception as e:
        print(f"Error al obtener detalles de vecinos CDP: {e}")
        return -1


def nueva_conexion(ip):
    """Configura una nueva conexión con un switch vecino."""
    print(f"\nConectando al switch con IP: {ip}")
    return {
        "device_type": "cisco_ios",
        "host": ip,
        "username": "cisco",
        "password": "cisco",
    }


def main():
    """Función principal para buscar una dirección MAC a través de switches."""
    global SWITCH_MAIN
    while True:
        try:
            connection = ConnectHandler(**SWITCH_MAIN)
            print(f"Conectado al switch: {SWITCH_MAIN['host']}")

            port = show_mac_address_table(connection, mac_address)
            if port == -1:
                break

            interface = show_interface(connection, port)
            if not interface:
                break

            ip = cdp_neighbor_details(connection, interface)
            if ip == -1:
                break

            SWITCH_MAIN = nueva_conexion(ip)
            connection.disconnect()

        except Exception as e:
            print(f"Error al procesar el switch {SWITCH_MAIN['host']}: {e}")
            break
        finally:
            if 'connection' in locals():
                connection.disconnect()
                print(f"Conexión cerrada para el switch: {SWITCH_MAIN['host']}")


if __name__ == "__main__":
    main()