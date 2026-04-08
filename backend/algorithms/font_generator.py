"""
动态字体映射生成器
通过CSS @font-face + unicode-range 实现字符视觉混淆
无需 FontForge，纯 Python + CSS 方案
"""
import random
import string
import json
from typing import Optional


def generate_font_mapping(
    text: str,
    seed: Optional[int] = None,
    complexity: str = "medium",
) -> dict:
    """
    生成动态字体映射方案

    核心思路：
    1. 收集页面实际使用的字符集（子集化）
    2. 为每个字符分配一个"展示字符"（随机偏移码位）
    3. 在 HTML 中实际写入"展示字符"，通过 CSS font-family + 自定义字体映射显示正确字形
    4. 由于 CSS @font-face 的 unicode-range 方案无法在纯后端实现完整字形替换，
       本方案采用 JS 客户端动态映射：
       - 生成一个随机 charCode offset 映射表（JSON）
       - JS 在客户端将 HTML 中的"代理字符"转换为真实字符
       - HTML 源码存储的是代理字符，爬虫直接读到乱码

    :param text: 原始文本
    :param seed: 随机种子（保证同一页面可复现）
    :param complexity: 混淆复杂度 low/medium/high
    :return: 映射方案 dict
    """
    if seed is None:
        seed = random.randint(10000, 99999)

    rng = random.Random(seed)

    # 收集实际使用的可打印字符（包括中文等 Unicode 字符），排除控制字符
    unique_chars = sorted(set(c for c in text if ord(c) >= 0x20 and not (0x7F <= ord(c) <= 0x9F)))

    # 复杂度影响混淆字符范围
    complexity_map = {
        "low": 0.3,       # 30% 的字符参与混淆
        "medium": 0.6,    # 60%
        "high": 1.0,      # 100%
    }
    obfuscate_ratio = complexity_map.get(complexity, 0.6)

    # 生成字符映射：原始字符 → 代理码位（私用区 U+E000~U+F8FF）
    char_to_proxy = {}  # 原始字符 → 代理字符（用于HTML存储）
    proxy_to_char = {}  # 代理字符 → 原始字符（用于JS还原）

    pua_start = 0xE000
    pua_offset = 0

    for char in unique_chars:
        if rng.random() < obfuscate_ratio:
            proxy_codepoint = pua_start + pua_offset
            pua_offset += 1
            proxy_char = chr(proxy_codepoint)
            char_to_proxy[char] = proxy_char
            proxy_to_char[proxy_char] = char

    return {
        "seed": seed,
        "complexity": complexity,
        "char_to_proxy": char_to_proxy,
        "proxy_to_char": proxy_to_char,
        # JSON 序列化版（用于传给前端JS）
        "proxy_map_json": json.dumps(
            {hex(ord(k)): hex(ord(v)) for k, v in char_to_proxy.items()},
            ensure_ascii=False,
        ),
        "restore_map_json": json.dumps(
            {hex(ord(k)): v for k, v in proxy_to_char.items()},
            ensure_ascii=False,
        ),
    }


def apply_font_mapping(text: str, mapping: dict) -> str:
    """将原始文本中的字符替换为代理字符（用于HTML源码存储）"""
    char_to_proxy = mapping.get("char_to_proxy", {})
    result = []
    for char in text:
        result.append(char_to_proxy.get(char, char))
    return "".join(result)


def generate_restore_script(mapping: dict) -> str:
    """
    生成客户端 JS 还原脚本
    该脚本将 DOM 中的代理字符还原为真实字符，让用户看到正确内容
    爬虫若不执行 JS 则只能读到代理字符（私用区乱码）
    """
    restore_map = mapping.get("restore_map_json", "{}")

    return f"""
(function() {{
    const restoreMap = {restore_map};

    // 跳过隐藏的污染节点
    function shouldSkipNode(node) {{
        if (node.nodeType !== Node.ELEMENT_NODE) return false;
        if (node.getAttribute('aria-hidden') === 'true') return true;
        const style = node.style;
        if (style && (style.opacity === '0' || style.opacity === '0.01' ||
                     style.position === 'absolute' || style.display === 'none')) {{
            return true;
        }}
        return false;
    }}

    function restoreText(text) {{
        let changed = false;
        let result = '';
        for (let i = 0; i < text.length; i++) {{
            const hex = '0x' + text.charCodeAt(i).toString(16).toLowerCase();
            if (restoreMap[hex] !== undefined) {{
                result += restoreMap[hex];
                changed = true;
            }} else {{
                result += text[i];
            }}
        }}
        return {{changed, result}};
    }}

    function restoreNode(node) {{
        if (shouldSkipNode(node)) return;

        if (node.nodeType === Node.TEXT_NODE) {{
            const {{changed, result}} = restoreText(node.textContent);
            if (changed) node.textContent = result;
        }} else if (node.nodeType === Node.ELEMENT_NODE) {{
            // 处理 DOM 碎片化容器
            if (node.classList && node.classList.contains('dom-fragment-container')) {{
                restoreFragmentedContainer(node);
                return;
            }}

            // Handle bdo elements used for reversing text in high DOM obfuscation mode
            if (node.tagName && node.tagName.toLowerCase() === 'bdo' && node.dir === 'rtl') {{
                const textNodes = [];
                const walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT, null, false);
                let textNode;
                while(textNode = walker.nextNode()) {{
                    textNodes.push(textNode);
                }}

                textNodes.forEach(rn => {{
                    restoreNode(rn);
                    if (rn.textContent) {{
                        rn.textContent = rn.textContent.split('').reverse().join('');
                    }}
                }});

                // Remove bdo direction to not flip it twice, as we reversed the text manually
                node.removeAttribute('dir');
                return;
            }}

            // 递归处理子节点
            node.childNodes.forEach(restoreNode);
        }}
    }}

    function restoreFragmentedContainer(container) {{
        // 收集所有 .frag 元素
        const fragments = Array.from(container.querySelectorAll('.frag'));
        if (fragments.length === 0) {{
            // 如果没有 .frag 类，尝试所有子元素
            fragments.push(...container.children);
        }}

        // 按 order 属性排序
        fragments.sort((a, b) => {{
            const orderA = parseInt(a.style.order || getComputedStyle(a).order || '0');
            const orderB = parseInt(b.style.order || getComputedStyle(b).order || '0');
            return orderA - orderB;
        }});

        // 处理每个片段
        fragments.forEach(frag => {{
            if (shouldSkipNode(frag)) return;
            // 递归处理片段内的节点
            frag.childNodes.forEach(restoreNode);
        }});
    }}

    function restorePage() {{
        restoreNode(document.body);
    }}

    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', restorePage);
    }} else {{
        restorePage();
    }}
}})();
"""
