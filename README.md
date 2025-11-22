# Face Recognition Attendance System

A modern, contactless attendance system using face recognition and Flask. Students register their face via webcam, and attendance is marked with a simple scan. Admins can manage requests and view statistics. Built with Python, Flask, MongoDB, and face_recognition.

---

## Features
- AI-powered face recognition for secure, fast attendance
- Webcam-based registration and attendance
- Admin approval for new signups
- Real-time statistics and reporting
- Cloud-based with MongoDB Atlas

---

## Installation Guide (Windows)

### 1. **Install Python**
- Download and install Python 3.8–3.11 from [python.org](https://www.python.org/downloads/).
- During installation, check **"Add Python to PATH"**.

### 2. **Install Git (optional, for code download)**
- Download from [git-scm.com](https://git-scm.com/download/win).

### 3. **Install CMake**
- Download the Windows x64 Installer from [cmake.org/download](https://cmake.org/download/).
- Run the installer and **check the box to add CMake to your PATH**.
- After install, verify in Command Prompt:
  ```sh
  cmake --version
  ```

### 4. **Install Visual Studio Build Tools**
- Download from [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
- In the installer, select **"Desktop development with C++"** workload.
- Complete installation (may take several minutes).
- **Restart your computer** after installation.

### 5. **Clone or Download the Project**
- Using Git:
  ```sh
  git clone <your-repo-url>
  cd attendance-system
  ```
- Or download and extract the ZIP, then open the folder in your terminal.

### 6. **Create a Virtual Environment (Recommended)**
```sh
python -m venv venv
venv\Scripts\activate
```

### 7. **Install Python Dependencies**
```sh
pip install --upgrade pip
pip install cmake
pip install -r requirements.txt
```
If you get errors with `dlib`, make sure CMake and Visual Studio Build Tools are installed and in your PATH.

### 8. **MongoDB Atlas Setup**
- Create a free cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
- Whitelist your IP and get your connection string.
- Update `MONGO_URI` in `app.py` with your connection string.

### 9. **Run the Application**
```sh
python app.py
```
- Visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## Troubleshooting
- **dlib install errors:**
  - Ensure CMake and Visual Studio Build Tools are installed and in your PATH.
  - Try installing a pre-built dlib wheel from [Gohlke's Unofficial Windows Binaries](https://www.lfd.uci.edu/~gohlke/pythonlibs/#dlib) if you still have issues.
- **Webcam not working:**
  - Make sure your browser has permission to access the webcam.
- **MongoDB connection errors:**
  - Double-check your connection string and IP whitelist in MongoDB Atlas.

---

## Project Structure
```
attendance-system/
  app.py
  requirements.txt
  README.md
  templates/
    home.html
    login.html
    signup.html
    dashboard.html
    mark_attendance.html
    register_face.html
    ...
```

---

## Credits
- Face recognition icon by [Flat Icons - Flaticon](https://www.flaticon.com/free-icons/facial-recognition)
- Face recognition powered by [face_recognition](https://github.com/ageitgey/face_recognition)
- UI styled with [Tailwind CSS](https://tailwindcss.com/)

---

## License
This project is for educational and demonstration purposes. 