import datetime
import os
from flask import Blueprint, render_template, redirect, url_for, session, flash, request, current_app
import db
from forms import TicketForm, TicketEditForm
from functools import wraps

tickets_bp = Blueprint('tickets', __name__, template_folder='templates')

# Decoratore per le rotte protette
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash("Effettua il login per accedere a questa pagina.", "warning")
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return wrapper

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@tickets_bp.route('/nuovo', methods=['GET', 'POST'])
@login_required
def nuovo_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        department = form.department.data
        status = "Nuovo"
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_id = session['user_id']
        attachment = None

        if form.attachment.data:
            file = form.attachment.data
            if file and allowed_file(file.filename):
                filename = f"{user_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                attachment = filename

        conn = db.get_db_connection()
        conn.execute("""
            INSERT INTO tickets (user_id, title, description, department, status, created_at, attachment)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, title, description, department, status, created_at, attachment))
        conn.commit()
        conn.close()
        flash("Ticket creato con successo.", "success")
        return redirect(url_for('index'))
    return render_template("ticket_form.html", form=form)

@tickets_bp.route('/modifica/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def modifica_ticket(ticket_id):
    conn = db.get_db_connection()
    ticket = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    if not ticket:
        conn.close()
        flash("Ticket non trovato.", "danger")
        return redirect(url_for('index'))

    if ticket['user_id'] != session['user_id']:
        conn.close()
        flash("Non sei autorizzato a modificare questo ticket.", "danger")
        return redirect(url_for('index'))

    form = TicketEditForm()
    if request.method == 'GET':
        form.title.data = ticket['title']
        form.description.data = ticket['description']
        form.department.data = ticket['department']
        form.status.data = ticket['status']

    if form.validate_on_submit():
        new_title = form.title.data
        new_description = form.description.data
        new_department = form.department.data
        new_status = form.status.data
        modified_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        modified_by = session['user_id']

        # Inserisci nello storico la versione precedente
        conn.execute("""
            INSERT INTO ticket_history (ticket_id, title, description, department, status, modified_at, modified_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (ticket_id, ticket['title'], ticket['description'], ticket['department'], ticket['status'], modified_at, modified_by))

        # Aggiorna il ticket
        conn.execute("""
            UPDATE tickets
            SET title = ?, description = ?, department = ?, status = ?
            WHERE id = ?
        """, (new_title, new_description, new_department, new_status, ticket_id))
        conn.commit()
        conn.close()
        flash("Ticket aggiornato con successo.", "success")
        return redirect(url_for('index'))

    conn.close()
    return render_template("ticket_edit.html", form=form, ticket=ticket)
