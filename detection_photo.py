import cv2, torch, uuid, imghdr, os, time

# Muat Model
print("# PENDETEKSI KERUSAKAN JALAN BERASPAL MENGGUNAKAN YOLOv5 ( PHOTO )")
image_path = input("Masukkan path gambar (jpg, jpeg, png, gif, bmp) : ")

# Memeriksa keberadaan path
if os.path.exists(image_path.strip()):

    # Pastikan MIMETYPE berupa gambar
    image_type = imghdr.what(image_path)
    if image_type in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:

        # Mulai mendeteksi dan Muat Model
        print('Mulai mendeteksi gambar ... \n')
        start_time = time.time()
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='model/best_THREE_CLASS_T3.pt', force_reload=False)
        model.eval()

        # Muat Foto
        img = cv2.imread(image_path)

        # Penggunaan Model
        results = model(img)

        # Buat rentacle / shape berdasarkan hasil dari perhitungan gambar dengan model
        img_with_boxes = img.copy()
        for det in results.xyxy[0]:
            # Konversi nilai kordinat float menjadi integer
            xmin, ymin, xmax, ymax, confidence, class_id = map(float, det)

            # Mengubah confidance menjadi percent & mengambil lebar serta keliling box
            confidence_percent = int(confidence * 100)
            width = xmax - xmin
            perimeter = 2 * (xmax - xmin) + 2 * (ymax - ymin)

            # Jika confidence lebih dari 50 maka buatkan rentacle
            if confidence_percent >= 50:
                xmin, ymin, xmax, ymax = map(int, [xmin, ymin, xmax, ymax])

                # Kalkulasi titik tengah
                center_x = int((xmin + xmax) / 2)
                center_y = int((ymin + ymax) / 2)

                # Buat gambar di titik tengah
                rect_size = 4
                cv2.rectangle(img_with_boxes, (center_x - rect_size, center_y - rect_size),(center_x + rect_size, center_y + rect_size), color=(0, 255, 81), thickness=cv2.FILLED)

                # Buat gambar untuk background informasi box
                cv2.rectangle(img_with_boxes, (xmin, ymin - 20), (xmax, ymin), color=(0, 0, 255), thickness=cv2.FILLED)
                
                # Buat gambar untuk box berdasarkan titik kordinat
                cv2.rectangle(img_with_boxes, (xmin, ymin), (xmax, ymax), color=(0, 0, 255), thickness=1)

                # Buat tulisan class dan confidence yang terdeteksi
                cv2.putText(img_with_boxes, f'{model.names[int(class_id)]} {confidence_percent}%', (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Simpan hasil gambar
        output_filename = f'photo_{uuid.uuid4()}.jpg'
        save_path = os.path.join('result', 'photos', output_filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        cv2.imwrite(save_path, img_with_boxes)

        # Informasi hasil deteksi
        print(f'\nOK - Hasil deteksi tersimpan di (result/photos/{output_filename})')
        print("Waktu -", round(time.time() - start_time) , "Detik")

    else:
        print("File yang dimasukkan bukan gambar.")

else:
    print("Path tidak valid atau tidak ditemukan.")