import scapy.all as scapy 
import socket
import psutil
import sys
import signal

PYCHON_ETHERTYPE=0x1234
BROADCAST_MAC="ff:ff:ff:ff:ff:ff"

def get_nic(interface):
    # genera un diccionario con la información de la interfaz de red
    data = {
        'name': interface
    }
    for snicaddr in psutil.net_if_addrs()[interface]:
        if snicaddr.family == socket.AF_INET:
            data['ipv4'] = snicaddr.address
            data['netmask'] = snicaddr.netmask
        elif snicaddr.family == psutil.AF_LINK:
            data['mac'] = snicaddr.address.replace('-', ':')
    if not 'mac' in data:
        data['mac'] = "No disponible"
    return data

def get_all_nics():
    # devuelve una lista con todas las interfaces de red disponibles
    return [ get_nic(interface) for interface in psutil.net_if_stats().keys() ]

def choose_nic():
    # obtiene todas las interfaces de red disponibles
    nics = get_all_nics()
    # imprime un menú con las interfaces de red disponibles
    print("Interfaces de red disponibles:")
    for i, nic in enumerate(nics):
        print(f"{i+1}. {nic['name']} ({nic['mac']})")
    # entra en bucle infinito hasta que se selecciona un valor válido
    while True:
        try:
            # solicita al usuario que elija una interfaz
            index = int(input(f"Elige una interfaz (1-{len(nics)}): ")) - 1
            # devuelve el nombre de la interfaz seleccionada
            return nics[index]['name']
        except (ValueError, IndexError):
            print("Opción no válida")

def process_frame(frame):
    # comprueba si el frame es de tipo PYCHON_ETHERTYPE
    if frame.type == PYCHON_ETHERTYPE:
        # obtiene la dirección MAC de origen del frame
        src = frame.src
        # previene errores si el campo Raw no está presente
        load = frame[scapy.Raw].load.decode("utf-8") if scapy.Raw in frame else ""
        # imprime el mensaje y su remitente
        print(f"[{src}]: {load}")

def handle_ctrl_c(sig, frame):
    # se ejecuta cuando se pulsa CTRL+C
    print('Terminando programa...')
    sys.exit(0)

def receive(interface):
    # captura paquetes en la interfaz de red y los procesa
    print(f"Recibiendo paquetes en {interface} (CTRL+C para detener)")
    scapy.sniff(iface=interface, prn=process_frame)

def send(message):
    # difunde un mensaje en la red
    frame = scapy.Ether(dst=BROADCAST_MAC, type=PYCHON_ETHERTYPE) / scapy.Raw(load=message.encode("utf-8"))
    scapy.sendp(frame, verbose=False)

if __name__ == "__main__":
    option = sys.argv[1]
    match option:
        case "--receive":
            # captura la señal de CTRL+C
            signal.signal(signal.SIGINT, handle_ctrl_c)
            # elige la interfaz de red si no se proporciona como argumento
            interface = choose_nic() if len(sys.argv) < 3 else sys.argv[2]
            # recibe mensajes de la interfaz de red seleccionada
            receive(interface)
        case "--send":
            # envía mensajes hasta que se pulsa ENTER
            while True:
                message = input("Introduce el mensaje a enviar (ENTER para terminar): ")
                if message:
                    send(message)
                else:
                    break
        case _:
            print("Uso: python chat.py [--receive [nic] | --send]")
