# 追劇推薦系統路由設計文件 (Routes Design)

本文件定義了「追劇推薦系統」的所有 Flask 路由、HTTP 方法、對應模板與處理邏輯。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁 (推薦榜單)** | GET | `/` | `templates/index.html` | 顯示 Top 10 熱門劇集與最新推薦。 |
| **搜尋與篩選** | GET | `/search` | `templates/search.html` | 根據關鍵字、演員或類型篩選劇集。 |
| **劇集詳情** | GET | `/drama/<int:id>` | `templates/detail.html` | 顯示單部劇集的詳細資訊、演員與評分。 |
| **我的收藏清單** | GET | `/collection` | `templates/collection.html` | 顯示使用者已收藏的「想看清單」。 |
| **加入收藏** | POST | `/collection/add` | — | 接收 `drama_id`，加入資料庫後重導向至收藏頁面。 |
| **移除收藏** | POST | `/collection/remove` | — | 接收 `drama_id`，從收藏清單中移除。 |

---

## 2. 每個路由的詳細說明

### 1. 首頁 (index)
- **處理邏輯**: 呼叫 `Drama.get_all()` 獲取所有劇集，並依評分排序取前 10 名。
- **輸出**: 渲染 `index.html`。

### 2. 搜尋與篩選 (search)
- **輸入**: 
  - `q` (query string): 關鍵字搜尋。
  - `actor` (optional): 演員名稱搜尋。
  - `category` (optional): 類型篩選。
- **處理邏輯**: 根據傳入參數呼叫 `Drama.filter_by_category()` 或自定義搜尋邏輯。
- **輸出**: 渲染 `search.html` 顯示結果。

### 3. 劇集詳情 (drama_detail)
- **輸入**: `id` (URL 參數)。
- **處理邏輯**: 呼叫 `Drama.get_by_id(id)`。
- **錯誤處理**: 若 `id` 不存在，回傳 404 頁面。
- **輸出**: 渲染 `detail.html`。

### 4. 我的收藏清單 (my_collection)
- **處理邏輯**: 呼叫 `Collection.get_all()` 獲取當前使用者的所有收藏。
- **輸出**: 渲染 `collection.html`。

### 5. 加入收藏 (add_collection)
- **輸入**: `drama_id` (Form Data)。
- **處理邏輯**: 呼叫 `Collection.add(drama_id)`。
- **輸出**: 重導向 (Redirect) 至 `/collection`。

### 6. 移除收藏 (remove_collection)
- **輸入**: `drama_id` (Form Data)。
- **處理邏輯**: 呼叫 `Collection.remove(drama_id)`。
- **輸出**: 重導向 (Redirect) 至 `/collection`。

---

## 3. Jinja2 模板清單

| 模板檔案 | 繼承對象 | 說明 |
| :--- | :--- | :--- |
| `templates/base.html` | — | 基礎佈局，包含導覽列 (Navbar) 與 Footer。 |
| `templates/index.html` | `base.html` | 呈現熱門劇集卡片牆。 |
| `templates/search.html` | `base.html` | 呈現搜尋結果。 |
| `templates/detail.html` | `base.html` | 呈現單一劇集的詳細大圖、描述與演員名單。 |
| `templates/collection.html` | `base.html` | 呈現使用者的個人收藏清單。 |

---

## 4. 路由骨架程式碼

- **Main 模組**: [app/routes/main.py](file:///c:/Users/User/Desktop/web_app_development2/app/routes/main.py)
- **Collection 模組**: [app/routes/collection.py](file:///c:/Users/User/Desktop/web_app_development2/app/routes/collection.py)
