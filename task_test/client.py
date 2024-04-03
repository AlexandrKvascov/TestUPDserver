import socket
import json
import struct
import random
import time
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# Функция для генерации словаря с данными о местоположении и параметрах движения объекта
def generate_dictionary():
    latitude = round(random.uniform(-100, 100),4)
    longitude = round(random.uniform(-100, 100),4)
    speed = round(random.randint(1, 280),4)


    return {
        "latitude": latitude,
        "longitude": longitude,
        "speed": speed,
   
    }

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for i in range(1,4):
    # time.sleep(2)
    # Пример данных о местоположении и параметрах движения объекта в формате JSON
    location_data = generate_dictionary()
    # print("Sending data:", location_data)

    # Преобразуем данные в JSON-строку
    json_data = json.dumps(location_data)

    # Определяем размер блока данных сообщения (8 + N, где N - длина JSON-строки)
    data_size = min(len(json_data), 1000) + 8

# Обрезаем JSON-строку, если она превышает 1000 байт
    json_data = json_data[:1000]

    # Формируем заголовок сообщения
    header = struct.pack('!2sII', b'EE', 1, data_size)

    # Формируем информационное сообщение
    message = header + json_data.encode('utf-8')

    # Отправляем сообщение на сервер

    client_socket.sendto(message, (UDP_IP, UDP_PORT))
# client_socket.sendto(mes_test, (UDP_IP, UDP_PORT))

client_socket.close()
