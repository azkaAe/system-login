
from flask import Flask, render_template, request, session, redirect
import os

app = Flask(__name__)
# Key ini penting untuk menyimpan data sesi (jumlah percobaan)
app.secret_key = 'hacker_mode_on' 

# CONFIGURATION
CORRECT_PIN = "040908"  # PIN yang benar untuk membuka akses
TARGET_FILE = "SECRETFORMULA"

def wipe_sensitive_data():
    if os.path.exists("SECRETFORMULA"):
        os.remove("SECRETFORMULA")
        return True
    return False

@app.route('/', methods=['GET', 'POST'])
def index():
    # Inisialisasi percobaan (3x) jika sesi baru dimulai
    if 'attempts' not in session:
        session['attempts'] = 3

    error_message = ""

    if request.method == 'POST':
        user_input = request.form.get('code_input')

        # 1. Validasi PIN Benar
       
        if user_input == CORRECT_PIN:
            session['attempts'] = 3
            return render_template('Succes.html') 
            
        # 2. Validasi PIN Salah
        else:
            session['attempts'] -= 1
            
            if session['attempts'] <= 0:
                wipe_sensitive_data()
                return "<h1 style='color:red; text-align:center; background:black; height:100vh; padding-top:20%;'>[ SYSTEM TERMINATED: DATA WIPED ]</h1>"
            else:
                error_message = f"INVALID CODE. {session['attempts']} ATTEMPTS REMAINING."

    return render_template('Index.html', msg=error_message)
    
if __name__ == '__main__':
    app.run(debug=True)
