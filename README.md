# 🌍 Disaster Relief Resource Allocation System

A **DBMS-based web application** designed to efficiently manage and allocate disaster relief resources during emergencies such as floods, earthquakes, or cyclones.

This system acts as a **centralized platform** to track relief camps, victims, supplies, and donations, ensuring fair and timely distribution of resources.

---

## 📌 Problem Statement
During disasters, relief operations often rely on manual records or scattered spreadsheets, leading to delays, shortages, and mismanagement. There is a need for a centralized, automated system to coordinate relief efforts effectively.

---

## 🎯 Project Objectives
- Create a **centralized database** for disaster relief data
- Provide an **easy-to-use web interface** for relief workers
- Automatically **match resource demand with available supplies**
- Generate **alerts** for low stock of critical resources
- Enable **report generation** for better decision-making

---

## 🏗️ System Architecture

### 🔹 Backend (The Brain)
- **MySQL Database**
  - Stores data related to regions, relief camps, victims, supplies, and donations
  - Uses **triggers** for low-stock alerts
  - Uses **stored procedures** for resource allocation logic
- **Python Flask**
  - Handles communication between frontend and database
  - Processes user requests securely

### 🔹 Frontend (The Face)
- **HTML** – Page structure  
- **CSS** – Styling and layout    

---

## ⚙️ How It Works
1. Relief workers interact with the web interface
2. Data is sent to the Flask backend
3. Backend processes requests and updates the MySQL database
4. Triggers and procedures automate alerts and allocation
5. Reports help administrators monitor operations

---

## 🛠️ Tools & Technologies
- **Frontend:** HTML, CSS  
- **Backend:** Python (Flask)  
- **Database:** MySQL  
- **Development Tool:** VS Code  

---

## 👩‍💻 Authors
- **Vedika Jindal** (2401030030)  
- **Vedika Dureja** (2401030014)  
- **Shreya Sharma** (2401030008)  

Jaypee Institute of Information Technology, Noida
