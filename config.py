import os

class Config:
    # 應用程式密鑰，用於保護 session 和表單提交
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
    
    # 資料庫的連接 URI
    # 預設使用 SQLite，本地開發環境建議使用此 URI
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///site.db")
    
    # 禁用 SQLAlchemy 的事件通知系統（可提升性能）
    SQLALCHEMY_TRACK_MODIFICATIONS = False
