<p align="center">
  <img src="assets/logo.png" alt="local-privacy-guard logo" width="160" />
</p>

# local-privacy-guard

Pure-local privacy redaction for **OpenClaw users**.

**Language / 语言**
- [English](#english)
- [中文](#中文)

---

## English

### What this is

`local-privacy-guard` is a minimal, auditable privacy-redaction skill and Python CLI built for **OpenClaw users** who want to protect sensitive text **before sending content to external models, sharing logs, exporting notes, or posting debugging output**.

In one line:

> it helps OpenClaw users redact high-confidence sensitive values locally, with zero network access and safe defaults.

### Why it exists

OpenClaw users often need to:
- paste logs into chats
- send prompts to external models
- share notes or transcripts
- export debugging material

That creates one recurring risk: **private information leaves the machine too easily**.

This project exists to reduce that risk with a narrow, auditable tool that prioritizes:

- local-only execution
- default-irreversible redaction
- no raw sensitive values in default reports
- no surrounding-context preview in default output
- no persistent side effects by default
- no third-party runtime dependencies
- code small enough to audit by hand

### Security invariants

1. Mainline execution must not perform network I/O
2. Default mode must not emit raw sensitive values
3. Default mode must not emit surrounding-context previews
4. Default mode must not create persistent side effects
5. No file writes without explicit `--output`
6. All output paths must be `resolve()`-checked before use
7. `--force` only removes the non-empty overwrite guard; it never bypasses path or symlink protections
8. No deanonymize support
9. No third-party runtime dependencies
10. UTF-8 only input policy (UTF-8 BOM accepted)

### Supported inputs

- `stdin` (preferred)
- UTF-8 / UTF-8 BOM files:
  - `.txt`
  - `.md`
  - `.json`
  - `.csv`
  - `.tsv`

Currently unsupported:
- PDF / DOCX / image / audio / video
- restore / deanonymize flows
- generic entropy scanning by default

### What it detects by default

High-confidence defaults:
- email addresses
- conservative phone numbers
- IPv4 addresses
- secret-bearing URL query parameters
- common API key formats
- conservative strong-format card-like / ID-like strings

Not enabled by default:
- generic high-entropy token detection
- semantic names / entities

### Quick start

#### Read from stdin

```bash
cat secret.txt | python3 scripts/redact.py --stdin --json
```

#### Read from file and print redacted text

```bash
python3 scripts/redact.py --input ./note.md
```

#### Write redacted text to file

```bash
python3 scripts/redact.py --input ./note.md --output ./note.redacted.md
```

#### Write JSON to file

```bash
python3 scripts/redact.py --input ./note.md --json --output ./note.redacted.json
```

### Output example

```json
{
  "success": true,
  "tool": "local-privacy-guard",
  "mode": "local-only",
  "reversible": false,
  "input_type": "text",
  "detections": [
    {
      "type": "email",
      "placeholder": "[[EMAIL:7f3a91c24e6b]]",
      "fingerprint": "7f3a91c24e6b",
      "start": 5,
      "end": 22,
      "confidence": "high"
    }
  ],
  "redacted_text": "Contact me at [[EMAIL:7f3a91c24e6b]]",
  "warnings": []
}
```

### CLI rules

- `--json` and `--stdout` are mutually exclusive
- no `--output` → write to stdout only
- `--output` without `--json` → write redacted text to file
- `--output` with `--stdout` → write redacted text to file and mirror it to stdout
- `--output` with `--json` → write JSON to file
- `--force` only allows overwrite of an existing ordinary file after all path checks pass

### Testing

```bash
python3 -m unittest discover -s tests -v
```

### GitHub Pages

- Project site: <https://harlan66.github.io/local-privacy-guard/>

### License

MIT.

---

## 中文

### 这是什么

`local-privacy-guard` 是一个为 **OpenClaw 用户**设计的、最小化且可审计的隐私脱敏 skill + Python CLI。

它的核心用途不是“做一个泛用脱敏库”，而是：

> 帮 OpenClaw 用户在把内容发给外部模型、分享日志、导出笔记或贴出调试信息之前，先在本地把高置信度敏感值替换掉。

### 为什么做它

OpenClaw 用户很常见的动作是：
- 把日志贴到对话里
- 把提示词发给外部模型
- 分享笔记、转录或排障材料
- 导出调试内容给别人看

真正的问题不复杂：**私人信息太容易离开本机**。

这个项目就是为了解决这个问题，而且只解决这个问题。它优先追求：

- 纯本地执行
- 默认不可逆脱敏
- 默认 JSON 不包含原始敏感值
- 默认不输出上下文预览
- 默认不产生持久化副产物
- 不依赖第三方运行时依赖
- 代码足够小，方便人工审计

### 安全不变量

1. 主流程不得进行网络 I/O
2. 默认模式不得输出原始敏感值
3. 默认模式不得输出原文上下文预览
4. 默认模式不得产生持久化副产物
5. 未显式指定 `--output` 时不得写文件
6. 任何输出路径都必须先 `resolve()` 再校验
7. `--force` 只解除覆盖保护，不能绕过路径与 symlink 防护
8. 不支持 deanonymize / restore
9. 不依赖第三方运行时依赖
10. 输入编码固定为 UTF-8（可接受 UTF-8 BOM）

### 支持的输入

- `stdin`（推荐）
- UTF-8 / UTF-8 BOM 文件：
  - `.txt`
  - `.md`
  - `.json`
  - `.csv`
  - `.tsv`

当前明确不支持：
- PDF / DOCX / 图片 / 音频 / 视频
- 还原 / 反脱敏流程
- 默认开启的高熵检测

### 默认检测范围

高置信度、低歧义：
- 邮箱
- 保守手机号 / 电话号
- IPv4
- URL 中的敏感 query 参数
- 常见 API key 模式
- 保守的强格式卡号 / 证件类字符串

默认不启用：
- 通用高熵 token 检测
- 语义级姓名 / 实体识别

### 快速开始

#### 从 stdin 读取

```bash
cat secret.txt | python3 scripts/redact.py --stdin --json
```

#### 从文件读取并输出脱敏文本

```bash
python3 scripts/redact.py --input ./note.md
```

#### 写出脱敏文本到文件

```bash
python3 scripts/redact.py --input ./note.md --output ./note.redacted.md
```

#### 写出 JSON 到文件

```bash
python3 scripts/redact.py --input ./note.md --json --output ./note.redacted.json
```

### CLI 规则

- `--json` 与 `--stdout` 互斥
- 不带 `--output` 时，只输出到 stdout
- `--output` 且不带 `--json` → 写脱敏文本
- `--output` 且带 `--stdout` → 写脱敏文本到文件，同时镜像输出到 stdout
- `--output` 且带 `--json` → 写 JSON
- `--force` 只允许在全部路径校验通过后覆盖普通文件

### 测试

```bash
python3 -m unittest discover -s tests -v
```

### GitHub Pages

- 项目页面：<https://harlan66.github.io/local-privacy-guard/>

### 许可证

MIT。

#huanyuan
