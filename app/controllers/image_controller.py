from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from io import BytesIO

from app.repositories import image_repo
from app.services import image_service

image_bp = Blueprint('image_bp', __name__)

@image_bp.route('/')
def index():
    return render_template('index.html')

@image_bp.route('/search', methods=["GET", "POST"])
def search():
    filter_options = image_service.get_filter_options()

    images = []
    selected_stainings = request.form.getlist("staining")
    selected_tissues = request.form.getlist("tissue")
    selected_diagnoses = request.form.getlist("diagnosis")
    search_done = False

    if request.method == "POST":
        search_done = True
        images = image_service.search_images(selected_stainings, selected_tissues, selected_diagnoses)

    return render_template('search.html',
                           images=images,
                           search_done=search_done,
                           selected_stainings=selected_stainings,
                           selected_tissues=selected_tissues,
                           selected_diagnoses=selected_diagnoses,
                           **filter_options)

@image_bp.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        image_file = request.files["image"]
        if not image_file:
            return "No image uploaded", 400

        filename = secure_filename(image_file.filename)
        image_data = image_file.read()

        new_image = image_service.create_image(
            filename=filename,
            image_data=image_data,
            staining=request.form.get("staining"),
            tissue=request.form.get("tissue"),
            magnification=request.form.get("magnification"),
            diagnosis=request.form.get("diagnosis"),
            marker_purpose=request.form.get("marker_purpose")
        )

        image_repo.save_image(new_image)
        return f"Image uploaded successfully: {filename}"

    return render_template('upload.html')

@image_bp.route('/gallery')
def gallery():
    images = image_repo.get_all_images()
    return render_template('gallery.html', images=images)

@image_bp.route('/image/<int:image_id>')
def image(image_id):
    img = image_repo.get_image_by_id(image_id)
    return send_file(BytesIO(img.data), mimetype='image/jpeg')

@image_bp.route('/update_marker_purpose/<int:image_id>', methods=["POST"])
def update_marker_purpose(image_id):
    img = image_repo.get_image_by_id(image_id)
    new_value = request.form.get('marker_purpose')

    if new_value:
        image_repo.update_marker_purpose(img, new_value)
        flash('Marker purpose updated successfully!', 'success')
    else:
        flash('Please enter a marker purpose.', 'warning')

    return redirect(url_for('image_bp.gallery'))
