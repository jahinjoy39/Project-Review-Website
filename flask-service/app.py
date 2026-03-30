import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

load_dotenv('.env')
load_dotenv('.env.example')

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER','projectuser')}:{os.getenv('MYSQL_PASSWORD','projectpass')}@"
    f"{os.getenv('MYSQL_HOST','localhost')}:{os.getenv('MYSQL_PORT','3306')}/{os.getenv('MYSQL_DB','projectreview')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'flask_feedback'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, nullable=False)
    reviewer_id = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    helpful_votes = db.Column(db.Integer, default=0)
    not_helpful_votes = db.Column(db.Integer, default=0)
    helpful_reason = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

class ReviewerCredibility(db.Model):
    __tablename__ = 'reviewer_credibility'
    reviewer_id = db.Column(db.Integer, primary_key=True)
    credibility_score = db.Column(db.Float, default=0.0)
    helpful_count = db.Column(db.Integer, default=0)
    not_helpful_count = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

@app.get('/')
def home():
    return {'service': 'feedback-search-service', 'status': 'running'}

@app.post('/feedback')
def create_feedback():
    data = request.get_json()
    feedback = Feedback(
        project_id=data['project_id'],
        reviewer_id=data['reviewer_id'],
        comment=data['comment']
    )
    db.session.add(feedback)
    db.session.commit()
    recalculate_reviewer(feedback.reviewer_id)
    return jsonify({'message': 'Feedback created', 'id': feedback.id}), 201

@app.get('/feedback/project/<int:project_id>')
def list_feedback(project_id):
    items = Feedback.query.filter_by(project_id=project_id).order_by(Feedback.created_at.desc()).all()
    return jsonify([
        {
            'id': i.id,
            'project_id': i.project_id,
            'reviewer_id': i.reviewer_id,
            'comment': i.comment,
            'helpful_votes': i.helpful_votes,
            'not_helpful_votes': i.not_helpful_votes,
            'helpful_reason': i.helpful_reason,
            'created_at': i.created_at.isoformat() if i.created_at else None,
        } for i in items
    ])

@app.post('/feedback/<int:feedback_id>/mark')
def mark_feedback(feedback_id):
    data = request.get_json()
    feedback = Feedback.query.get_or_404(feedback_id)
    helpful = bool(data.get('helpful', True))
    reason = data.get('reason')
    if helpful:
        feedback.helpful_votes += 1
        if reason:
            feedback.helpful_reason = reason
    else:
        feedback.not_helpful_votes += 1
    db.session.commit()
    recalculate_reviewer(feedback.reviewer_id)
    return jsonify({'message': 'Feedback updated'})

@app.get('/leaderboard/top-reviewers')
def top_reviewers():
    rows = ReviewerCredibility.query.order_by(ReviewerCredibility.credibility_score.desc()).limit(10).all()
    return jsonify([
        {
            'reviewer_id': r.reviewer_id,
            'credibility_score': round(r.credibility_score, 2),
            'helpful_count': r.helpful_count,
            'not_helpful_count': r.not_helpful_count,
        } for r in rows
    ])

@app.get('/search')
def search_feedback():
    q = request.args.get('q', '')
    items = Feedback.query.filter(Feedback.comment.ilike(f'%{q}%')).all()
    return jsonify([
        {'id': i.id, 'project_id': i.project_id, 'reviewer_id': i.reviewer_id, 'comment': i.comment}
        for i in items
    ])


def recalculate_reviewer(reviewer_id: int):
    rows = Feedback.query.filter_by(reviewer_id=reviewer_id).all()
    helpful = sum(r.helpful_votes for r in rows)
    not_helpful = sum(r.not_helpful_votes for r in rows)
    total = helpful + not_helpful
    score = helpful / total if total else 0.0
    cred = ReviewerCredibility.query.filter_by(reviewer_id=reviewer_id).first()
    if not cred:
        cred = ReviewerCredibility(reviewer_id=reviewer_id)
        db.session.add(cred)
    cred.helpful_count = helpful
    cred.not_helpful_count = not_helpful
    cred.credibility_score = score * 100
    db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
