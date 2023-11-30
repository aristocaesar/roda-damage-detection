import cv2, torch, uuid, mimetypes, os, time

# Muat Model
print("# PENDETEKSI KERUSAKAN JALAN BERASPAL MENGGUNAKAN YOLOv5 ( VIDEO )")
video_path = input("Masukkan path vidio (mp4, mov) : ")

# Memeriksa keberadaan path
if os.path.exists(video_path.strip()):

    # Pastikan MIMETYPE berupa vidio
    image_type, _ = mimetypes.guess_type(video_path)
    
    print(image_type)
    
    if image_type in ['video/mp4', 'video/quicktime']:

        # Mulai mendeteksi dan Muat Model
        print('Mulai mendeteksi vidio ... \n')
        start_time = time.time()
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='model/best.pt', force_reload=False)
        model.eval()

        # Muat Vidio
        video_capture = cv2.VideoCapture(video_path)

        # Mendapatkan informasi tentang vidio (lebar, tinggi, frame per detik)
        frame_width = int(video_capture.get(3))
        frame_height = int(video_capture.get(4))
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        # Proses vidio
        output_filename = f'video_{uuid.uuid4()}.mp4'
        save_path = os.path.join('result', 'videos', output_filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        output_video = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

        while True:
            # Membaca satu frame dari vidio
            ret, frame = video_capture.read()

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

                # Warna berdasarkan class
                # 0, 0, 255 ( Merah ) -> berlubang
                # 235, 229, 52 ( Biru muda ) -> retak_buaya
                # 3, 154, 255 ( orange ) -> retak_panjang
                color = [(0, 0, 255) , (235, 229, 52), (3, 154, 255)]

                # Mengubah confidance menjadi percent & mengambil lebar serta keliling box
                confidence_percent = int(confidence * 100)
                wide = xmax - xmin

                # Jika confidence lebih dari 50 maka buatkan rentacle
                if confidence_percent >= 50:
                    # Tambahkan object confidence kearray detect untuk menghithung
                    # jumlah yang terderteksi
                    detected.append(f'{model.names[int(class_id)]} - {confidence_percent}%')

                    # Konversi nilai kordinat float menjadi integer
                    xmin, ymin, xmax, ymax = map(int, [xmin, ymin, xmax, ymax])

                    # Kalkulasi titik tengah
                    center_x = int((xmin + xmax) / 2)
                    center_y = int((ymin + ymax) / 2)

                    # Buat gambar di titik tengah
                    rect_size = 4
                    cv2.rectangle(frame_with_boxes, (center_x - rect_size, center_y - rect_size),(center_x + rect_size, center_y + rect_size), color=(0, 255, 81), thickness=cv2.FILLED)

                    # Buat gambar untuk background informasi box
                    cv2.rectangle(frame_with_boxes, (xmin, ymin - 20), (xmax, ymin), color=(color[int(class_id)]), thickness=cv2.FILLED)

                    # Buat gambar box berdasarkan titik kordinat
                    cv2.rectangle(frame_with_boxes, (xmin, ymin), (xmax, ymax), color=(color[int(class_id)]), thickness=2)
                    
                    # Buat tulisan class dan confidence yang terdeteksi
                    cv2.putText(frame_with_boxes, f'{model.names[int(class_id)]} {confidence_percent}%', (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Menulis frame yang telah diberi bounding box kemudian simpan
            output_video.write(frame_with_boxes)
            # Menampilkan nomor frame
            current_frame = int(video_capture.get(cv2.CAP_PROP_POS_FRAMES))
            print(f'Frame: {current_frame}/{total_frames} | ',f'Objek yang terdeteksi: {detected} | ',f'Proses: {round(time.time() - start_frame_time)} Detik')
        
        # Tutup video capture dan release video ( simpan vidio )
        video_capture.release()
        output_video.release()

        # Informasi hasil deteksi
        print(f'\nOK - Hasil deteksi tersimpan di (result/videos/{output_filename})')
        print("Waktu -", round(time.time() - start_time) , "Detik")

    else:
        print("File yang dimasukkan bukan gambar.")   

else:
    print("Path tidak valid atau tidak ditemukan.")