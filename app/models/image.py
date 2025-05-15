from app import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    staining = db.Column(db.String(50), nullable=True)
    tissue = db.Column(db.String(50), nullable=True)
    magnification = db.Column(db.String(50), nullable=True)
    diagnosis = db.Column(db.String(100), nullable=True)
    marker_purpose = db.Column(db.String(100), nullable=True)

    @staticmethod
    def from_upload(filename, image_data, form_data):
        staining = form_data.get("staining")
        tissue = form_data.get("tissue")
        magnification = form_data.get("magnification")
        diagnosis = form_data.get("diagnosis")
        marker_purpose = form_data.get("marker_purpose")

        # Basic validation
        if not staining or not tissue or not diagnosis:
            raise ValueError("Staining, tissue, and diagnosis are required fields.")

        if magnification and not magnification.isdigit():
            raise ValueError("Magnification must be a number.")

        return Image(
            filename=filename,
            data=image_data,
            staining=staining,
            tissue=tissue,
            magnification=magnification,
            diagnosis=diagnosis,
            marker_purpose=marker_purpose
        )
