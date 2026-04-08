#!/usr/bin/env python3
"""
修复现有页面的JS还原脚本
重新生成HTML内容，使用更新后的还原脚本
"""
import os
import sys
import sqlite3
import json

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from algorithms.html_generator import generate_protected_html

def fix_all_pages():
    db_path = os.path.join(os.path.dirname(__file__), "protected_pages.db")
    if not os.path.exists(db_path):
        print(f"数据库文件不存在: {db_path}")
        return

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 获取所有页面
    cursor.execute("SELECT id, title, encrypted_text, font_mapping, config, html_content FROM protected_pages")
    pages = cursor.fetchall()
    print(f"找到 {len(pages)} 个页面")

    updated = 0
    for page in pages:
        page_id = page['id']
        title = page['title']
        encrypted_text = page['encrypted_text']
        font_mapping_str = page['font_mapping']
        config_str = page['config']
        old_html = page['html_content']

        try:
            # 解析JSON字段
            font_mapping = json.loads(font_mapping_str) if font_mapping_str else {}
            config = json.loads(config_str) if config_str else {}
        except json.JSONDecodeError as e:
            print(f"页面 {page_id}: JSON解析失败: {e}")
            continue

        # 重新生成HTML
        try:
            new_html = generate_protected_html(
                original_text=encrypted_text,
                title=title,
                mapping=font_mapping,
                config=config,
            )
        except Exception as e:
            print(f"页面 {page_id}: 生成HTML失败: {e}")
            continue

        # 更新数据库
        cursor.execute(
            "UPDATE protected_pages SET html_content = ? WHERE id = ?",
            (new_html, page_id)
        )
        updated += 1
        print(f"页面 {page_id}: 已更新")

    conn.commit()
    conn.close()
    print(f"完成。更新了 {updated}/{len(pages)} 个页面")

if __name__ == "__main__":
    fix_all_pages()