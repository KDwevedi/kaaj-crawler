from flask import Flask, request, jsonify
from .crawler import crawl_for_business_by_name, get_business_details
from .db import init_db, db, save_company_details, get_company_details_by_entity_name
from flask_cors import CORS

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)
    CORS(app, origins=["http://localhost:3000"])

    # Initialize the database
    init_db(app)

    with app.app_context():
        if not tables_exist():
            db.create_all()


    @app.route("/")
    def hello():
        return "Hello World"
    
    @app.route("/business/crawl")
    def crawl_for_data():
        businessName = request.args.get('business-name')
        if businessName:
            searchResults = crawl_for_business_by_name(businessName)
            # Assuming the first search result is most relevant
            companyDetails = get_business_details(searchResults[0]['link'])
            # Save Crawler Results to the db
            save_company_details(companyDetails)
            
            # Convert to dict before returning
            return jsonify(companyDetails.to_dict())
        else:
            return jsonify({"error": "Missing required query parameter 'business-name'"}), 400

    @app.route("/business/db-lookup")
    def get_business():
        businessName = request.args.get('business-name')

        company_details = get_company_details_by_entity_name(businessName)
        if company_details:
            return jsonify(company_details.to_dict())
        else:
            return jsonify({"error": f"No company found with entity name '{businessName}'"}), 404
            
    return app


def tables_exist():
    """
    Check if all tables for the application exist.
    Returns True if tables exist, otherwise False.
    """
    engine = db.get_engine()
    inspector = db.inspect(engine)
    tables = inspector.get_table_names()
    required_tables = ['company_details']
    return all(table in tables for table in required_tables)

