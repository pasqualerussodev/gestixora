from flask import Flask, render_template, session, send_from_directory
from config import Config
from flask_wtf.csrf import CSRFProtect
import db
from auth import auth_bp
from tickets import tickets_bp
import os

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)

# Crea la cartella per gli upload se non esiste
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Inizializza il database all'avvio dell'applicazione
db.init_db()

# Registra i blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(tickets_bp)

@app.route('/')
def index():
    conn = db.get_db_connection()
    tickets = conn.execute("""
        SELECT t.*, u.username
        FROM tickets t
        JOIN users u ON t.user_id = u.id
        ORDER BY t.created_at DESC
    """).fetchall()
    conn.close()
    return render_template("index.html", tickets=tickets)

# ✅ Nuova route per servire gli allegati
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
