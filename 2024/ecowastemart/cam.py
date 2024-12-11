import cv2

# Membuka kamera
cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Tidak bisa membuka kamera")
    exit()

while True:
    # Membaca frame dari kamera
    ret, frame = cap.read()

    if not ret:
        print("Gagal mendapatkan frame")
        break

    # Menampilkan frame
    cv2.imshow('Kamera', frame)
    cv2.

    # Menekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Membersihkan dan menutup jendela
cap.release()
cv2.destroyAllWindows()
