from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models.drama import Drama
from app.models.actor import Actor
from app.models.collection import Collection

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁：顯示推薦榜單
    """
    try:
        # 獲取所有劇集，Drama.get_all 預設已依評分排序
        dramas = Drama.get_all()
        # 取前 10 名作為熱門推薦
        top_dramas = dramas[:10]
        return render_template('index.html', dramas=top_dramas)
    except Exception as e:
        flash(f"載入首頁時發生錯誤：{e}", "danger")
        return render_template('index.html', dramas=[])

@main_bp.route('/search')
def search():
    """
    搜尋頁面：根據關鍵字、演員或類型篩選劇集
    """
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    try:
        if query:
            # 關鍵字搜尋
            results = Drama.search(query)
        elif category:
            # 類型篩選
            results = Drama.filter_by_category(category)
        else:
            # 若無條件則導向首頁
            return redirect(url_for('main.index'))
            
        return render_template('search.html', dramas=results, query=query or category)
    except Exception as e:
        flash(f"搜尋時發生錯誤：{e}", "danger")
        return redirect(url_for('main.index'))

@main_bp.route('/drama/<int:id>')
def drama_detail(id):
    """
    劇集詳情頁面
    """
    try:
        drama = Drama.get_by_id(id)
        if not drama:
            flash("找不到該劇集資訊。", "warning")
            return redirect(url_for('main.index'))
            
        # 獲取該劇集的演員清單 (假設我們在 Actor Model 有對應方法或直接查詢)
        # 這裡簡化處理：假設 Actor.get_dramas_by_actor 的反向邏輯
        # 實務上我們可能需要一個 Drama.get_actors(id)
        # 目前我們先獲取該劇集是否已被收藏
        is_collected = Collection.is_collected(id)
        
        return render_template('detail.html', drama=drama, is_collected=is_collected)
    except Exception as e:
        flash(f"載入詳情時發生錯誤：{e}", "danger")
        return redirect(url_for('main.index'))
