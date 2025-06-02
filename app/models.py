from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
import uuid
import hashlib

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    polls = db.relationship('Poll', backref='creator', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    unique_share_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    creation_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    options = db.relationship('Option', backref='poll', lazy='dynamic', cascade='all, delete-orphan')
    vote_records = db.relationship('VoteRecord', backref='poll', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Poll {self.question}>'

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    vote_count = db.Column(db.Integer, default=0)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    vote_records = db.relationship('VoteRecord', backref='option', lazy='dynamic')
    
    def __repr__(self):
        return f'<Option {self.text}>'

class VoteRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('option.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    voter_ip_hash = db.Column(db.String(64), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('poll_id', 'user_id', name='_poll_user_uc'),
    )
    
    @staticmethod
    def hash_ip(ip_address):
        """对IP地址进行哈希处理，保护隐私"""
        return hashlib.sha256(ip_address.encode()).hexdigest()
    
    def __repr__(self):
        return f'<VoteRecord {self.id}>' 