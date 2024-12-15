from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from .company_details import CompanyDetails

# Initialize SQLAlchemy (to be used in the main app)
db = SQLAlchemy()

# Define the CompanyDetailsModel
class CompanyDetailsModel(db.Model):
    __tablename__ = 'company_details'

    id = db.Column(db.Integer, primary_key=True)
    entity_name = db.Column(db.String, nullable=False)
    corporation_type = db.Column(db.String, nullable=True)
    filing_information = db.Column(JSONB, nullable=True)
    principal_address = db.Column(db.String, nullable=True)
    mailing_address = db.Column(db.String, nullable=True)
    registered_agent = db.Column(JSONB, nullable=True)
    officers_directors = db.Column(JSONB, nullable=True)

    def to_obj(self):
        obj = CompanyDetails()
        obj.entity_name = self.entity_name
        obj.corporation_type = self.corporation_type
        obj.filing_information = self.filing_information
        obj.principal_address = self.principal_address
        obj.mailing_address = self.mailing_address
        obj.registered_agent = self.registered_agent
        obj.officers_directors = self.officers_directors
        return obj

    @staticmethod
    def from_obj(obj):
        return CompanyDetailsModel(
            entity_name=obj.entity_name,
            corporation_type=obj.corporation_type,
            filing_information=obj.filing_information,
            principal_address=obj.principal_address,
            mailing_address=obj.mailing_address,
            registered_agent=obj.registered_agent,
            officers_directors=obj.officers_directors,
        )

# Helper functions to interact with the database
def save_company_details(details_obj):
    details_model = CompanyDetailsModel.from_obj(details_obj)
    db.session.add(details_model)
    db.session.commit()

def get_company_details_by_id(company_id):
    details_model = CompanyDetailsModel.query.get(company_id)
    return details_model.to_obj() if details_model else None

def get_company_details_by_entity_name(entity_name):
    details_model = CompanyDetailsModel.query.filter(
        CompanyDetailsModel.entity_name.ilike(f"%{entity_name}%")
    ).first()
    return details_model.to_obj() if details_model else None



def get_all_company_details():
    all_details = CompanyDetailsModel.query.all()
    return [details.to_obj() for details in all_details]

def delete_company_details_by_id(company_id):
    details_model = CompanyDetailsModel.query.get(company_id)
    if details_model:
        db.session.delete(details_model)
        db.session.commit()

# Function to initialize the database with the Flask app
def init_db(app):
    """
    Initialize the database with the Flask app.
    """
    db.init_app(app)
