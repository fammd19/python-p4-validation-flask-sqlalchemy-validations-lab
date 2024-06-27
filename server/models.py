from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        author = db.session.query(Author.id).filter_by(name = name).first()
        if len(name)==0 or author is not None:
            raise ValueError("Name cannot be blank")
        return name

    @validates('phone_number')
    def validate_phone_number(self,key,phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Phone number is not 10 digits")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_name(self, key, title):
        if len(title)==0:
            raise ValueError("Title cannot be blank")
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(substring in title for substring in clickbait):
            raise ValueError("No clickbait found")
        return title

    @validates('content')
    def valiate_content(self,key,content):
        if len(content) <250:
            raise ValueError("Content is too short")
        return content
    
    @validates('summary')
    def validate_content(self,key,summary):
        if len(summary) >250:
            raise ValueError("Summary is too long")
        return summary

    @validates('category')
    def validate_cateory(self,key,category):
        if category!="Fiction" and category!="Non-Fiction":
            raise ValueError("Invalid category")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
