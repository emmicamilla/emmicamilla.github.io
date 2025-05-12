from flask import Flask, flash, render_template, request, send_file, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
import os
from werkzeug.utils import secure_filename
from flask_migrate import Migrate

# Määritellään Flask-sovellus ja SQLAlchemy
app = Flask(__name__)
app.secret_key = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ihc.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Luodaan db-objekti
db = SQLAlchemy(app)

# Flask-Migrate
migrate = Migrate(app, db)

# Luodaan malliluokka
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    staining = db.Column(db.String(120), nullable=False)
    tissue = db.Column(db.String(120), nullable=False)
    magnification = db.Column(db.String(120), nullable=False)
    diagnosis = db.Column(db.String(120))
    marker_purpose = db.Column(db.Text, nullable=True)

# Reitit
@app.route('/', methods=["GET"])
def index():

    return render_template('index.html')

@app.route('/search', methods=["GET", "POST"])
def search():
    #Dropdown values
    stainings = [s[0] for s in db.session.query(Image.staining).distinct().all() if s[0]]
    tissues = [t[0] for t in db.session.query(Image.tissue).distinct().all() if t[0]]
    diagnoses = [d[0] for d in db.session.query(Image.diagnosis).distinct().all() if d[0]]

    images = []
    selected_stainings = []
    selected_tissues = []
    selected_diagnoses = []
    search_done = False

    if request.method == "POST":
        search_done = True
        query = Image.query

        selected_stainings = request.form.getlist("staining")
        selected_tissues = request.form.getlist("tissue")
        selected_diagnoses = request.form.getlist("diagnosis")

        if selected_stainings:
            query = query.filter(Image.staining.in_(selected_stainings))
        if selected_tissues:
            query = query.filter(Image.tissue.in_(selected_tissues))
        if selected_diagnoses:
            query = query.filter(Image.diagnosis.in_(selected_diagnoses))

        images = query.all()

    return render_template('search.html', images=images, stainings=stainings, tissues=tissues, diagnoses=diagnoses, search_done=search_done, selected_stainings=selected_stainings, selected_tissues=selected_tissues, selected_diagnoses=selected_diagnoses)

@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        image = request.files["image"]
        staining = request.form.get("staining")
        tissue = request.form.get("tissue")
        magnification = request.form.get("magnification")
        diagnosis = request.form.get("diagnosis")
        marker_purpose = request.form.get("marker_purpose")

        if image:
            filename = secure_filename(image.filename)
            image_data = image.read()
            # Saving the image details to the database
            new_image = Image(
                filename=filename,
                data=image_data,
                staining=staining,
                tissue=tissue,
                magnification=magnification,
                diagnosis=diagnosis,
                marker_purpose=marker_purpose
            )
            db.session.add(new_image)
            db.session.commit()
            return f"Image uploaded successfully: {filename}"

        else:
            return "No image uploaded", 400
    return render_template('upload.html')

@app.route('/gallery')
def gallery():
    images = Image.query.all()
    return render_template('gallery.html', images=images)

#route for displaying images (returns the image for serverr as an object)
@app.route('/image/<int:image_id>')
def image(image_id):
    img = Image.query.get_or_404(image_id)
    return send_file(BytesIO(img.data), mimetype='image/jpeg')

#route for updating the marker purpose-field
@app.route('/update_marker_purpose/<int:image_id>', methods=["POST"])
def update_marker_purpose(image_id):
    image = Image.query.get_or_404(image_id)
    marker_purpose = request.form.get('marker_purpose')
    
    if marker_purpose:
        image.marker_purpose = marker_purpose
        db.session.commit()
        flash('Marker purpose updated successfully!', 'success')
    else:
        flash('Please enter a marker purpose.', 'warning')
    
    return redirect(url_for('gallery'))

# Määritä, että sovellus pyörii debug-tilassa
if __name__ == '__main__':
    app.run(debug=True)
