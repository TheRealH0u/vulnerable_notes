from flask import Blueprint, render_template, request, session, redirect, url_for, flash, make_response, jsonify
from application.models import db, Users, LoginForm, RegistrationForm, Note, NoteForm, SettingsForm
from application.util import authenticated, createJWT, isAdmin, getUsername
from werkzeug.security import check_password_hash, generate_password_hash

web = Blueprint('web', __name__)

@web.route('/')
@authenticated
def home():
    username = getUsername()
    user = Users.query.filter_by(username=username).first()
    notes = user.notes  # fetch all notes of the user
    return render_template('index.html', notes=notes)

@web.route('/logout')
def logout():
    resp = make_response(redirect(url_for('web.login')))
    resp.delete_cookie('token')
    return resp

# - - - - - - - - - - - - - - - -
# Vulnerabilities: 
# + User enumeration
# + Brute forcing
# - - - - - - - - - - - - - - - -
@web.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    token = createJWT(user.username)
                    resp = make_response(redirect(url_for('web.home')))
                    resp.set_cookie('token', token, path='/', httponly=False, secure=False)
                    return resp
                else:
                    form.password.errors.append("Password is incorrect!")
            else:
                form.username.errors.append("Username is incorrect!")

    return render_template('login.html', form=form)

# - - - - - - - - - - - - - - - -
# Vulnerabilities: 
# + User enumeration
# - - - - - - - - - - - - - - - -
@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Route-level validation
        if form.password.data != form.verify.data:
            form.password.errors.append("Passwords don't match!")
            form.verify.errors.append("Passwords don't match!")

        if not form.username.data.isalnum():
            form.username.errors.append("Username contains a non-alphanumeric character!")

        if Users.query.filter_by(email=form.email.data).first():
            form.email.errors.append("Email is already used!")

        if Users.query.filter_by(username=form.username.data).first():
            form.username.errors.append("Username is already taken!")

        # If there are no errors, create the user
        if not (form.username.errors or form.email.errors or form.password.errors or form.verify.errors):
            hash = generate_password_hash(form.password.data)
            user = Users(username=form.username.data, email=form.email.data, password=hash)
            db.session.add(user)
            db.session.commit()
            flash("Account created successfully! Please login.", "success")
            return redirect(url_for('web.login'))

    return render_template('register.html', form=form)

@web.route('/settings', methods=['GET', 'POST'])
@authenticated
def settings():
    username = getUsername()
    user = Users.query.filter_by(username=username).first()
    form = SettingsForm()

    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data)
        db.session.commit()
        flash("Password changed successfully!", "success")
        return redirect(url_for('web.settings'))

    return render_template('settings.html', user=user, form=form)


# - - - - - 
# Note api
# - - - - -
@web.route('/note', methods=['GET', 'POST'])
@authenticated
def notes():
    # List all notes / create new note
    username = getUsername()
    user = Users.query.filter_by(username=username).first()
    notes = Note.query.filter_by(user_id=user.id).all()
    form = NoteForm()
    if form.validate_on_submit():
        new_note = Note(title=form.title.data, content=form.content.data, user_id=user.id)
        db.session.add(new_note)
        db.session.commit()
        flash("Note created successfully!", "success")
        return redirect(url_for('web.home'))
    return render_template('note.html', form=form, note=None)

# - - - - - - - - - - - - - - - -
# Vulnerabilities: 
# + IDOR
# + XSS
# - - - - - - - - - - - - - - - -
@web.route('/note/<int:note_id>', methods=['GET', 'POST'])
@authenticated
def note_view(note_id):
    note = Note.query.filter_by(id=note_id).first()
    if not note:
        flash("Note not found!", "danger")
        return redirect(url_for('web.home'))

    # Lock admin notes: normal users cannot see admin notes
    note_owner_username = note.user.username
    # if note_owner_username == "admin" and user.username != "admin":
    #     # pretend note doesn't exist for normal users
    #     flash("Note not found!", "danger")
    #     return redirect(url_for('web.home'))

    # At this point, the IDOR is still "active" for all non-admin notes
    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        flash("Note updated successfully!", "success")
        return redirect(url_for('web.home'))

    return render_template('note.html', note=note, form=form, note_owner_username=note_owner_username)

@web.route('/note/<int:note_id>/delete', methods=['POST'])
@authenticated
def note_delete(note_id):
    username = getUsername()
    user = Users.query.filter_by(username=username).first()
    note = Note.query.filter_by(id=note_id, user_id=user.id).first()
    if note:
        db.session.delete(note)
        db.session.commit()
        flash("Note deleted successfully!", "success")
        return redirect(url_for('web.home'))
    else:
        flash("Can't delete note! Note not found!", "danger")
        return redirect(url_for('web.home'))


