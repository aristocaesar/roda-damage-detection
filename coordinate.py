import serial

# Mengambil titik kordinat menggunakan serial node mcu + gps
def get_latitude_longitude_address():
    # Init NodeMCU Serial
    # ser = serial.Serial('/dev/ttyUSB0', baudrate = 9600, timeout=1)

    # # Mengirim perintah ke NodeMCU
    # ser.write('GET_COORDINATE'.encode('utf-8'))

    # # Menerima hasil perintah dari NodeMCU
    # coordinate = ser.readline().decode('utf-8')

    # # Melakukan format untuk return
    # result = coordinate.split(',')
    # result = tuple(item.strip() for item in result)
    # latitude = result[0]
    # longitude = result[1]

    # return latitude, longitude
    latitude = -8.159085
    longitude = 113.721818
    return latitude, longitude