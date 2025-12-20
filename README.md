
# MediConnect - Effortless Medicine Tracking

**MediConnect** simplifies medicine tracking and availability for pharmacies and users, ensuring you never run out of essential medications when you need them most.

---

## 🏆 Achievements

- **Winner**: CodeUtsava 8.0 (Open Innovation Category) - *Developed in a 28-hour hackathon*
- **2nd Runner-Up**: Ignition Business Model Competition at E-Summit 2025 (NIT Raipur)

## 🚀 Overview

MediConnect is a comprehensive solution addressing critical healthcare challenges such as missed medicine doses, pharmacy stock shortages, emergency medicine access, and communication gaps between pharmacies and customers.

**Key Features:**
- **Real-Time Medicine Tracking**: Locate medicines in your vicinity instantly.
- **Interactive Maps**: Leverages Leaflet.js to display nearby medical stores based on user location.
- **Inventory Management**: Real-time updates for pharmacy stocks.
- **Pre-order & Pickup**: Reserve medicines ahead of time.
- **Emergency Locator**: Find open pharmacies in emergencies, reducing search time by 50%.
- **Low-Stock Alerts**: Get notified when essentials are running low via geolocation services.

## 🛠️ Tech Stack

- **Backend Framework**: Python | FastAPI
- **Database**: MongoDB
- **Deployment**: Vercel (Ready)
- **Frontend Integration**: JavaScript (Consumed by [MediConnect-Frontend](https://github.com/swastikd16/MediConnect-Frontend))

## 📦 Installation & Setup

Follow these steps to set up the backend locally:

### Prerequisites
- Python 3.8 or higher
- MongoDB instance (Local or Cloud)

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/TechShreyash/MediConnectBackend
   cd MediConnectBackend
   ```

2. **Install Dependencies**
   It is recommended to use a virtual environment.
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup**
   Ensure you have your MongoDB connection string ready. You may need to configure environment variables (check `utils/database.py` or similar for connection details).

4. **Run the Application**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

## 🔗 Project Links

- **Frontend Repository**: [GitHub Link](https://github.com/swastikd16/MediConnect-Frontend)
- **Devfolio Project**: [MediConnect on Devfolio](https://devfolio.co/projects/mediconnect-effortless-medicine-tracking-dfc8)
- **Pitch Presentation**: [LinkedIn Post & Pitch](https://docs.google.com/presentation/d/1yhJDuZMVcPzsP8YFFA0kj5IbeYseGAQw/edit?slide=id.p1#slide=id.p1)