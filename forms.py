from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=50)])
    confirm_password = PasswordField('Conferma Password',
                                     validators=[DataRequired(), EqualTo('password', message='Le password devono coincidere')])
    submit = SubmitField('Registrati')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Accedi')

class TicketForm(FlaskForm):
    title = StringField('Titolo', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Descrizione', validators=[DataRequired()])
    department = StringField('Reparto', validators=[DataRequired()])
    attachment = FileField('Allega File')
    submit = SubmitField('Crea Ticket')

class TicketEditForm(FlaskForm):
    title = StringField('Titolo', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Descrizione', validators=[DataRequired()])
    department = StringField('Reparto', validators=[DataRequired()])
    status = SelectField('Stato', choices=[
        ('Nuovo', 'Nuovo'),
        ('In Lavorazione', 'In Lavorazione'),
        ('Chiuso', 'Chiuso')
    ], validators=[DataRequired()])
    submit = SubmitField('Aggiorna Ticket')
