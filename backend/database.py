"""
database.py —— SQLite 数据库操作封装
使用 Python 标准库 sqlite3，无需额外依赖
"""
import sqlite3
import json
import os
from contextlib import contextmanager
from typing import Optional, List, Dict, Any

# 数据库文件路径（与 main.py 同目录）
DB_PATH = os.path.join(os.path.dirname(__file__), "protected_pages.db")

# ──────────────────────────────────────────────
# 初始化
# ──────────────────────────────────────────────

def init_db() -> None:
    """创建数据表（幂等，已存在则跳过）"""
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS protected_pages (
                id           TEXT PRIMARY KEY,
                title        TEXT NOT NULL DEFAULT '',
                original_text  TEXT NOT NULL DEFAULT '',
                encrypted_text TEXT NOT NULL DEFAULT '',
                font_mapping   TEXT NOT NULL DEFAULT '{}',
                html_content   TEXT NOT NULL DEFAULT '',
                config         TEXT NOT NULL DEFAULT '{}',
                view_count     INTEGER NOT NULL DEFAULT 0,
                created_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

# ──────────────────────────────────────────────
# 连接上下文管理器
# ──────────────────────────────────────────────

@contextmanager
def get_conn():
    """获取数据库连接，用 with 语句自动关闭"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          # 让查询结果支持字段名索引
    conn.execute("PRAGMA journal_mode=WAL") # 提高并发性能
    try:
        yield conn
    finally:
        conn.close()

# ──────────────────────────────────────────────
# CRUD 操作
# ──────────────────────────────────────────────

def create_page(page_data: Dict[str, Any]) -> Dict[str, Any]:
    """插入一条新的保护页面记录"""
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO protected_pages
                (id, title, original_text, encrypted_text,
                 font_mapping, html_content, config)
            VALUES
                (:id, :title, :original_text, :encrypted_text,
                 :font_mapping, :html_content, :config)
        """, {
            "id":             page_data["id"],
            "title":          page_data.get("title", ""),
            "original_text":  page_data.get("original_text", ""),
            "encrypted_text": page_data.get("encrypted_text", ""),
            "font_mapping":   json.dumps(page_data.get("font_mapping", {}), ensure_ascii=False),
            "html_content":   page_data.get("html_content", ""),
            "config":         json.dumps(page_data.get("config", {}), ensure_ascii=False),
        })
        conn.commit()
    return get_page(page_data["id"])


def get_page(page_id: str) -> Optional[Dict[str, Any]]:
    """按 ID 查询单条记录，不存在返回 None"""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM protected_pages WHERE id = ?", (page_id,)
        ).fetchone()
    if row is None:
        return None
    return _row_to_dict(row)


def list_pages() -> List[Dict[str, Any]]:
    """查询所有记录（按创建时间倒序），不返回 html_content 以减少流量"""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT id, title, original_text, encrypted_text,
                   font_mapping, config, view_count, created_at
            FROM protected_pages
            ORDER BY created_at DESC
        """).fetchall()
    return [_row_to_dict(row) for row in rows]


def increment_view_count(page_id: str) -> None:
    """访问计数 +1"""
    with get_conn() as conn:
        conn.execute(
            "UPDATE protected_pages SET view_count = view_count + 1 WHERE id = ?",
            (page_id,)
        )
        conn.commit()


def delete_page(page_id: str) -> bool:
    """删除记录，返回是否实际删除了数据"""
    with get_conn() as conn:
        cursor = conn.execute(
            "DELETE FROM protected_pages WHERE id = ?", (page_id,)
        )
        conn.commit()
    return cursor.rowcount > 0


def get_page_stats(page_id: str) -> Optional[Dict[str, Any]]:
    """仅获取统计数据"""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id, title, view_count, created_at FROM protected_pages WHERE id = ?",
            (page_id,)
        ).fetchone()
    if row is None:
        return None
    return dict(row)

# ──────────────────────────────────────────────
# 辅助
# ──────────────────────────────────────────────

def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    """将 sqlite3.Row 转为普通字典，并反序列化 JSON 字段"""
    d = dict(row)
    for json_field in ("font_mapping", "config"):
        if json_field in d and isinstance(d[json_field], str):
            try:
                d[json_field] = json.loads(d[json_field])
            except (json.JSONDecodeError, TypeError):
                d[json_field] = {}
    return d
