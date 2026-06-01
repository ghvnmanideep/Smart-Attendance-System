# 📸 Smart Face Recognition Attendance System

A modern, contactless attendance management system powered by AI face recognition and built with Flask. Securely register student faces, log attendance effortlessly, and manage records through an intuitive, fully responsive dashboard.

---

## ✨ Key Features

- **🤖 AI-Powered Face Recognition**: Secure and fast contactless attendance using the advanced `face_recognition` library.
- **📱 Fully Responsive UI**: A modern interface built with Tailwind CSS, featuring glassmorphism and fully collapsible sidebars for mobile.
- **👨‍💼 Admin & Student Dashboards**: Dedicated portals for students (to register faces and view history) and admins (to approve signups and manage records).
- **📊 Real-Time Analytics & CSV Export**: Admins can instantly view attendance statistics, filter by dates or names, and export records to CSV.
- **☁️ Cloud Database**: Powered by MongoDB Atlas for secure, distributed data storage.
- **🚀 Production Ready**: Configured for seamless deployment on Render using Gunicorn (Linux) or Waitress (Windows).

---

## 📷 How It Works

1. **Student Registration**: Students create an account and capture 3 distinct angles of their face using their webcam.
2. **Admin Approval**: An administrator reviews and approves the pending signup request.
3. **Daily Attendance**: Students log in during allowed time slots and scan their face. The AI instantly verifies their identity and marks their attendance!

---

## 🛠️ Installation & Setup (Local Development)

### 1. Prerequisites
- **Python 3.8+** (Ensure Python is added to your PATH)
- **CMake** & **Visual Studio C++ Build Tools** (Required to compile the `dlib` dependency for face recognition on Windows)
- **MongoDB Atlas** Account

### 2. Clone the Repository
```sh
git clone <your-repo-url>
cd attendance-system
```

### 3. Install Dependencies
It's highly recommended to use a virtual environment.
```sh
python -m venv venv
venv\Scripts\activate  # On Windows
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure MongoDB
1. Create a free cluster on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Set up a Database User and whitelist your IP address.
3. Replace the `MONGO_URI` variable in `app.py` with your connection string.

### 5. Run the Application
For local testing using the Waitress production server:
```sh
waitress-serve --port=5000 app:app
```
Then, open your browser and visit: `http://localhost:5000`

---

## 🚀 Deployment (Render)

This application is configured for easy deployment on [Render](https://render.com/).

1. Create a **New Web Service** and connect this GitHub repository.
2. Set the **Build Command** to: `pip install -r requirements.txt`
3. Set the **Start Command** to: `gunicorn app:app`
4. Add an **Environment Variable** named `MONGO_URI` with your MongoDB connection string.
5. Click **Deploy**!

---

## 🐛 Troubleshooting

- **`dlib` Installation Errors**: This is the most common issue on Windows. You **must** install CMake and the "Desktop development with C++" workload via Visual Studio Build Tools *before* installing `requirements.txt`.
- **Webcam Access Denied**: Ensure your browser has permission to access the camera, and that no other application is currently using it.

---

## 📄 License
This project is for educational and demonstration purposes.