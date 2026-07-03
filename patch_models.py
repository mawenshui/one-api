"""
替换 one-api 源码中各 adaptor 的 ModelList 为 2026-07 最新版本
使用前:已 git clone 到 $ROOT 目录
"""
import re
from pathlib import Path

# 11 个最常用 provider 的最新模型清单(截至 2026-07)
MODELS = {
    'openai': [
        # GPT-5 系列
        'gpt-5', 'gpt-5-mini', 'gpt-5-nano', 'gpt-5-chat-latest',
        'gpt-5.1', 'gpt-5.2', 'gpt-5.4', 'gpt-5.5',
        # GPT-4.1
        'gpt-4.1', 'gpt-4.1-mini', 'gpt-4.1-nano',
        'gpt-4.1-2025-04-14',
        # GPT-4o
        'gpt-4o', 'gpt-4o-mini',
        'gpt-4o-2024-08-06', 'gpt-4o-2024-11-20',
        'chatgpt-4o-latest',
        # o-series (reasoning)
        'o3', 'o3-mini', 'o3-pro', 'o4-mini',
        'o1', 'o1-mini', 'o1-pro',
        # 开源
        'gpt-oss-120b', 'gpt-oss-20b',
        # Embedding / 工具
        'text-embedding-3-small', 'text-embedding-3-large',
        'dall-e-3', 'whisper-1', 'tts-1', 'tts-1-hd',
    ],
    'anthropic': [
        'claude-opus-4-5-20251101',
        'claude-sonnet-4-5-20250929', 'claude-sonnet-4-6',
        'claude-haiku-4-5-20251001',
        'claude-opus-4-20250514', 'claude-sonnet-4-20250514',
        'claude-3-7-sonnet-20250219',
        'claude-3-5-sonnet-latest', 'claude-3-5-haiku-latest',
        'claude-3-5-sonnet-20241022', 'claude-3-5-sonnet-20240620',
        'claude-3-5-haiku-20241022',
    ],
    'geminiv2': [  # gemini adaptor 引用 geminiv2,所以改这里
        'gemini-2.5-pro', 'gemini-2.5-flash', 'gemini-2.5-flash-lite',
        'gemini-2.0-flash', 'gemini-2.0-flash-lite', 'gemini-2.0-pro',
        'gemini-2.0-flash-thinking-exp',
        'gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-1.5-flash-8b',
        'gemini-embedding-001', 'text-embedding-004',
    ],
    'deepseek': [
        'deepseek-chat', 'deepseek-reasoner',
        'deepseek-v4-pro', 'deepseek-v4-flash',
        'deepseek-v3.1', 'deepseek-v3.1-think',
        'deepseek-v3.2', 'deepseek-v3.2-exp', 'deepseek-v3.2-speciale',
        'deepseek-coder', 'deepseek-vl2',
    ],
    'zhipu': [
        'glm-4.6', 'glm-4.5', 'glm-4.5-air', 'glm-4.5-x',
        'glm-z1-air', 'glm-z1-airx', 'glm-z1-thinking',
        'glm-4-plus', 'glm-4-air', 'glm-4-airx', 'glm-4-long',
        'glm-4-flash', 'glm-4-flashx',
        'glm-4v-plus', 'glm-4v', 'glm-4v-flash',
        'cogview-3-plus', 'cogviewx',
        'codegeex-4', 'embedding-3',
    ],
    'alibailian': [  # 阿里百炼 / 通义千问
        'qwen3-max', 'qwen3-max-preview', 'qwen3-plus', 'qwen3-flash',
        'qwen3-coder-plus',
        'qwen-max', 'qwen-max-latest',
        'qwen-plus', 'qwen-plus-latest',
        'qwen-turbo', 'qwen-turbo-latest',
        'qwen-coder-plus', 'qwen-coder-turbo',
        'qwen-long', 'qwen-mt-plus', 'qwen-mt-turbo', 'qwq-32b-preview',
        'qwen-vl-max', 'qwen-vl-plus', 'qwen-omni-turbo',
        'text-embedding-v3', 'text-embedding-v4',
        'deepseek-r1', 'deepseek-v3', 'deepseek-v3.1', 'deepseek-v3.2',
        'kimi-k2-0711-preview', 'kimi-k2-0905-preview',
    ],
    'moonshot': [
        'kimi-k2-0711-preview', 'kimi-k2-0905-preview', 'kimi-k2-thinking',
        'kimi-latest', 'kimi-thinking-preview',
        'moonshot-v1-8k', 'moonshot-v1-32k', 'moonshot-v1-128k', 'moonshot-v1-auto',
    ],
    'xai': [
        'grok-4', 'grok-4-0709', 'grok-4-heavy',
        'grok-4-fast-reasoning', 'grok-4-fast-non-reasoning',
        'grok-3', 'grok-3-mini', 'grok-3-fast', 'grok-3-mini-fast',
        'grok-2-image-1212',
    ],
    'groq': [
        'llama-3.3-70b-versatile', 'llama-3.3-70b-specdec',
        'llama-3.1-8b-instant', 'llama-3.1-70b-versatile',
        'llama-guard-3-8b',
        'meta-llama/llama-4-maverick-17b-128e-instruct',
        'meta-llama/llama-4-scout-17b-16e-instruct',
        'mixtral-8x7b-32768',
        'whisper-large-v3', 'whisper-large-v3-turbo',
        'deepseek-r1-distill-llama-70b',
    ],
    'mistral': [
        'mistral-large-latest', 'mistral-large-2407', 'mistral-large-2-latest',
        'mistral-medium-latest', 'mistral-small-latest', 'mistral-tiny-latest',
        'codestral-latest', 'codestral-mamba-latest',
        'pixtral-large-latest', 'pixtral-12b-2409',
        'ministral-8b-latest', 'ministral-3b-latest',
    ],
    'doubao': [
        'doubao-seed-1-6-250615', 'doubao-seed-1-6-thinking-250715',
        'doubao-1-5-pro-32k-250115', 'doubao-1-5-pro-256k',
        'doubao-1-5-thinking-pro-250415',
        'doubao-lite-32k', 'doubao-lite-128k',
        'doubao-pro-32k', 'doubao-pro-256k',
        'doubao-vision-pro-32k', 'doubao-vision-lite-32k',
    ],
}


def patch_one(adaptor_dir: Path, provider: str, models: list) -> str:
    """Replace ModelList block in one constants.go. Returns status string."""
    f = adaptor_dir / 'constants.go'
    if not f.exists():
        return f'[skip] no file'
    
    content = f.read_text(encoding='utf-8')
    
    # 检查是不是引用型(不直接定义)
    if re.search(r'var\s+ModelList\s*=\s*\w+\.ModelList', content):
        return f'[skip] referenced (edit source package)'
    
    # 检查有没有 var ModelList = []string{
    if 'var ModelList = []string{' not in content:
        return f'[skip] no direct ModelList'
    
    # 找块
    start = content.index('var ModelList = []string{')
    # 找匹配的 },必须单独一行
    end_marker = '\n}'
    end = content.index(end_marker, start)
    end += len(end_marker)
    
    # 生成新块(Go 现代规范:每个元素必须带逗号,包括最后一个,便于 git diff)
    new_lines = ['var ModelList = []string{']
    for m in models:
        new_lines.append(f'\t"{m}",')
    new_lines.append('}')
    new_block = '\n'.join(new_lines)
    
    new_content = content[:start] + new_block + content[end:]
    
    # 备份
    bak = f.with_suffix('.go.bak')
    if not bak.exists():
        bak.write_text(content, encoding='utf-8')
    
    f.write_text(new_content, encoding='utf-8')
    return f'[ok] {len(models)} models'


def main():
    root = Path('relay/adaptor')
    if not root.exists():
        print(f'[X] {root} not found, run from repo root')
        return
    
    print(f'Patching {len(MODELS)} providers...\n')
    for provider, models in MODELS.items():
        status = patch_one(root / provider, provider, models)
        print(f'  {provider:20s} {status}')
    
    # gemini 是引用型,跳过
    print(f'\ngemini: skipped (references geminiv2.ModelList, edited above)')
    print(f'\n[done] backup files at *.go.bak')


if __name__ == '__main__':
    main()