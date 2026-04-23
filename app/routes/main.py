from flask import Blueprint, render_to_string, request

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁：顯示推薦榜單
    處理邏輯：
    1. 呼叫 Drama.get_all() 獲取熱門劇集
    2. 渲染 index.html 模板
    """
    pass

@main_bp.route('/search')
def search():
    """
    搜尋頁面：根據條件篩選劇集
    處理邏輯：
    1. 取得 request.args 中的 q, actor, category
    2. 呼叫對應的 Model 方法篩選資料
    3. 渲染 search.html 模板
    """
    pass

@main_bp.route('/drama/<int:id>')
def drama_detail(id):
    """
    劇集詳情頁面
    處理邏輯：
    1. 呼叫 Drama.get_by_id(id)
    2. 若找不到則回傳 404
    3. 渲染 detail.html 模板
    """
    pass
