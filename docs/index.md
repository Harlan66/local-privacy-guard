<div align="center">
  <img src="assets/logo.png" alt="local-privacy-guard logo" width="160" />
  <h1>local-privacy-guard</h1>
  <p><strong>EN</strong> Pure-local privacy redaction for text and simple text files.</p>
  <p><strong>中文</strong> 纯本地、零联网、面向文本与简单文本文件的隐私脱敏工具。</p>
</div>

---

## English

### What it does

`local-privacy-guard` replaces high-confidence sensitive values locally before you share logs, notes, or prompts with external systems.

### Security model

- zero network I/O in the main path
- default-irreversible output
- no raw sensitive matches in default JSON
- no context preview by default
- no persistence without explicit output
- no third-party runtime dependencies in v1

### Supported inputs

- stdin
- UTF-8 / UTF-8 BOM `.txt`, `.md`, `.json`, `.csv`, `.tsv`

### Current scope

- email
- conservative phone patterns
- IPv4
- URL query secrets
- common API key patterns
- conservative strong-format IDs / card-like strings

### Repository

- GitHub: <https://github.com/Harlan66/local-privacy-guard>

---

## 中文

### 能做什么

`local-privacy-guard` 用来在你把日志、笔记、提示词发给外部系统之前，先在本地替换掉高置信度敏感值。

### 安全模型

- 主流程零网络 I/O
- 默认不可逆
- 默认 JSON 不包含原始敏感值
- 默认不输出上下文预览
- 不显式指定输出就不写文件
- v1 不依赖第三方运行时依赖

### 支持输入

- stdin
- UTF-8 / UTF-8 BOM 的 `.txt`、`.md`、`.json`、`.csv`、`.tsv`

### 当前范围

- 邮箱
- 保守手机号规则
- IPv4
- URL 敏感参数
- 常见 API key 模式
- 保守强格式证件 / 卡号类字符串

### 仓库

- GitHub：<https://github.com/Harlan66/local-privacy-guard>

## Status

v0.1.1 — bilingual README + generated logo.

#huanyuan
