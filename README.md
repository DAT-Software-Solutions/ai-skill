# ai-skill

Bộ sưu tập **skills** và **subagents** dùng nội bộ tại **[DAT Software Solutions](https://github.com/DAT-Software-Solutions)** cho [Claude Code](https://docs.claude.com/en/docs/claude-code) — cũng cài được vào **Cursor** qua `AGENTS.md`.

Một URL. Chọn AI tool, chọn scope, chọn item cần cài. Không có gì tự động — bạn chọn gì thì cài cái đó.

```bash
curl -fsSL https://raw.githubusercontent.com/DAT-Software-Solutions/ai-skill/main/install.sh | bash
```

Bạn sẽ thấy 3 prompt tương tác:

```
1) Pick AI tool         →  Claude Code  /  Cursor
2) Pick scope            →  user (~/.claude/)  /  project ($PWD/.claude/)   ← Claude only
3) Pick item(s)          →  multi-select: Space toggles, Enter confirms
```

---

## Nội dung repo

### Skills (`skills/<name>/`)

Workflow recipes — auto-trigger khi prompt match, ép output theo cấu trúc cố định.

| Skill | Mô tả |
|---|---|
| [`architecture-doc-writer`](skills/architecture-doc-writer/) | Viết HLD backend, migration plan, component deep-dives — Mermaid, state machines, queue topology, SQL schema, phased rollout, risk register, SLO. Trigger trên *"viết tài liệu kiến trúc"*, *"architecture doc"*, *"HLD"*, *"migration plan"*, *"RFC"*. |

### Subagents (`agents/<name>.md`)

Specialist persona, có context window riêng. Gọi qua tool `Task` hoặc Claude tự kích hoạt.

| Agent | Mô tả |
|---|---|
| [`seo-expert`](agents/seo-expert.md) | Technical SEO cho **Next.js App Router** — metadata API, JSON-LD, sitemaps, robots, canonical/hreflang, image SEO, Core Web Vitals, i18n. Audit page mới và PR. Model: `sonnet`. |

> Sẽ có thêm item mới trong tương lai mà không phá install cũ. Installer chỉ động vào những gì bạn chọn.

---

## Cài đặt — interactive (1 URL)

```bash
curl -fsSL https://raw.githubusercontent.com/DAT-Software-Solutions/ai-skill/main/install.sh | bash
```

Picker đọc từ `/dev/tty` nên chạy ngon dưới `curl | bash`.

### Bước 1 — Chọn AI tool

```
Pick AI tool (↑/↓ + Enter, q to cancel):
> Claude Code   →  .claude/skills + .claude/agents
  Cursor        →  AGENTS.md at project root
```

### Bước 2 — (Claude only) Chọn scope

```
Install destination:
  user    → ~/.claude/{skills,agents}
  project → $PWD/.claude/{skills,agents}

Pick scope (↑/↓ + Enter, q to cancel):
> user      (global — dùng được trong mọi project)
  project   (chỉ trong thư mục hiện tại)
```

Cursor luôn ghi vào `$PWD/AGENTS.md` (override bằng `CURSOR_AGENTS_FILE=...`).

### Bước 3 — Chọn item (multi-select)

```
Pick item(s) (↑/↓ move, Space toggle, a all, Enter confirm, q cancel):
> [x] architecture-doc-writer  (skill)
  [x] seo-expert               (agent)
```

`Space` toggle, `a` chọn tất cả, `Enter` confirm. Không confirm thì không có gì xảy ra.

---

## Cài đặt — non-interactive (skip prompt)

```bash
# Claude Code, user-level, 1 agent
./install.sh --claude --user seo-expert

# Claude Code, project-level, nhiều item
./install.sh --claude --project seo-expert architecture-doc-writer

# Cursor (luôn ghi vào project root)
./install.sh --cursor seo-expert architecture-doc-writer

# Symlink thay vì copy (Claude only, tiện để live-edit)
./install.sh --claude --link --user seo-expert

# Cài hàng loạt
./install.sh --claude --user all-skills
./install.sh --claude --user all-agents

# Gỡ
./install.sh --uninstall --claude --user seo-expert
./install.sh --uninstall --cursor seo-expert    # xoá section khỏi AGENTS.md
```

> `all` đơn lẻ **không hỗ trợ** — phải dùng `all-skills` hoặc `all-agents`.

### Env overrides

```bash
CLAUDE_SKILLS_DIR=/path     # override Claude skills destination
CLAUDE_AGENTS_DIR=/path     # override Claude agents destination
CURSOR_AGENTS_FILE=/path    # override Cursor AGENTS.md path
```

---

## Mỗi target lưu item như thế nào

### Claude Code

| Item | Destination (user scope) |
|---|---|
| Skill | `~/.claude/skills/<name>/` (full directory) |
| Agent | `~/.claude/agents/<name>.md` (single file) |

Đổi `~/.claude/` thành `$PWD/.claude/` cho project scope.

### Cursor

Tất cả vào 1 file `AGENTS.md` ở project root. Mỗi item là 1 section ngăn bởi marker comment:

```markdown
<!-- ai-skill:start seo-expert -->
## Agent: seo-expert

(full agent prompt)
<!-- ai-skill:end seo-expert -->
```

- **Skills** được flatten: `## Skill: <name>` + body `SKILL.md`, kèm sub-section `### References` và `### Assets` chứa từng file inline.
- **Agents** strip YAML frontmatter, gắn dưới `## Agent: <name>`.
- Cài lại cùng 1 item sẽ replace block tại chỗ — **idempotent**, edit ngoài marker được giữ nguyên.

---

## Cài tay (nếu không muốn chạy script)

**Claude — skill:**

```bash
mkdir -p ~/.claude/skills
cp -R skills/architecture-doc-writer ~/.claude/skills/
```

**Claude — agent:**

```bash
mkdir -p ~/.claude/agents
cp agents/seo-expert.md ~/.claude/agents/
```

**Cursor:** logic flatten `AGENTS.md` không đơn giản — chạy `./install.sh --cursor <name>` thay vì viết tay.

> Sau khi cài, **restart Claude Code / Cursor** để load item mới.

---

## Verify

**Claude:**

```bash
ls ~/.claude/skills/architecture-doc-writer
ls ~/.claude/agents/seo-expert.md
```

Trong Claude Code: gõ `/architecture-doc-writer`, hoặc nói tự nhiên (*"viết tài liệu kiến trúc cho hệ thống X"*). Với agent: *"use the seo-expert agent to audit `app/blog/[slug]/page.tsx`"*.

**Cursor:**

```bash
grep '<!-- ai-skill:start' AGENTS.md
```

Cursor tự đọc `AGENTS.md` khi mở project.

---

## Update

```bash
# Chạy lại installer cho item cần update
curl -fsSL https://raw.githubusercontent.com/DAT-Software-Solutions/ai-skill/main/install.sh | bash

# Hoặc nếu đã clone:
git pull && ./install.sh --claude --user all-skills all-agents
```

> Nếu cài Claude item bằng `--link`, chỉ cần `git pull` là refresh.

---

## Uninstall

```bash
./install.sh --uninstall --claude --user seo-expert
./install.sh --uninstall --cursor seo-expert     # xoá section trong AGENTS.md
```

Hoặc tay:

```bash
rm ~/.claude/agents/seo-expert.md
rm -rf ~/.claude/skills/architecture-doc-writer
# Cursor: xoá đoạn giữa cặp marker <!-- ai-skill:start/end -->.
```

---

## Cấu trúc repo

```
.
├── README.md
├── LICENSE
├── install.sh
├── agents/
│   └── seo-expert.md              # → ~/.claude/agents/seo-expert.md  (Claude)
│                                  # → ## Agent: seo-expert trong AGENTS.md (Cursor)
└── skills/
    └── architecture-doc-writer/   # → ~/.claude/skills/architecture-doc-writer/ (Claude)
        ├── SKILL.md               # → ## Skill: architecture-doc-writer trong AGENTS.md (Cursor)
        ├── references/            # → ### References / #### <file> sub-sections
        └── assets/                # → ### Assets / #### <file> sub-sections
```

---

## Đóng góp (nội bộ DAT)

**Thêm skill:**
1. Tạo thư mục mới dưới `skills/<your-skill-name>/`.
2. `SKILL.md` với YAML frontmatter (`name`, `description`).
3. Optional: `references/` (Claude load on demand), `assets/` (template).
4. Thêm 1 dòng vào bảng **Skills** ở trên.

**Thêm subagent:**
1. File mới tại `agents/<your-agent-name>.md`.
2. Frontmatter: `name`, `description`, optional `model` (`sonnet` / `opus` / `haiku`).
3. Body = system prompt — viết rõ khi nào dùng, kiểm tra gì, convention nào.
4. Thêm 1 dòng vào bảng **Subagents** ở trên.

Tham khảo [skills docs](https://docs.claude.com/en/docs/claude-code/skills) và [subagents docs](https://docs.claude.com/en/docs/claude-code/sub-agents).

Workflow: tạo branch, push, mở PR vào `main`. Review nội bộ trước khi merge.

---

## License

MIT — xem [LICENSE](LICENSE).

© DAT Software Solutions.
