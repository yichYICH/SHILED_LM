"""
FastAPI 主程序
知识产权主动防护平台 API 服务
"""
import os
import random
import string
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

from algorithms.text_obfuscator import obfuscate_text
from algorithms.font_generator import generate_font_mapping
from algorithms.html_generator import generate_protected_html
import database

# ──────────────────────────────────────────
# 初始化
# ──────────────────────────────────────────
app = FastAPI(
    title="IP Shield - 知识产权主动防护平台",
    description="文本混淆与动态字体保护 API",
    version="1.0.0",
)

# CORS 配置（允许前端跨域）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库初始化
database.init_db()

# ──────────────────────────────────────────
# 数据模型
# ──────────────────────────────────────────


class EncryptRequest(BaseModel):
    """文本加密请求"""
    text: str = Field(..., min_length=1, max_length=10000, description="原始文本")
    title: str = Field(default="受保护页面", max_length=200, description="页面标题")
    zw_frequency: float = Field(default=0.2, ge=0.0, le=1.0, description="零宽字符注入频率")
    homoglyph_ratio: float = Field(default=0.1, ge=0.0, le=1.0, description="同形字替换比例")
    dom_intensity: str = Field(default="medium", pattern="^(low|medium|high)$", description="DOM混淆强度")


class PageListItem(BaseModel):
    """页面列表项"""
    id: str
    title: str
    view_count: int
    created_at: str


class EncryptResponse(BaseModel):
    """文本加密响应"""
    encrypted_text: str
    page_id: str
    page_url: str
    stats: dict
    original_length: int
    encrypted_length: int


class PageListResponse(BaseModel):
    """页面列表响应"""
    pages: list[PageListItem]


class PageStats(BaseModel):
    """页面统计数据"""
    page_id: str
    title: str
    view_count: int
    created_at: str


# ──────────────────────────────────────────
# 工具函数
# ──────────────────────────────────────────


def generate_page_id() -> str:
    """生成 8 位随机页面 ID"""
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=8))


# ──────────────────────────────────────────
# API 路由
# ──────────────────────────────────────────


@app.get("/")
def read_root():
    """根路由，API 状态检查"""
    return {
        "status": "active",
        "service": "IP Shield - 知识产权主动防护平台",
        "version": "1.0.0",
        "endpoints": {
            "encrypt": "POST /api/encrypt-text",
            "list_pages": "GET /api/pages",
            "view_page": "GET /page/{page_id}",
            "delete_page": "DELETE /api/pages/{page_id}",
            "page_stats": "GET /api/pages/{page_id}/stats",
        }
    }


@app.post("/api/encrypt-text", response_model=EncryptResponse)
def encrypt_text_endpoint(request: EncryptRequest):
    """
    文本加密处理
    1. 零宽字符注入
    2. 同形字替换
    3. 生成动态字体映射
    4. 创建保护页面并存储到数据库
    5. 返回加密结果与页面链接
    """
    try:
        # 生成页面 ID
        page_id = generate_page_id()

        # 文本混淆处理
        result = obfuscate_text(
            text=request.text,
            zw_frequency=request.zw_frequency,
            homoglyph_ratio=request.homoglyph_ratio,
            seed=random.randint(0, 999999),
        )

        # 生成动态字体映射
        # 获取混淆结果的最终文本
        obfuscated_str = result["encrypted_text"]

        # 生成动态字体映射
        font_mapping = generate_font_mapping(
            text=obfuscated_str,
            seed=random.randint(10000, 99999),
            complexity=request.dom_intensity,
        )

        # 生成受保护 HTML
        config = {
            "zw_frequency": request.zw_frequency,
            "homoglyph_ratio": request.homoglyph_ratio,
            "dom_intensity": request.dom_intensity,
        }
        html_content = generate_protected_html(
            original_text=obfuscated_str,
            title=request.title,
            mapping=font_mapping,
            config=config,
        )

        # 存储到数据库
        page_data = {
            "id": page_id,
            "title": request.title,
            "original_text": request.text,
            "encrypted_text": result["encrypted_text"],
            "font_mapping": font_mapping,
            "html_content": html_content,
            "config": config,
        }
        saved = database.create_page(page_data)
        if not saved:
            raise HTTPException(status_code=500, detail="页面保存失败")

        return EncryptResponse(
            encrypted_text=result["zw_injected"],  # 为前端提供不带 PUA 破坏的视觉结果
            page_id=page_id,
            page_url=f"/page/{page_id}",
            stats=result["stats"],
            original_length=result["original_length"],
            encrypted_length=result["encrypted_length"],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


@app.get("/api/pages", response_model=PageListResponse)
def list_pages_endpoint():
    """获取所有保护页面列表"""
    pages = database.list_pages()
    items = []
    for page in pages:
        items.append(PageListItem(
            id=page["id"],
            title=page["title"],
            view_count=page["view_count"],
            created_at=page["created_at"],
        ))
    return PageListResponse(pages=items)


@app.get("/page/{page_id}", response_class=HTMLResponse)
def get_protected_page(page_id: str):
    """访问受保护页面（返回HTML）"""
    page = database.get_page(page_id)
    if page is None:
        raise HTTPException(status_code=404, detail="页面不存在")

    # 增加访问计数
    database.increment_view_count(page_id)

    # 直接返回存储的HTML内容
    return HTMLResponse(
        content=page["html_content"],
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        }
    )


@app.get("/api/pages/{page_id}/stats", response_model=PageStats)
def get_page_stats_endpoint(page_id: str):
    """获取页面访问统计数据"""
    page = database.get_page(page_id)
    if page is None:
        raise HTTPException(status_code=404, detail="页面不存在")

    stats = database.get_page_stats(page_id)
    if stats is None:
        raise HTTPException(status_code=404, detail="页面不存在")

    return PageStats(
        page_id=page_id,
        title=stats.get("title", ""),
        view_count=stats.get("view_count", 0),
        created_at=stats.get("created_at", ""),
    )


@app.delete("/api/pages/{page_id}")
def delete_page_endpoint(page_id: str):
    """删除保护页面"""
    success = database.delete_page(page_id)
    if not success:
        raise HTTPException(status_code=404, detail="页面不存在")
    return {"message": "页面已删除", "page_id": page_id}


@app.get("/api/health")
def health_check():
    """健康检查端点"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


# ──────────────────────────────────────────
# 启动配置
# ──────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    print("启动 IP Shield API 服务...")
    print("访问地址: http://127.0.0.1:8000")
    print("API文档: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
