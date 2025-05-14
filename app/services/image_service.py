from werkzeug.utils import secure_filename
from app.repositories import image_repo
from app.models.image import Image

def get_filter_options():
    return {
        'stainings': image_repo.get_distinct_values(Image.staining),
        'tissues': image_repo.get_distinct_values(Image.tissue),
        'diagnoses': image_repo.get_distinct_values(Image.diagnosis)
    }


def search_images(stainings, tissues, diagnoses):
    return image_repo.filter_images(stainings, tissues, diagnoses)


def upload_image(file, form_data):
    if not file or not file.filename:
        return False, "No image uploaded."

    filename = secure_filename(file.filename)
    image_data = file.read()

    new_image = Image(
        filename=filename,
        data=image_data,
        staining=form_data.get("staining"),
        tissue=form_data.get("tissue"),
        magnification=form_data.get("magnification"),
        diagnosis=form_data.get("diagnosis"),
        marker_purpose=form_data.get("marker_purpose")
    )

    image_repo.save_image(new_image)
    return True, f"Image {filename} uploaded successfully."


def get_all_images():
    return image_repo.get_all_images()


def get_image_data_by_id(image_id):
    image = image_repo.get_image_by_id(image_id)
    return image.data


def update_marker_purpose(image_id, new_value):
    if not new_value:
        return False, "Please enter a marker purpose."

    image = image_repo.get_image_by_id(image_id)
    image.marker_purpose = new_value
    image_repo.save_image(image)
    return True, "Marker purpose updated successfully!"
