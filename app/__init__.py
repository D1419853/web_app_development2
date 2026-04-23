import os
import sqlite3
from flask import Flask
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def create_app():
    # 確保 instance 資料夾存在
    try:
        os.makedirs('instance')
    except OSError:
        pass

    # 注意：這裡的 template_folder 和 static_folder 路徑相對於此檔案
    app = Flask(__name__, instance_relative_config=True)
    
    # 設定 SECRET_KEY
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    # 註冊 Blueprints
    from app.routes.main import main_bp
    from app.routes.collection import collection_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(collection_bp)

    return app

def init_db():
    """初始化資料庫並執行 schema.sql"""
    db_path = os.path.join('instance', 'database.db')
    schema_path = os.path.join('database', 'schema.sql')
    
    # 建立 instance 目錄
    if not os.path.exists('instance'):
        os.makedirs('instance')
        
    conn = sqlite3.connect(db_path)
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("資料庫初始化成功！已匯入範例資料。")
