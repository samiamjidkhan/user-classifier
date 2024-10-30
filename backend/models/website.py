# models/website.py
from extensions import db
from datetime import datetime

class Website(db.Model):
    __tablename__ = 'websites'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    intent_question = db.Column(db.String(255), nullable=True)
    intent_options = db.Column(db.Text, nullable=True)  # Stored as '||' separated string
    last_analyzed = db.Column(db.DateTime, nullable=True)

    def __init__(self, url, content, intent_question=None, intent_options=None, last_analyzed=None):
        self.url = url
        self.content = content
        self.intent_question = intent_question
        self.intent_options = intent_options
        self.last_analyzed = last_analyzed
        
    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "content": self.content,
            "intent_question": self.intent_question,
            "intent_options": self.intent_options.split('||') if self.intent_options else [],
            "last_analyzed": self.last_analyzed.isoformat() if self.last_analyzed else None
        }