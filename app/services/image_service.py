from werkzeug.utils import secure_filename
from io import BytesIO

from app.repositories import image_repo
from app.models.image import Image

def get_filter_options():
    """Return distinct staining, tissue, and diagnosis values from the Image table."""
    return {
        'stainings': image_repo.get_distinct_values(Image.staining),
        'tissues': image_repo.get_distinct_values(Image.tissue),
        'diagnoses': image_repo.get_distinct_values(Image.diagnosis)
    }

def search_images(stainings, tissues, diagnoses):
    """Return filtered image results."""
    return image_repo.filter_images(stainings, tissues, diagnoses)

def upload_image(file, form_data):
    if not file or not file.filename:
        return False, "No image uploaded."

    filename = secure_filename(file.filename)
    image_data = file.read()

    try:
        new_image = Image.from_upload(filename, image_data, form_data)
    except ValueError as e:
        return False, str(e)

    image_repo.save_image(new_image)
    return True, f"Image {filename} uploaded successfully."


def get_all_images():
    """Retrieve all images from the database."""
    return image_repo.get_all_images()

def get_image_data_by_id(image_id):
    """Return image binary data by ID."""
    image = image_repo.get_image_by_id(image_id)
    return image.data

def update_marker_purpose(image_id, new_value):
    """Update the marker purpose of an image."""
    if not new_value:
        return False, "Please enter a marker purpose."

    image = image_repo.get_image_by_id(image_id)
    image.marker_purpose = new_value
    image_repo.save_image(image)
    return True, "Marker purpose updated successfully!"
