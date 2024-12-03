from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# 初始化資料庫
db = SQLAlchemy()

# 使用者模型
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # 主鍵
    username = db.Column(db.String(20), unique=True, nullable=False)  # 使用者名稱
    email = db.Column(db.String(120), unique=True, nullable=False)  # 使用者 Email
    password = db.Column(db.String(60), nullable=False)  # 加密後的密碼
    posts = db.relationship('Post', backref='author', lazy=True)  # 與 Post 模型建立關聯

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# 文章模型
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主鍵
    title = db.Column(db.String(100), nullable=False)  # 文章標題
    content = db.Column(db.Text, nullable=False)  # 文章內容
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 關聯到 User 表的外鍵

    def __repr__(self):
        return f"Post('{self.title}')"
