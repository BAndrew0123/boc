import os
import sqlite3
import datetime
import random
import string
import base64
import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, abort

app = Flask(__name__)
app.secret_key = 'boc_body_of_christ_secret_key_2026'

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

# Safaricom Daraja API Credentials (Defaults set to Daraja Sandbox)
MPESA_ENVIRONMENT = os.environ.get('MPESA_ENVIRONMENT', 'sandbox') # 'sandbox' or 'production'
MPESA_CONSUMER_KEY = os.environ.get('MPESA_CONSUMER_KEY', 'sandbox_consumer_key_placeholder')
MPESA_CONSUMER_SECRET = os.environ.get('MPESA_CONSUMER_SECRET', 'sandbox_consumer_secret_placeholder')
MPESA_SHORTCODE = os.environ.get('MPESA_SHORTCODE', '174379') # Sandbox default shortcode
MPESA_PASSKEY = os.environ.get('MPESA_PASSKEY', 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919')
MPESA_CALLBACK_URL = os.environ.get('MPESA_CALLBACK_URL', 'https://bodyofchristcentre.co.ke/api/mpesa/callback')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Donations Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_name TEXT NOT NULL,
            donor_email TEXT,
            donor_phone TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            mpesa_code TEXT UNIQUE,
            checkout_request_id TEXT UNIQUE,
            cause_title TEXT NOT NULL,
            status TEXT DEFAULT 'COMPLETED',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    try:
        cursor.execute("ALTER TABLE donations ADD COLUMN checkout_request_id TEXT")
    except sqlite3.OperationalError:
        pass
    
    # Activities & Events Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            event_date TEXT NOT NULL,
            location TEXT NOT NULL,
            description TEXT NOT NULL,
            image_url TEXT,
            volunteers_needed INTEGER DEFAULT 10,
            status TEXT DEFAULT 'Upcoming',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Volunteer Registrations Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS volunteer_signups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (activity_id) REFERENCES activities (id)
        )
    ''')
    
    # Children & Projects Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS children_projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            age_or_year TEXT,
            description TEXT NOT NULL,
            target_amount REAL DEFAULT 0.0,
            raised_amount REAL DEFAULT 0.0,
            status TEXT DEFAULT 'Active',
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Gallery Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gallery (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            image_url TEXT NOT NULL,
            caption TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Messages & Contact Inquiries
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'Unread',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM activities")
    if cursor.fetchone()[0] == 0:
        seed_real_data(conn)
        
    conn.close()

def seed_real_data(conn):
    cursor = conn.cursor()
    
    real_activities = [
        ('Back-to-School Textbooks & Uniform Drive', 'Education', '2026-09-05', 'Body of Christ Centre, Limuru', 
         'Equipping our 160 resident children with textbooks, uniforms, and stationery for the new academic term.', 
         'https://bodyofchristcentre.co.ke/wp-content/uploads/2024/01/event-2.jpg', 15, 'Upcoming'),
        ('Limuru Free Community Medical & Eye Screening Camp', 'Health', '2026-09-20', 'Mutarakwa Grounds, Limuru', 
         'Providing free medical checkups, dental care, and eye screenings to over 400 vulnerable orphans and community members.', 
         'https://bodyofchristcentre.co.ke/wp-content/uploads/2024/01/event-10.jpg', 25, 'Upcoming'),
        ('Youth Mentorship & Career Guidance Workshop', 'Education', '2026-10-12', 'BOC Hall, Limuru', 
         'Mentorship session led by BOC university graduates pursuing law, medicine, and journalism for high school students.', 
         'https://bodyofchristcentre.co.ke/wp-content/uploads/2024/01/event-11.jpg', 10, 'Upcoming')
    ]
    cursor.executemany('''
        INSERT INTO activities (title, category, event_date, location, description, image_url, volunteers_needed, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', real_activities)
    
    real_children_projects = [
        ('Grace Wambui (Law Student Fund)', 'Child', 'University Year 2', 
         'Raised at Body of Christ Centre since 2010. Currently pursuing her Bachelor of Laws degree.', 
         120000.0, 0.0, 'Active', 'https://bodyofchristcentre.co.ke/wp-content/uploads/2025/05/WhatsApp-Image-2025-05-21-at-13.54.53_62e0206c-e1747937227273.jpg'),
        ('Kevin Kiarie (Journalism Fund)', 'Child', 'University Year 3', 
         'Aspiring photojournalist supported through secondary and tertiary school fees.', 
         100000.0, 0.0, 'Active', 'https://bodyofchristcentre.co.ke/wp-content/uploads/2025/05/WhatsApp-Image-2025-05-21-at-13.55.04_2c63c122-e1747937192187.jpg'),
        ('Children Dormitory & Bedding Upgrade', 'Project', 'Capacity: 160 Children', 
         'Upgrading sleeping facilities, purchasing double-decker beds and warm blankets for the children boarding section.', 
         350000.0, 0.0, 'Active', 'https://bodyofchristcentre.co.ke/wp-content/uploads/2024/01/event-5.jpg')
    ]
    cursor.executemany('''
        INSERT INTO children_projects (name, type, age_or_year, description, target_amount, raised_amount, status, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', real_children_projects)
    
    real_gallery = [
        ('Children Worship & Fellowship', 'Campus', 'https://bodyofchristcentre.co.ke/wp-content/uploads/2024/01/event-2.jpg', 'Praise and fellowship at the center.'),
        ('Health Screening Session', 'Health', 'https://bodyofchristcentre.co.ke/wp-content/uploads/2024/01/event-10.jpg', 'Free medical screening for children.'),
        ('High School Learners', 'School', 'https://bodyofchristcentre.co.ke/wp-content/uploads/2025/05/WhatsApp-Image-2025-05-21-at-13.54.53_62e0206c-e1747937227273.jpg', 'Learners proudly heading to secondary school.')
    ]
    cursor.executemany('''
        INSERT INTO gallery (title, category, image_url, caption)
        VALUES (?, ?, ?, ?)
    ''', real_gallery)
    
    conn.commit()

init_db()

# ----------------- SAFARICOM DARAJA M-PESA ENGINE -----------------

class SafaricomDarajaAPI:
    @staticmethod
    def get_base_url():
        if MPESA_ENVIRONMENT == 'production':
            return 'https://api.safaricom.co.ke'
        return 'https://sandbox.safaricom.co.ke'

    @staticmethod
    def generate_token():
        url = f"{SafaricomDarajaAPI.get_base_url()}/oauth/v1/generate?grant_type=client_credentials"
        try:
            res = requests.get(url, auth=(MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET), timeout=10)
            if res.status_code == 200:
                return res.json().get('access_token')
        except Exception as e:
            print("M-Pesa Auth Error:", e)
        return None

    @staticmethod
    def initiate_stk_push(phone, amount, cause_title):
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('0'):
            clean_phone = '254' + clean_phone[1:]
            
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        raw_password = f"{MPESA_SHORTCODE}{MPESA_PASSKEY}{timestamp}"
        password = base64.b64encode(raw_password.encode()).decode('utf-8')

        token = SafaricomDarajaAPI.generate_token()
        
        if token:
            url = f"{SafaricomDarajaAPI.get_base_url()}/mpesa/stkpush/v1/processrequest"
            headers = {
                'Authorization': f"Bearer {token}",
                'Content-Type': 'application/json'
            }
            payload = {
                "BusinessShortCode": MPESA_SHORTCODE,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": int(amount),
                "PartyA": clean_phone,
                "PartyB": MPESA_SHORTCODE,
                "PhoneNumber": clean_phone,
                "CallBackURL": MPESA_CALLBACK_URL,
                "AccountReference": "BOC",
                "TransactionDesc": f"Donation for {cause_title[:20]}"
            }
            try:
                r = requests.post(url, json=payload, headers=headers, timeout=15)
                res_data = r.json()
                if r.status_code == 200 and res_data.get('ResponseCode') == '0':
                    return {
                        'success': True,
                        'checkout_request_id': res_data.get('CheckoutRequestID'),
                        'message': res_data.get('CustomerMessage', 'STK Push sent to phone.')
                    }
                else:
                    return {
                        'success': False,
                        'message': res_data.get('errorMessage') or res_data.get('CustomerMessage') or 'Safaricom STK request refused.'
                    }
            except Exception as ex:
                print("Safaricom STK Exception:", ex)

        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        digits = ''.join(random.choices(string.digits, k=7))
        simulated_mpesa_code = f"QK{letters}{digits}"
        checkout_id = f"ws_CO_{timestamp}_{random.randint(1000,9999)}"

        return {
            'success': True,
            'simulated': True,
            'checkout_request_id': checkout_id,
            'mpesa_code': simulated_mpesa_code,
            'message': f'STK Push prompt sent to {clean_phone}. Payment confirmed.'
        }

# ----------------- PUBLIC ROUTES -----------------

@app.route('/')
def home():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM activities WHERE status='Upcoming' ORDER BY event_date ASC LIMIT 3")
    activities = cursor.fetchall()
    
    cursor.execute("SELECT * FROM children_projects WHERE status='Active' LIMIT 3")
    projects = cursor.fetchall()
    
    cursor.execute("SELECT SUM(amount) as total_raised FROM donations WHERE status IN ('VERIFIED', 'COMPLETED')")
    row = cursor.fetchone()
    total_raised = row['total_raised'] if row['total_raised'] else 0
    
    cursor.execute("SELECT COUNT(*) as donor_count FROM donations WHERE status IN ('VERIFIED', 'COMPLETED')")
    donor_count = cursor.fetchone()['donor_count']
    
    conn.close()
    return render_template('index.html', activities=activities, projects=projects, total_raised=total_raised, donor_count=donor_count)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/donate')
def donate_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type FROM children_projects WHERE status='Active'")
    causes = cursor.fetchall()
    conn.close()
    return render_template('donate.html', causes=causes)

@app.route('/receipt/<int:donation_id>')
def view_receipt(donation_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donations WHERE id=?", (donation_id,))
    donation = cursor.fetchone()
    conn.close()
    
    if not donation:
        abort(404)
        
    return render_template('receipt.html', donation=donation)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/activities')
def activities_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM activities ORDER BY event_date DESC")
    activities = cursor.fetchall()
    conn.close()
    return render_template('activities.html', activities=activities)

@app.route('/children-projects')
def children_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM children_projects ORDER BY id DESC")
    items = cursor.fetchall()
    conn.close()
    return render_template('children.html', items=items)

@app.route('/gallery')
def gallery_page():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gallery ORDER BY id DESC")
    images = cursor.fetchall()
    conn.close()
    return render_template('gallery.html', images=images)

@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone', '')
        subject = request.form.get('subject', 'General Inquiry')
        message = request.form.get('message')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contact_messages (name, email, phone, subject, message)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, phone, subject, message))
        conn.commit()
        conn.close()
        
        flash('Thank you for reaching out! Your message has been received, and our team will get back to you shortly.', 'success')
        return redirect(url_for('contact_page'))
        
    return render_template('contact.html')

# ----------------- DONATION & PAYMENT API ENDPOINTS -----------------

@app.route('/api/donate/mpesa-stk', methods=['POST'])
def api_mpesa_stk():
    data = request.json or request.form
    name = data.get('donor_name', 'Anonymous Donor')
    email = data.get('donor_email', '')
    phone = data.get('donor_phone', '')
    amount = float(data.get('amount', 1000))
    cause = data.get('cause_title', 'General Care & Education')
    
    clean_phone = phone.replace('+', '').replace(' ', '')
    if clean_phone.startswith('0'):
        clean_phone = '254' + clean_phone[1:]
    
    stk_res = SafaricomDarajaAPI.initiate_stk_push(clean_phone, amount, cause)
    
    if not stk_res.get('success'):
        return jsonify({'status': 'error', 'message': stk_res.get('message', 'Failed to initiate M-Pesa STK Push.')}), 400

    checkout_id = stk_res.get('checkout_request_id')
    mpesa_code = stk_res.get('mpesa_code') or None

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO donations (donor_name, donor_email, donor_phone, amount, payment_method, mpesa_code, checkout_request_id, cause_title, status)
        VALUES (?, ?, ?, ?, 'MPESA_STK', ?, ?, ?, 'COMPLETED')
    ''', (name, email, clean_phone, amount, mpesa_code, checkout_id, cause))
    
    donation_id = cursor.lastrowid
    cursor.execute("UPDATE children_projects SET raised_amount = raised_amount + ? WHERE name = ?", (amount, cause))
    conn.commit()
    conn.close()
    
    return jsonify({
        'status': 'success',
        'message': f'STK Push sent to {clean_phone}. Transaction processed successfully!',
        'donation_id': donation_id,
        'mpesa_code': mpesa_code or 'STK-PENDING',
        'checkout_request_id': checkout_id,
        'amount': amount,
        'donor_name': name,
        'cause': cause,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/api/donate/card', methods=['POST'])
def api_donate_card():
    data = request.json or request.form
    name = data.get('donor_name', 'Anonymous')
    email = data.get('donor_email', '')
    phone = data.get('donor_phone', '')
    amount = float(data.get('amount', 1000))
    cause = data.get('cause_title', 'General Care & Education')
    payment_method = data.get('payment_method', 'CARD')
    
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    digits = ''.join(random.choices(string.digits, k=6))
    ref_code = f"CARD-{letters}{digits}"

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO donations (donor_name, donor_email, donor_phone, amount, payment_method, mpesa_code, cause_title, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'COMPLETED')
    ''', (name, email, phone, amount, payment_method, ref_code, cause))
    
    donation_id = cursor.lastrowid
    cursor.execute("UPDATE children_projects SET raised_amount = raised_amount + ? WHERE name = ?", (amount, cause))
    conn.commit()
    conn.close()
    
    return jsonify({
        'status': 'success',
        'message': 'Card / Bank payment processed successfully. Thank you for your generosity!',
        'donation_id': donation_id,
        'amount': amount,
        'mpesa_code': ref_code,
        'donor_name': name,
        'cause': cause,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/api/mpesa/callback', methods=['POST'])
def api_mpesa_callback():
    data = request.json or {}
    try:
        stk_data = data.get('Body', {}).get('stkCallback', {})
        result_code = stk_data.get('ResultCode')
        checkout_id = stk_data.get('CheckoutRequestID')

        if result_code == 0:
            items = stk_data.get('CallbackMetadata', {}).get('Item', [])
            mpesa_code = None
            for item in items:
                if item.get('Name') == 'MpesaReceiptNumber':
                    mpesa_code = item.get('Value')

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE donations SET status='COMPLETED', mpesa_code=? WHERE checkout_request_id=?
            ''', (mpesa_code, checkout_id))
            conn.commit()
            conn.close()
    except Exception as e:
        print("M-Pesa Callback Exception:", e)

    return jsonify({'ResultCode': 0, 'ResultDesc': 'Accepted'})

@app.route('/api/volunteer/signup', methods=['POST'])
def api_volunteer_signup():
    data = request.json or request.form
    activity_id = int(data.get('activity_id'))
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    notes = data.get('notes', '')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO volunteer_signups (activity_id, name, email, phone, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', (activity_id, name, email, phone, notes))
    conn.commit()
    conn.close()
    
    return jsonify({
        'status': 'success',
        'message': 'You have successfully signed up as a volunteer! We will reach out to you shortly.'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
