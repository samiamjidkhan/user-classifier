from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
from flask_migrate import Migrate
from extensions import db
from models.website import Website
from services.scraper import scrape_website_content
from services.intent_analyzer import IntentAnalyzer

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Initialize intent analyzer
    intent_analyzer = IntentAnalyzer(os.getenv('GROQ_API_KEY'))

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()}), 200

    @app.route('/analyze', methods=['POST'])
    def analyze_website():
        """
        Analyze a website and generate an intent-classification question.
        
        Expected JSON payload:
        {
            "url": "https://example.com"
        }
        """
        url = request.json.get('url')
        if not url:
            return jsonify({"error": "URL is required"}), 400

        try:
            # Check if we already have analyzed this website recently
            website = Website.query.filter_by(url=url).first()
            
            if website and website.last_analyzed and \
               (datetime.utcnow() - website.last_analyzed).days < 7:
                return jsonify({
                    "url": website.url,
                    "question": website.intent_question,
                    "options": website.intent_options.split('||'),
                }), 200

            # Scrape and analyze the website
            content = scrape_website_content(url)
            question, options = intent_analyzer.generate_intent_question(content)

            # Save or update the analysis
            if not website:
                website = Website(
                    url=url,
                    content=content,
                    intent_question=question,
                    intent_options='||'.join(options),
                    last_analyzed=datetime.utcnow()
                )
                db.session.add(website)
            else:
                website.content = content
                website.intent_question = question
                website.intent_options = '||'.join(options)
                website.last_analyzed = datetime.utcnow()

            db.session.commit()

            return jsonify({
                "url": url,
                "question": question,
                "options": options,
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

    return app

def init_database(app):
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    app = create_app()
    init_database(app)
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5001)))