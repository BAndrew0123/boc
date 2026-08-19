// Body of Christ Centre (BOC) Main JavaScript & Full DOM Swahili Translation Engine

const swahili_translations = [
    // Navigation & Buttons
    ["Home", "Nyumbani"],
    ["About Us", "Kuhusu Sisi"],
    ["Activities & Events", "Matukio na Shughuli"],
    ["Children & Projects", "Watoto na Miradi"],
    ["Gallery", "Picha na Media"],
    ["Contact Us", "Wasiliana Nasi"],
    ["DONATE NOW", "CHANGIA SASA"],
    ["Donate Now", "Changia Sasa"],
    ["Make a Difference Today", "Fanya Tofauti Leo"],
    ["Our Founder & Story", "Hadithi na Mwanzilishi"],
    ["Our Story & Founder", "Hadithi na Mwanzilishi"],
    ["Read Our Full History & Mission", "Soma Historia na Dira Yetu"],
    
    // Stats & Headings
    ["Children Boarded", "Watoto Wanaohudumiwa"],
    ["Years of Service", "Miaka ya Huduma"],
    ["Total Verified Raised", "Jumla ya Michango"],
    ["Generous Donors", "Wachangiaji"],
    ["Our Journey of Hope", "Safari Yetu ya Matumaini"],
    ["A Safe Haven Born Out of Compassion & Faith", "Kituo Salama Kilichozaliwa kwa Upendo na Imani"],
    ["Full Education", "Elimu Kamili"],
    ["Holistic Care", "Malezi Bora"],
    ["School fees, uniforms, and textbooks provided.", "Karo ya shule, sare, na vitabu vinatolewa."],
    ["Healthcare, nutrition, and counseling support.", "Huduma za afya, chakula bora na ushauri."],
    
    // Section Titles
    ["Causes We Champion", "Miradi Tunayosaidia"],
    ["Support Active Projects & Children", "Saidia Watoto na Miradi"],
    ["Donate to Cause", "Changia Mradi"],
    ["Upcoming Activities & Events", "Matukio na Shughuli Zijazo"],
    ["View All Activities", "Ona Shughuli Zote"],
    ["Volunteer Sign Up", "Jiandikishe Mjitolea"],
    ["Sign Up to Volunteer", "Jiandikishe Mjitolea"],
    
    // M-Pesa & Payment
    ["Pay Directly via M-Pesa Paybill", "Lipa Direct Kupitia M-Pesa Paybill"],
    ["Submit M-Pesa Code for Receipt", "Weka Nambari ya M-Pesa Kupata Risiti"],
    ["DONATE NOW VIA M-PESA STK PUSH", "CHANGIA SASA KUPITIA M-PESA"],
    ["Official M-Pesa Channel", "Njia Rasmi ya M-Pesa"],
    ["Step-by-Step Payment Instructions", "Maagizo ya Malipo"],
    ["Business / Paybill No.", "Nambari ya Paybill"],
    ["Account Name", "Jina la Akaunti"],
    ["Full Name", "Jina Kamili"],
    ["M-Pesa Phone Number", "Nambari ya Simu ya M-Pesa"],
    ["Email Address", "Anwani ya Barua Pepe"],
    ["Select Cause / Project", "Chagua Mradi"],
    ["Select Donation Amount (KES)", "Chagua Kiasi cha Kuchangia (KES)"],
    ["VERIFY CODE & GENERATE OFFICIAL RECEIPT", "THIBITISHA NAMBARI NA UPATE RISITI"],
    ["Direct Bank Transfer Details", "Maelezo ya Benki"],
    ["Bank Name", "Jina la Benki"],
    ["Branch", "Tawi"],
    ["Print / Download PDF Receipt", "Chapisha Risiti ya PDF"],
    ["Print Official Receipt", "Chapisha Risiti"],
    
    // About & Contact
    ["Who We Are", "Sisi ni Nani"],
    ["About Body of Christ Centre", "Kuhusu Kituo cha Body of Christ"],
    ["Our Founder & History", "Mwanzilishi na Historia"],
    ["Our Mission", "Dira Yetu"],
    ["Our Vision", "Dhamira Yetu"],
    ["Core Values", "Maadili Yetu"],
    ["Mutarakwa Village, Limuru", "Kijiji cha Mutarakwa, Limuru"],
    ["Plan a Visit / Get Directions", "Panga Kutembelea"],
    ["Send Us a Message", "Tutumie Ujumbe"],
    ["Your Name", "Jina Lako"],
    ["Subject", "Mada"],
    ["Your Message", "Ujumbe Wako"],
    ["SEND MESSAGE NOW", "TUMA UJUMBE SASA"],
    ["Contact Information", "Mawasiliano"],
    ["Physical Address", "Anwani"],
    ["Phone Numbers", "Nambari za Simu"],
    ["Visiting Hours", "Saa za Kutembelea"],
    ["Ways to Give", "Njia za Kuchangia"],
    ["Quick Links", "Viungo vya Haraka"],
    ["English", "English"],
    ["Kiswahili", "Kiswahili"]
];

let originalDOMTextMap = new Map();

function storeOriginalText(node) {
    if (node.nodeType === Node.TEXT_NODE && node.nodeValue.trim().length > 0) {
        if (!originalDOMTextMap.has(node)) {
            originalDOMTextMap.set(node, node.nodeValue);
        }
    } else {
        for (let child of node.childNodes) {
            storeOriginalText(child);
        }
    }
}

function translateDOMToSwahili() {
    originalDOMTextMap.forEach((origText, node) => {
        let newText = origText;
        for (let [eng, sw] of swahili_translations) {
            if (newText.includes(eng)) {
                newText = newText.replaceAll(eng, sw);
            }
        }
        node.nodeValue = newText;
    });
}

function restoreDOMToEnglish() {
    originalDOMTextMap.forEach((origText, node) => {
        node.nodeValue = origText;
    });
}

function switchLanguage(lang) {
    localStorage.setItem('boc_lang', lang);

    const btnEn = document.getElementById('btn-lang-en');
    const btnSw = document.getElementById('btn-lang-sw');

    if (lang === 'sw') {
        if (btnSw) { btnSw.className = "font-extrabold text-brand bg-slate-800 px-2 py-0.5 rounded"; }
        if (btnEn) { btnEn.className = "font-bold text-slate-400 hover:text-white"; }
        translateDOMToSwahili();
    } else {
        if (btnEn) { btnEn.className = "font-extrabold text-white bg-slate-800 px-2 py-0.5 rounded"; }
        if (btnSw) { btnSw.className = "font-bold text-slate-400 hover:text-white"; }
        restoreDOMToEnglish();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('BOC Web Application Full DOM Translator Loaded.');
    
    // Save original DOM text nodes
    storeOriginalText(document.body);

    // Apply saved language preference
    const savedLang = localStorage.getItem('boc_lang') || 'en';
    if (savedLang === 'sw') {
        switchLanguage('sw');
    }

    // Initialize Mobile Navigation Toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Modal close buttons helper
    document.querySelectorAll('[data-modal-close]').forEach(btn => {
        btn.addEventListener('click', function() {
            const modalId = this.getAttribute('data-modal-close');
            const modal = document.getElementById(modalId);
            if (modal) modal.classList.add('hidden');
        });
    });
});

// STK Push Payment Handler
function submitMpesaStk(event) {
    event.preventDefault();
    const btn = document.getElementById('stk-submit-btn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Sending STK Push to Phone...';
    btn.disabled = true;

    const payload = {
        donor_name: document.getElementById('stk_name').value,
        donor_email: document.getElementById('stk_email').value,
        donor_phone: document.getElementById('stk_phone').value,
        amount: parseFloat(document.getElementById('stk_amount').value),
        cause_title: document.getElementById('stk_cause').value
    };

    fetch('/api/donate/mpesa-stk', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        btn.innerHTML = originalText;
        btn.disabled = false;
        if (data.status === 'success') {
            document.getElementById('receipt-donor-name').textContent = data.donor_name;
            document.getElementById('receipt-amount').textContent = 'KES ' + parseFloat(data.amount).toLocaleString('en-US', {minimumFractionDigits: 2});
            document.getElementById('receipt-mpesa-code').textContent = data.mpesa_code || data.checkout_request_id;
            document.getElementById('receipt-cause').textContent = data.cause;
            document.getElementById('receipt-timestamp').textContent = data.timestamp;

            document.getElementById('receipt-modal').classList.remove('hidden');
        } else {
            alert(data.message || 'Error processing STK Push.');
        }
    })
    .catch(err => {
        btn.innerHTML = originalText;
        btn.disabled = false;
        alert('Network error initiating M-Pesa STK Push.');
    });
}

// Card Payment Processing
function submitCardPayment(event) {
    event.preventDefault();
    const form = event.target;
    
    const payload = {
        donor_name: form.donor_name.value,
        donor_email: form.donor_email.value,
        donor_phone: form.donor_phone.value,
        amount: parseFloat(form.amount.value),
        cause_title: form.cause_title.value
    };

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Processing Payment...';
    submitBtn.disabled = true;

    fetch('/api/donate/card', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
        if (data.status === 'success') {
            document.getElementById('receipt-donor-name').textContent = data.donor_name;
            document.getElementById('receipt-amount').textContent = 'KES ' + parseFloat(data.amount).toLocaleString('en-US', {minimumFractionDigits: 2});
            document.getElementById('receipt-mpesa-code').textContent = data.mpesa_code;
            document.getElementById('receipt-cause').textContent = data.cause;
            document.getElementById('receipt-timestamp').textContent = data.timestamp;

            document.getElementById('receipt-modal').classList.remove('hidden');
        }
    })
    .catch(err => {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
        alert('Payment failed. Please try again.');
    });
}

// Volunteer Registration Submission
function submitVolunteerSignup(event, activityId) {
    event.preventDefault();
    const form = event.target;
    
    const payload = {
        activity_id: activityId,
        name: form.name.value,
        email: form.email.value,
        phone: form.phone.value,
        notes: form.notes ? form.notes.value : ''
    };

    fetch('/api/volunteer/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            alert(data.message);
            form.reset();
            const modal = document.getElementById(`volunteer-modal-${activityId}`);
            if (modal) modal.classList.add('hidden');
        }
    })
    .catch(err => {
        alert('Error signing up for volunteer work. Please try again.');
    });
}
