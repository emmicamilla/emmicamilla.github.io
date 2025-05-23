from flask import Blueprint, render_template, request, redirect, session, url_for, flash, send_file
from io import BytesIO

from app.services import image_service

image_bp = Blueprint('image_bp', __name__)

@image_bp.route('/')
def index():
    return render_template('index.html')


@image_bp.route('/search', methods=["GET", "POST"])
def search():
    # Fetch filter options from the database
    filters = image_service.get_filter_options()
    stainings = filters["stainings"]
    tissues = filters["tissues"]
    diagnoses = filters["diagnoses"]

    # Alusta tyhjät listat
    selected_stainings = session.get("selected_stainings", [])
    selected_tissues = session.get("selected_tissues", [])
    selected_diagnoses = session.get("selected_diagnoses", [])

    search_done = False
    images = []

    if request.method == "POST":
        # Poistotoiminnot
        if "remove_stain" in request.form:
            selected_stainings = [s for s in selected_stainings if s != request.form["remove_stain"]]
        elif "staining" in request.form:
            stain = request.form["staining"]
            if stain and stain not in selected_stainings:
                selected_stainings.append(stain)

        if "remove_tissue" in request.form:
            selected_tissues = [t for t in selected_tissues if t != request.form["remove_tissue"]]
        elif "tissue" in request.form:
            tissue = request.form["tissue"]
            if tissue and tissue not in selected_tissues:
                selected_tissues.append(tissue)

        if "remove_diagnosis" in request.form:
            selected_diagnoses = [d for d in selected_diagnoses if d != request.form["remove_diagnosis"]]
        elif "diagnosis" in request.form:
            diagnosis = request.form["diagnosis"]
            if diagnosis and diagnosis not in selected_diagnoses:
                selected_diagnoses.append(diagnosis)

        # Päivitä sessiot
        session["selected_stainings"] = selected_stainings
        session["selected_tissues"] = selected_tissues
        session["selected_diagnoses"] = selected_diagnoses

        # Tarkista, että ainakin yksi filtteri on valittu
        if not (selected_stainings or selected_tissues or selected_diagnoses):
            flash("Please select at least one filter before searching.", "warning")
        else:
            search_done = True
            images = image_service.search_images(
                selected_stainings, selected_tissues, selected_diagnoses
            )

    return render_template(
        "search.html",
        images=images,
        search_done=search_done,
        selected_stainings=selected_stainings,
        selected_tissues=selected_tissues,
        selected_diagnoses=selected_diagnoses,
        stainings=stainings,
        tissues=tissues,
        diagnoses=diagnoses
    )


@image_bp.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("image")
        form_data = request.form

        success, message = image_service.upload_image(file, form_data)
        flash(message, 'success' if success else 'danger')
        return redirect(url_for("image_bp.upload"))

    return render_template('upload.html')


@image_bp.route('/gallery')
def gallery():
    images = image_service.get_all_images()
    return render_template('gallery.html', images=images)


@image_bp.route('/image/<int:image_id>')
def image(image_id):
    try:
        image_data = image_service.get_image_data_by_id(image_id)
        return send_file(BytesIO(image_data), mimetype='image/jpeg')
    except Exception:
        flash("Image could not be retrieved.", "danger")
        return redirect(url_for("image_bp.gallery"))


@image_bp.route('/update_marker_purpose/<int:image_id>', methods=["POST"])
def update_marker_purpose(image_id):
    new_value = request.form.get("marker_purpose")
    success, message = image_service.update_marker_purpose(image_id, new_value)
    flash(message, 'success' if success else 'warning')
    return redirect(url_for('image_bp.gallery'))
