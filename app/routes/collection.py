from flask import Blueprint, request, redirect, url_for

collection_bp = Blueprint('collection', __name__)

@collection_bp.route('/collection')
def my_collection():
    """
    查看個人收藏清單
    處理邏輯：
    1. 呼叫 Collection.get_all()
    2. 渲染 collection.html 模板
    """
    pass

@collection_bp.route('/collection/add', methods=['POST'])
def add_to_collection():
    """
    加入收藏
    處理邏輯：
    1. 取得表單中的 drama_id
    2. 呼叫 Collection.add(drama_id)
    3. 重導向至 /collection
    """
    pass

@collection_bp.route('/collection/remove', methods=['POST'])
def remove_from_collection():
    """
    移除收藏
    處理邏輯：
    1. 取得表單中的 drama_id
    2. 呼叫 Collection.remove(drama_id)
    3. 重導向至 /collection
    """
    pass
