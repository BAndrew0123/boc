# Body of Christ Centre (BOC) Web Application & Desktop Admin Panel

A secure, full-stack application built for **Body of Christ Centre (Limuru, Kenya)** with interactive donation processing (M-Pesa STK Push simulation, Paybill, Card processing), community activity tracking, children sponsorship & development project management, and an **Isolated Standalone Desktop Admin Application** for staff.

---

## 🔒 Security Architecture: Zero Web Admin Footprint

To prevent brute-force attacks, credential stuffing, and unauthorized web login attempts, **the public web application contains ZERO admin login pages or web admin routes**.

* **Public Web Portal (`app.py`)**: Runs strictly public-facing pages and donation API endpoints.
* **Staff Control Panel (`admin_app.py`)**: Runs as a **Standalone Desktop GUI Application** on authorized staff computers, directly managing the database and exporting CSV ledgers locally.

---

## 🌟 Key Features

### 1. **Public Web Portal (`python app.py`)**
* **Home Page (`/`)**: Hero banner, live donation impact counters (160+ children, KES total raised, donor count), Pastor Mary Watare Mbugua founder story, active causes, upcoming activities preview, M-Pesa Paybill quick banner.
* **About Us (`/about`)**: Comprehensive history of Pastor Mary Mbugua (2004 foundation), mission, vision, core values, location details in Mutarakwa Village, Limuru.
* **Donation Hub (`/donate`)**:
  * **M-Pesa Express STK Push Simulator**: Enter donor name, phone number (`07...` or `254...`), amount, and target cause -> Triggers simulated STK phone prompt modal -> Verifies PIN and generates an **Official Digital Receipt** with simulated M-Pesa reference code (e.g. `QK892XLP90`).
  * **M-Pesa Paybill**: Clear step-by-step instructions for Paybill **400200** (Account: **BOC**).
  * **Credit / Debit Card Payment**: Live card form simulation with printable digital receipt.
* **Activities & Events (`/activities`)**: Browse community drives, medical camps, and workshops with an interactive **Volunteer Sign-Up Modal** per event.
* **Children & Projects (`/children-projects`)**: Student academic progress tracking (Law, Journalism, High Schoolers) & campus infrastructure progress bars (Dormitory, Solar Borehole Water).
* **Media Gallery (`/gallery`)**: Image gallery with filterable lightbox viewer.
* **Contact Us (`/contact`)**: Interactive inquiry form saving messages directly to the admin inbox, contact numbers, and physical address.

---

### 2. **Standalone Desktop Admin App (`python admin_app.py`)**
* **Security Passcode Prompt**: Asks for staff passcode on launch (`admin123`).
* **Financial Summary Dashboard**: KPI cards for Total Raised, M-Pesa Total, Card Total, Volunteers, Children Tracked.
* **Donations Ledger**: Search & filter by donor name, phone number, M-Pesa code, or cause; view status and timestamps.
* **One-Click CSV Export**: Download `boc_donations_ledger.csv` directly to the staff computer.
* **Record Cash / Offline Donation**: Manually enter cash, cheque, or bank wire donations into the database.
* **Events & Activities Manager**: Create, publish, or remove upcoming volunteer events.
* **Children & Projects Tracker**: Add new student sponsorship profiles or project goals.
* **Inquiries Inbox**: View messages submitted through the public contact form.

---

## 🚀 How to Run the Applications

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Start the Public Web Portal**
```bash
python app.py
```
* Open [http://localhost:5000](http://localhost:5000) in your browser.

### 3. **Launch the Staff Desktop Admin Panel**
In a new terminal window or on a staff computer:
```bash
python admin_app.py
```
* **Staff Passcode**: `admin123`

---

## 📁 Project Structure

```
/home/joe/Documents/python/Python/BOC/
├── app.py                     # Public Flask backend server & REST API endpoints (No admin web routes)
├── admin_app.py               # Standalone Staff Desktop Application (Tkinter GUI with Passcode Lock)
├── database.db                # SQLite database (auto-created and seeded on first run)
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation & usage instructions
├── static/
│   ├── css/
│   │   └── style.css          # Custom styling & M-Pesa STK phone modal styles
│   └── js/
│       └── main.js            # M-Pesa STK engine, payment modals, AJAX requests
└── templates/
    ├── base.html              # Base layout template (Zero web admin links)
    ├── index.html             # Home page with hero, stats & cause cards
    ├── about.html             # Founder history & mission
    ├── donate.html            # M-Pesa STK Push, Paybill & Card donation hub
    ├── activities.html        # Events & volunteer sign-up modals
    ├── children.html          # Student sponsorship & project progress tracking
    ├── gallery.html           # Media photo gallery with lightbox viewer
    └── contact.html           # Contact form & location information
```
# boc
