import cv2, torch, time, database

# Main
def main():
    
    print("# PENDETEKSI KERUSAKAN JALAN BERASPAL MENGGUNAKAN YOLOv5 ( REAL-TIME )")
    # Buka kamera, default berada pada index 0
    cap = cv2.VideoCapture('/home/aristocaesar/Documents/Kuliah/5.SEMESTER_5/PROJECT/potholed_r4CZDuZp.mp4')

    # Cek apakah kamera berhasil dibuka
    if not cap.isOpened():
        print("\nKamera tidak valid atau tidak ditemukan.")
        return
    
    # Cek koneksi ke database
    db_connection = database.create_connection()
    if not db_connection:
        return

    # Mulai mendeteksi dan Muat Model
    print('\nInisialisasi model pendekteksian objek ... \n')
    model = torch.hub.load('ultralytics/yolov5', 'custom',
                           path='model/best_PT_3_32.pt', force_reload=False)
    model.eval()

    # Perulangan untuk membaca dan menampilkan frame
    print('\nMulai mendeteksi object ... \n')
    while True:
        # Baca frame dari kamera
        ret, frame = cap.read()

        # Keluar dari loop jika tidak ada frame lagi
        if not ret:
            break

        # Penggunaan Model
        start_frame_time = time.time()
        results = model(frame)

        # Buat rentacle / shape berdasarkan hasil dari perhitungan gambar dengan model
        detected = []
        frame_with_boxes = frame.copy()
        for det in results.xyxy[0]:
            # Destructuring array, mengambil beberapa paramater yang dibutuhkan
            xmin, ymin, xmax, ymax, confidence, class_id = map(float, det)

            # Mengubah confidance menjadi percent & mengambil lebar serta keliling box
            confidence_percent = int(confidence * 100)
            wide = xmax - xmin

            # Gambar garis horizontal kuning
            line_y = 250  # Ganti dengan posisi y garis horizontal yang diinginkan
            cv2.line(frame_with_boxes, (0, line_y), (frame_with_boxes.shape[1], line_y), color=(
                30, 255, 255), thickness=2)

            # Jika confidence lebih dari 50 maka buatkan rentacle
            if confidence_percent >= 50:
                # Tambahkan object confidence kearray detect untuk menghithung
                # jumlah yang terderteksi
                detected.append(confidence_percent)

                # Konversi nilai kordinat float menjadi integer
                xmin, ymin, xmax, ymax = map(int, [xmin, ymin, xmax, ymax])

                # Kalkulasi titik tengah
                center_x = int((xmin + xmax) / 2)
                center_y = int((ymin + ymax) / 2)

                # Buat gambar di titik tengah
                rect_size = 4
                cv2.rectangle(frame_with_boxes, (center_x - rect_size, center_y - rect_size),
                              (center_x + rect_size, center_y + rect_size), color=(0, 255, 81), thickness=cv2.FILLED)

                # Buat gambar untuk background informasi box
                cv2.rectangle(frame_with_boxes, (xmin, ymin - 20),
                              (xmax, ymin), color=(0, 0, 255), thickness=cv2.FILLED)

                # Buat gambar untuk box berdasarkan titik kordinat
                cv2.rectangle(frame_with_boxes, (xmin, ymin),
                              (xmax, ymax), color=(0, 0, 255), thickness=2)

                # Buat tulisan class dan confidence yang terdeteksi
                cv2.putText(frame_with_boxes, f'{model.names[int(class_id)]} {confidence_percent}%', (
                    xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                # Periksa apakah titik tengah berada dalam jarak tertentu dari posisi garis horizontal
                if abs(center_y - line_y) < 5:
                    database.store_object_and_cordinate(connection=db_connection,
                        image=frame_with_boxes, wide=wide, accuracy=confidence_percent)

        # Menampilkan ringkasan hasil deteksi
        print(f'Objek yang terdeteksi: {detected} | ',
              f'Proses: {round(time.time() - start_frame_time)} Detik')

        # Tampilkan frame ke dalam windows
        cv2.imshow(
            'PENDETEKSI KERUSAKAN JALAN BERASPAL MENGGUNAKAN YOLOv5 ( REAL-TIME )', frame_with_boxes)

        # Hentikan perulangan jika menekan tombol 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Tutup koneksi ke database
    database.close_connection(db_connection)

    # Menghentikan pengembilan frame kamera
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
