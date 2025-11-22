# Required: pip install flask pymongo face_recognition dlib pillow numpy
from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
import datetime
from bson.objectid import ObjectId
import face_recognition
import numpy as np
import base64
from PIL import Image
from io import BytesIO
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# MongoDB Atlas connection (replace with your actual URI and DB name)
MONGO_URI = 'mongodb+srv://gnana1313:Gnana1212@dbs.8wngtib.mongodb.net/?retryWrites=true&w=majority&appName=DBs'
DB_FACE = 'attendance_face_recognition'
client = MongoClient(MONGO_URI)
db_face = client[DB_FACE]

# Collections (all in db_face)
signup_requests = db_face['signup_requests']
students = db_face['students']
students_face = db_face['students_face']  # For storing face encodings
attendance_face = db_face['attendance_face']  # For storing attendance records
attendance = db_face['attendance']  # If needed for legacy or admin

@app.route('/')
def home():
    return render_template('home.html', year=datetime.datetime.now().year)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message = None
    if request.method == 'POST':
        rollno = request.form['rollno']
        name = request.form['name']
        class_ = request.form['class']
        branch = request.form['branch']
        mobile = request.form['mobile']
        password = request.form['password']
        # Check if already requested or exists
        if signup_requests.find_one({'rollno': rollno}) or students.find_one({'rollno': rollno}):
            message = 'Signup request or account already exists.'
        else:
            signup_requests.insert_one({
                'rollno': rollno,
                'name': name,
                'class': class_,
                'branch': branch,
                'mobile': mobile,
                'password': password
            })
            message = 'Signup request sent. Wait for admin approval.'
    return render_template('signup.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        login_type = request.form.get('login_type')
        if login_type == 'student':
            rollno = request.form['rollno']
            password = request.form['password']
            student = students.find_one({'rollno': rollno, 'password': password})
            if student:
                session['user'] = rollno
                session['role'] = 'student'
                return redirect(url_for('dashboard'))
            else:
                message = 'Invalid credentials or not approved.'
        elif login_type == 'admin':
            username = request.form['username']
            password = request.form['password']
            if username == 'admin' and password == '123456':
                session['user'] = 'admin'
                session['role'] = 'admin'
                return redirect(url_for('admin_dashboard'))
            else:
                message = 'Invalid admin credentials.'
    return render_template('login.html', message=message)

def login_required_student(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session or session.get('role') != 'student':
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/dashboard')
@login_required_student
def dashboard():
    rollno = session['user']
    student = students.find_one({'rollno': rollno})
    student_name = student['name'] if student else ''
    return render_template('dashboard.html', student_name=student_name)

@app.route('/dashboard/profile')
@login_required_student
def profile():
    rollno = session['user']
    student = students.find_one({'rollno': rollno})
    return render_template('profile.html', student=student)

@app.route('/dashboard/mark_attendance', methods=['GET', 'POST'])
@login_required_student
def mark_attendance():
    message = None
    success = False
    rollno = session['user']
    now = datetime.datetime.now()
    slot = None
    slot_enabled = False
    slot_available = True
    available_slot = None
    if now.time() >= datetime.time(8, 0) and now.time() <= datetime.time(10, 0):
        slot = 'Morning'
        slot_enabled = True
    elif now.time() >= datetime.time(12, 30) and now.time() <= datetime.time(18, 30):
        slot = 'Afternoon'
        slot_enabled = True
    # Check if already marked for this slot
    today = now.strftime('%Y-%m-%d')
    if slot_enabled and attendance_face.find_one({'rollno': rollno, 'date': today, 'slot': slot}):
        slot_available = False
    # Determine which slot is available for attendance
    morning_marked = attendance_face.find_one({'rollno': rollno, 'date': today, 'slot': 'Morning'})
    afternoon_marked = attendance_face.find_one({'rollno': rollno, 'date': today, 'slot': 'Afternoon'})
    if not morning_marked and now.time() <= datetime.time(13, 0):
        available_slot = 'Morning'
    elif not afternoon_marked and now.time() >= datetime.time(12, 30) and now.time() <= datetime.time(14, 30):
        available_slot = 'Afternoon'
    else:
        available_slot = None
    if request.method == 'POST':
        if not slot_enabled:
            message = 'Attendance can only be marked during the allowed time slots.'
        elif not slot_available:
            message = 'Attendance already marked for this slot.'
        else:
            face_image_data = request.form.get('face_image_data')
            if not face_image_data:
                message = 'No face image captured.'
            else:
                try:
                    if face_image_data.startswith('data:image'):
                        face_image_data = face_image_data.split(',')[1]
                    img_bytes = base64.b64decode(face_image_data)
                    img = Image.open(BytesIO(img_bytes)).convert('RGB')
                    img_np = np.array(img)
                    faces = face_recognition.face_locations(img_np)
                    if len(faces) == 0:
                        message = 'No face detected in the captured image.'
                    else:
                        encoding = face_recognition.face_encodings(img_np, known_face_locations=faces)[0]
                        student_face = students_face.find_one({'rollno': rollno})
                        if not student_face or not student_face.get('encodings'):
                            message = 'No registered face found. Please register your face first.'
                        else:
                            known_encodings = [np.array(e) for e in student_face['encodings']]
                            matches = face_recognition.compare_faces(known_encodings, encoding, tolerance=0.5)
                            if any(matches):
                                if attendance_face.find_one({'rollno': rollno, 'date': today, 'slot': slot}):
                                    message = 'Attendance already marked for this slot.'
                                    slot_available = False
                                else:
                                    attendance_face.insert_one({'rollno': rollno, 'date': today, 'slot': slot})
                                    message = 'Attendance marked.'
                                    success = True
                                    slot_available = False
                            else:
                                message = 'Face does not match your registered face.'
                except Exception as e:
                    message = 'Invalid image or face recognition error.'
    return render_template('mark_attendance.html', message=message, success=success, slot_enabled=slot_enabled, slot_available=slot_available, slot=slot, available_slot=available_slot)

@app.route('/dashboard/attendance_directory')
@login_required_student
def attendance_directory():
    rollno = session['user']
    records = []
    for att in attendance_face.find({'rollno': rollno}).sort('date', -1):
        records.append({
            'date': att['date'],
            'slot': att['slot'],
            'status': 'Marked'
        })
    return render_template('attendance_directory.html', attendance_records=records)

@app.route('/dashboard/register_face', methods=['GET', 'POST'])
@login_required_student
def register_face():
    message = None
    registered = False
    rollno = session['user']
    student_face = students_face.find_one({'rollno': rollno})
    if student_face and student_face.get('encodings') and len(student_face['encodings']) >= 3:
        registered = True
        message = 'Your face is already registered.'
    elif request.method == 'POST':
        face_images_data = request.form.get('face_images_data')
        if not face_images_data:
            message = 'No face images captured.'
        else:
            try:
                images = []
                encodings = []
                face_images = []
                for data_url in json.loads(face_images_data):
                    if data_url.startswith('data:image'):
                        data_url = data_url.split(',')[1]
                    img_bytes = base64.b64decode(data_url)
                    img = Image.open(BytesIO(img_bytes)).convert('RGB')
                    img_np = np.array(img)
                    faces = face_recognition.face_locations(img_np)
                    if len(faces) == 0:
                        continue
                    encoding = face_recognition.face_encodings(img_np, known_face_locations=faces)[0]
                    encodings.append(encoding.tolist())
                    top, right, bottom, left = faces[0]
                    face_crop = img_np[top:bottom, left:right]
                    face_crop = Image.fromarray(face_crop).resize((200, 200))
                    buffered = BytesIO()
                    face_crop.save(buffered, format="JPEG")
                    face_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    face_images.append(face_b64)
                if len(encodings) < 3:
                    message = 'Please capture at least 3 valid face images.'
                else:
                    if student_face:
                        students_face.update_one({'rollno': rollno}, {'$set': {'encodings': encodings, 'face_images': face_images}})
                    else:
                        students_face.insert_one({'rollno': rollno, 'encodings': encodings, 'face_images': face_images})
                    registered = True
                    message = 'Face registered successfully!'
            except Exception as e:
                message = 'Invalid image or face encoding error.'
    return render_template('register_face.html', message=message, registered=registered)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

def login_required_admin(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session or session.get('role') != 'admin':
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/admin_dashboard')
@login_required_admin
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/admin/requests', methods=['GET', 'POST'])
@login_required_admin
def admin_requests():
    message = None
    if request.method == 'POST':
        rollno = request.form['rollno']
        action = request.form['action']
        req = signup_requests.find_one({'rollno': rollno})
        if req:
            if action == 'approve':
                students.insert_one({
                    'rollno': req['rollno'],
                    'name': req['name'],
                    'class': req['class'],
                    'branch': req['branch'],
                    'mobile': req['mobile'],
                    'password': req['password']
                })
                signup_requests.delete_one({'rollno': rollno})
                message = f"Approved {rollno}."
            elif action == 'reject':
                signup_requests.delete_one({'rollno': rollno})
                message = f"Rejected {rollno}."
    requests_list = list(signup_requests.find())
    return render_template('admin_requests.html', requests=requests_list, message=message)

@app.route('/admin/attendance')
@login_required_admin
def admin_attendance():
    filter_rollno = request.args.get('rollno', '').strip()
    filter_date = request.args.get('date', '').strip()
    now = datetime.datetime.now()
    days_completed = now.day
    total_sessions = days_completed * 2
    student_list = list(students.find())
    attendance_table = []
    session_query = {}
    if filter_date:
        session_query['date'] = filter_date
        total_sessions = 2
    for student in student_list:
        rollno = student['rollno']
        name = student['name']
        if filter_rollno and filter_rollno != rollno:
            continue
        attended = attendance_face.count_documents({'rollno': rollno, **session_query})
        percent = round((attended / total_sessions) * 100, 2) if total_sessions > 0 else 0.0
        attendance_table.append({
            'rollno': rollno,
            'name': name,
            'total_sessions': total_sessions,
            'sessions_attended': attended,
            'attendance_percent': percent
        })
    return render_template('admin_attendance.html', attendance_table=attendance_table, filter_rollno=filter_rollno, filter_date=filter_date, students=student_list)

if __name__ == '__main__':
    app.run(debug=True) 