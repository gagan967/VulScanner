# 🛡️ Vulnerability Scanner Project

This project consists of three parts that need to run simultaneously.

## 🚀 How to Run

Please open **3 separate terminal windows** and run the following commands:

### Terminal 1: The Backend API
This powers the data and logic.
```powershell
cd backend
uvicorn app.main:app --reload
```
*You should see: `Uvicorn running on http://127.0.0.1:8000`*

### Terminal 2: The Scanner Service
This runs in the background to find installed software and check for CVEs.
```powershell
cd backend
python continuous_scanner.py
```
*You should see: `Continuous Vulnerability Scanner Service Started`*

### Terminal 3: The Frontend UI
This is the web dashboard.
```powershell
cd frontend
ng serve
```
*You should see: `Active on http://localhost:4200`*

---

## 🌐 Open the App
Once everything is running, open your browser and go to:
**[http://localhost:4200](http://localhost:4200)**

## ❓ Troubleshooting
- **Backend Error?** Make sure you installed requirements: `pip install -r backend/requirements.txt`
- **Frontend Error?** Make sure you installed packages: `cd frontend` then `npm install`
