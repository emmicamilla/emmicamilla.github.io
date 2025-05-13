from app.models.image import Image
from app import db

def get_all_images():
    return Image.query.all()

def get_image_by_id(image_id):
    return Image.query.get_or_404(image_id)

def get_distinct_values(column):
    return [val[0] for val in db.session.query(column).distinct().all() if val[0]]

def filter_images(stainings, tissues, diagnoses):
    query = Image.query
    if stainings:
        query = query.filter(Image.staining.in_(stainings))
    if tissues:
        query = query.filter(Image.tissue.in_(tissues))
    if diagnoses:
        query = query.filter(Image.diagnosis.in_(diagnoses))
    return query.all()

def save_image(image):
    db.session.add(image)
    db.session.commit()

def update_marker_purpose(image, new_value):
    image.marker_purpose = new_value
    db.session.commit()
