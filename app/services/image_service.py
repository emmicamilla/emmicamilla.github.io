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

def create_image(filename, image_data, staining, tissue, magnification, diagnosis, marker_purpose):
    return Image(
        filename=filename,
        data=image_data,
        staining=staining,
        tissue=tissue,
        magnification=magnification,
        diagnosis=diagnosis,
        marker_purpose=marker_purpose
    )
