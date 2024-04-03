import socket
import json
import struct
import signal
import sys
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

def messeng_number():
    try:
        with open("message_number.txt", 'r') as f:
            return int(f.read())
    except ValueError:
        # Если файл пустой, создаем значение 1 
        with open("message_number.txt", 'w') as f:
            f.write("1")
            return 1
    except FileNotFoundError:
        # Если файл не найден, создаем его и записываем начальное значение (1)
        with open("message_number.txt", 'w') as f:
            f.write("1")
            return 1
        


def write_message_number(message_number):
    with open("message_number.txt", "w") as f:
        f.write(str(message_number))



server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((UDP_IP, UDP_PORT))
number_messege = messeng_number()
print("UDP server started")


try:
    while True:
        data, addr = server_socket.recvfrom(1024)
        header = data[:10]

        # Извлекаем номер сообщения из заголовка
        marker, received_message_number, data_size = struct.unpack('!2sII', header)

        # Выводим информацию о номере сообщения
        print("Received message number:", number_messege)

        # Оставшиеся данные после заголовка
        message_data = data[10:]

        # Попытка декодирования JSON-данных
        try:
            message_data = message_data.decode('utf-8')
            json_data = json.loads(message_data)

            print(f"Received message: {json_data}")
        except json.JSONDecodeError as e:
            print("Received invalid JSON data", e)
        number_messege+=received_message_number
        if received_message_number >2**32 -1:
            messeng_number = 1
        write_message_number(number_messege)
except KeyboardInterrupt:

    print("Server stopped by user") 
finally:
    with open("message_number.txt", "w") as f:
        pass
    
    server_socket.close()
