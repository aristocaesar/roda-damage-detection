import os, cv2, time, coordinate, psycopg2
from datetime import datetime
from dotenv import load_dotenv

# Inisialisasi environtment
load_dotenv()
realtime_result_path = os.getenv('REALTIME_RESULT_PATH')
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_name = os.getenv('DB_NAME')
db_port = os.getenv('DB_PORT')

# Koneksi database postgresql
def create_connection():
    db_params = {
        'dbname': db_name,
        'user': db_user,
        'password': db_pass,
        'host': db_host,
        'port': db_port
    }

    try:
        connection = psycopg2.connect(**db_params)
        print("\nBerhasil koneksi ke database!")
        return connection

    except (Exception, psycopg2.Error) as error:
        print(f"\nTerjadi keasalahan saat koneksi database!\n{error}")
        return None
    
# Mengeksekusi Query
def execute_query(connection, query, id):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            print(f"Object berhasil disimpan! - {realtime_result_path}detection_{id}")
    except Exception as e:
        print(f"Error: {e}")

# Menutup Koneksi
def close_connection(connection):
    if connection:
        connection.close()
        print("\nMenutup koneksi ke database")
    
# Menyimpan gambar, titik kordinat pada database
def store_object_and_cordinate(**args):
    # Inisialisasi id dan folder
    id = str(int(time.time() * 1000))
    file_dir_path = os.path.join(realtime_result_path, f'detect_{id}')
    os.makedirs(file_dir_path)

    # Ambil titik kordinat
    latitude, longitude = coordinate.get_latitude_longitude_address()

    # Simpan gambar deteksi
    output_filename = f'photo_{id}.jpg'
    file_saved = os.path.join(file_dir_path, output_filename);
    cv2.imwrite(file_saved, args['image'])

    # Simpan ringkasan deteksi
    connection = args['connection']
    confidance = round(args["accuracy"])
    wide = round(args["wide"])

    with open(os.path.join(file_dir_path, f'summary_{id}.txt'), 'w') as file:
        file.write(
            f'Summary - ({id})\n\nLangitude : {latitude} \nLongitude : {longitude}\nAccuracy : {confidance}\nWide : {wide}\nImage : {file_saved}\n\nCreated : {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
        
    # Simpan ke dalam database
    execute_query(connection, f"INSERT INTO detections (id, latitude, longitude, confidance, wide, image) VALUES ('{id}', '{latitude}', '{longitude}', '{confidance}', '{wide}', '{output_filename}')", id)