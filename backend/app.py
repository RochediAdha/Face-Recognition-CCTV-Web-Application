from flask import Flask, Response, jsonify, request
from flask_cors import CORS  # Tambahkan import Flask-CORS
import cv2
import face_recognition
import os
import json
from dotenv import load_dotenv


# Muat variabel dari file .env
load_dotenv()

# Ambil konfigurasi dari .env
HOST = os.getenv("HOST", "127.0.0.1")  # Default ke 127.0.0.1 jika tidak ditemukan
PORT = int(os.getenv("PORT", 5000))  # Default ke 5000 jika tidak ditemukan

app = Flask(__name__)
CORS(app)  # Aktifkan CORS untuk semua rute

# Path file JSON untuk daftar CCTV
# CCTV_FILE = "cctv_list.json"
CCTV_FILE = os.path.join(os.path.dirname(__file__), "cctv_list.json")

# Path folder yang berisi gambar wajah yang dikenal
KNOWN_FACES_DIR = KNOWN_FACES_DIR = os.path.join(
    os.path.dirname(__file__), "known_faces"
)

# Variabel untuk menyimpan enkoding wajah dan nama
known_face_encodings = []
known_face_names = []


# Fungsi untuk memuat daftar CCTV dari file JSON
def load_cctv_list():
    try:
        with open(CCTV_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {CCTV_FILE} tidak ditemukan!")
        return []
    except json.JSONDecodeError:
        print(f"File {CCTV_FILE} tidak valid!")
        return []


# Fungsi untuk memuat wajah yang dikenal dari folder
def load_known_faces():
    print("Memuat wajah yang dikenal dari folder...")
    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.endswith(".jpg") or filename.endswith(".png"):  # Filter file gambar
            path = os.path.join(KNOWN_FACES_DIR, filename)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(os.path.splitext(filename)[0])
                print(f" - {filename} dimuat.")
            else:
                print(f" - {filename} tidak memiliki wajah yang terdeteksi.")


# Muat semua wajah dari folder
load_known_faces()


# Endpoint untuk mendapatkan daftar CCTV
@app.route("/api/cctv", methods=["GET"])
def get_cctv_list():
    cctv_list = load_cctv_list()
    return jsonify(cctv_list)


# Fungsi untuk memproses video stream dari URL CCTV
def generate_frames(cctv_url):
    video_capture = cv2.VideoCapture(cctv_url)
    if not video_capture.isOpened():
        raise RuntimeError(f"Gagal membuka stream CCTV: {cctv_url}")

    while True:
        success, frame = video_capture.read()
        if not success:
            break

        # Konversi frame ke RGB
        rgb_frame = frame[:, :, ::-1]

        # Temukan semua wajah di frame saat ini
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding, tolerance=0.6
            )
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            face_names.append(name)

        # Gambar kotak dan nama di sekitar wajah
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(
                frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED
            )
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(
                frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1
            )

        # Encode frame sebagai JPEG
        _, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


# Endpoint untuk stream CCTV berdasarkan ID
@app.route("/api/video_feed/<int:cctv_id>")
def video_feed(cctv_id):
    cctv_list = load_cctv_list()
    cctv = next((c for c in cctv_list if c["id"] == cctv_id), None)
    if not cctv:
        return "CCTV tidak ditemukan", 404
    return Response(
        generate_frames(cctv["url"]),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    app.run(debug=True, host=HOST, port=PORT)
