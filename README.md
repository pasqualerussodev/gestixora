# Gestixora 1.0 - piattaforma di ticketing

Questa è una semplice applicazione web di ticketing sviluppata con Flask. Permette agli utenti di registrarsi, effettuare il login, creare ticket, modificarli e allegare file.

## ✨ Funzionalità

- Registrazione e login sicuri con hashing delle password
- Creazione e modifica dei ticket
- Storico delle modifiche
- Upload di allegati
- Interfaccia responsive con Bootstrap

## 🗂️ Struttura del progetto

```
ticketing_app/
│
├── app.py
├── config.py
├── db.py
├── forms.py
├── auth.py
├── tickets.py
├── requirements.txt
├── uploads/               # Cartella per gli allegati
└── templates/
    ├── index.html
    ├── login.html
    ├── register.html
    ├── ticket_form.html
    └── ticket_edit.html
```

## ⚙️ Installazione

1. Clona il repository o copia i file nel tuo ambiente.
2. Crea un ambiente virtuale:

```bash
python -m venv venv
source venv/bin/activate  # Su Windows: venv\\Scripts\\activate
```

3. Installa le dipendenze:

```bash
pip install -r requirements.txt
```

4. Avvia l'applicazione:

```bash
python app.py
```

## 📂 Upload

I file allegati vengono salvati nella cartella `uploads/`. Assicurati che esista e sia scrivibile.

## 📄 Licenza

Questo progetto è distribuito sotto licenza **GNU GPL v3**. Vedi il file `LICENSE` per i dettagli.
