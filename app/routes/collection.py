from flask import Blueprint, request, redirect, url_for, render_template, flash
from app.models.collection import Collection

collection_bp = Blueprint('collection', __name__)

@collection_bp.route('/collection')
def my_collection():
    """
    查看個人收藏清單
    """
    try:
        items = Collection.get_all()
        return render_template('collection.html', items=items)
    except Exception as e:
        flash(f"載入收藏清單失敗：{e}", "danger")
        return redirect(url_for('main.index'))

@collection_bp.route('/collection/add', methods=['POST'])
def add_to_collection():
    """
    加入收藏
    """
    drama_id = request.form.get('drama_id')
    if not drama_id:
        flash("無效的劇集 ID。", "warning")
        return redirect(request.referrer or url_for('main.index'))
        
    try:
        success = Collection.add(int(drama_id))
        if success:
            flash("已成功加入想看清單！", "success")
        else:
            flash("加入收藏失敗。", "danger")
    except Exception as e:
        flash(f"操作失敗：{e}", "danger")
        
    return redirect(url_for('collection.my_collection'))

@collection_bp.route('/collection/remove', methods=['POST'])
def remove_from_collection():
    """
    移除收藏
    """
    drama_id = request.form.get('drama_id')
    if not drama_id:
        flash("無效的劇集 ID。", "warning")
        return redirect(url_for('collection.my_collection'))
        
    try:
        success = Collection.remove(int(drama_id))
        if success:
            flash("已從清單中移除。", "info")
        else:
            flash("移除失敗。", "danger")
    except Exception as e:
        flash(f"操作失敗：{e}", "danger")
        
    return redirect(url_for('collection.my_collection'))
