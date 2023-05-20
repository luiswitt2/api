import cv2
import face_recognition
import mysql.connector

# Conectando ao banco de dados MySQL
db = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="yourdatabase"
)

# Capturando imagens da câmera e calculando a codificação da face
def capture_face():
    video_capture = cv2.VideoCapture(0)
    face_locations = []
    face_encodings = []

    while len(face_locations) < 10:
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    video_capture.release()

    return face_encodings[0]

# Armazenando a codificação da face no banco de dados
def store_face(name, face_encoding):
    cursor = db.cursor()
    sql = "INSERT INTO faces (name, face_encoding) VALUES (%s, %s)"
    val = (name, face_encoding.tostring())
    cursor.execute(sql, val)
    db.commit()

# Reconhecendo a face a partir da codificação
def recognize_face(face_encoding):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM faces")
    result = cursor.fetchall()

    for row in result:
        stored_face_encoding = numpy.fromstring(row[2], dtype=float)
        distance = face_recognition.face_distance([stored_face_encoding], face_encoding)
        if distance < 0.6:
            return row[1]

    return "Desconhecido"

# Capturando a imagem da câmera e reconhecendo a face
def recognize_from_camera():
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        if len(face_encodings) > 0:
            name = recognize_face(face_encodings[0])
