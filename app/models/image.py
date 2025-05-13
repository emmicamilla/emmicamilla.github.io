from app import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    staining = db.Column(db.String(120), nullable=False)
    tissue = db.Column(db.String(120), nullable=False)
    magnification = db.Column(db.String(120), nullable=False)
    diagnosis = db.Column(db.String(120))
    marker_purpose = db.Column(db.Text, nullable=True)
