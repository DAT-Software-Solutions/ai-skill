# Contributing to DAT AI Skills

Cảm ơn bạn quan tâm đến repo này! Đây là collection các Claude Code skills và subagents do **DAT Software Solutions** maintain. Mọi đóng góp đều được hoan nghênh, nhưng phải đi qua quy trình review dưới đây.

> **Maintainer duy nhất:** [@chuthuong2004](https://github.com/chuthuong2004). Mọi PR đều cần approval từ maintainer trước khi được merge vào `main`. Đây là quy định bắt buộc, được enforce bằng GitHub branch ruleset + CODEOWNERS.

---

## TL;DR

1. **Đừng push trực tiếp lên `main`** — sẽ bị chặn.
2. Tạo branch hoặc fork → commit → mở PR → đợi maintainer review.
3. Tên branch và commit message phải theo convention bên dưới.
4. Một PR chỉ làm **một việc** (one skill / one fix / one feature).

---

## Quy trình đóng góp

Bạn có thể chọn **một trong hai** workflow:

### Workflow A — Fork + PR (cho người ngoài org)

```bash
# 1. Fork repo trên GitHub UI → có repo của riêng bạn
# 2. Clone fork về máy
git clone https://github.com/<your-username>/ai-skill.git
cd ai-skill

# 3. Add upstream để sync về sau
git remote add upstream https://github.com/DAT-Software-Solutions/ai-skill.git

# 4. Tạo branch
git checkout -b feat/my-new-skill

# 5. Commit + push lên fork của bạn
git push origin feat/my-new-skill

# 6. Mở PR từ fork về DAT-Software-Solutions/ai-skill:main trên GitHub UI
```

### Workflow B — Branch trong repo (cho collaborator nội bộ)

Chỉ áp dụng nếu bạn đã được maintainer add làm **collaborator** với quyền write.

```bash
git clone https://github.com/DAT-Software-Solutions/ai-skill.git
cd ai-skill
git checkout -b feat/my-new-skill
# ...commit...
git push -u origin feat/my-new-skill
# Mở PR trên GitHub UI: feat/my-new-skill → main
```

> Không phải member nào trong org cũng tự động có quyền push branch. Nếu chưa có quyền, dùng Workflow A (fork).

---

## Convention

### Tên branch

| Prefix    | Dùng khi                                   | Ví dụ                          |
| --------- | ------------------------------------------ | ------------------------------ |
| `feat/`   | Thêm skill, agent, hoặc tính năng mới      | `feat/seo-keyword-analyzer`    |
| `fix/`    | Sửa bug                                    | `fix/install-script-macos`     |
| `docs/`   | Chỉ sửa docs (README, hướng dẫn…)          | `docs/update-readme-vi`        |
| `chore/`  | Maintenance, tooling, không đổi behavior   | `chore/bump-install-script`    |
| `refactor/` | Refactor không đổi behavior              | `refactor/install-multi-pick`  |

### Commit message — Conventional Commits

Format: `<type>: <mô tả ngắn ở thì hiện tại, viết thường, không dấu chấm cuối>`

```
feat: add seo-keyword-analyzer skill
fix: handle missing ~/.claude/skills dir in install.sh
docs: update Vietnamese install instructions
chore: bump install.sh version banner
```

Types được chấp nhận: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `perf`, `style`.

Nếu thay đổi breaking, thêm `!`: `feat!: rename agents/ to subagents/`.

---

## Thêm skill mới (`skills/<your-skill>/`)

Mỗi skill là một thư mục trong `skills/` với cấu trúc tối thiểu:

```
skills/your-skill-name/
├── SKILL.md           # bắt buộc — frontmatter + nội dung skill
└── (resources/...)    # optional — file phụ trợ
```

`SKILL.md` phải có frontmatter:

```yaml
---
name: your-skill-name
description: Một câu mô tả khi nào dùng skill này. Càng cụ thể càng dễ trigger.
---
```

**Checklist:**
- [ ] Tên skill là `kebab-case`, không trùng skill đã có.
- [ ] `description` mô tả rõ **khi nào** Claude nên dùng skill này (trigger conditions).
- [ ] Đã test bằng cách invoke trong Claude Code (mention skill hoặc trigger qua mô tả).
- [ ] Thêm entry vào `README.md` ở section danh sách skills (nếu có).

---

## Thêm agent mới (`agents/<your-agent>.md`)

Mỗi agent là một file `.md` trong `agents/` với frontmatter:

```yaml
---
name: your-agent-name
description: Khi nào dùng agent này. Mô tả use cases cụ thể.
tools: Read, Grep, Glob, Bash   # liệt kê tools agent được dùng
---
```

**Checklist:**
- [ ] Tên file = tên agent (kebab-case).
- [ ] `tools` chỉ liệt kê những gì agent thực sự cần (principle of least privilege).
- [ ] Đã test invoke agent trong Claude Code.

---

## Test trước khi mở PR

```bash
# 1. Đảm bảo install.sh vẫn chạy được nếu bạn động vào nó
./install.sh --help    # hoặc chạy interactive picker
shellcheck install.sh  # nếu có cài shellcheck

# 2. Nếu thêm skill: invoke nó trong Claude Code và verify nó load đúng
# 3. Nếu thêm agent: gọi Agent tool với subagent_type=<your-agent>
```

---

## Khi mở PR

1. Điền đầy đủ template PR (sẽ auto-load khi bạn mở PR).
2. PR title cũng nên theo Conventional Commits format.
3. **Một PR = một concern.** Đừng gộp 3 skill khác nhau vào một PR.
4. Maintainer sẽ được auto-request review qua CODEOWNERS. Đừng tag thêm reviewer khác.
5. Sau review, nếu maintainer request changes: push thêm commit lên cùng branch (KHÔNG force-push, không squash trước khi merge — maintainer sẽ squash khi merge).

---

## Những thứ **sẽ bị reject ngay**

- Push trực tiếp lên `main` (đã bị ruleset chặn, nhưng nhắc lại).
- Force-push lên branch đã có PR open (làm mất review history).
- Commit secrets / API keys / `.env` files.
- PR không có mô tả hoặc không điền template.
- Đổi tên / xoá skill có sẵn mà không thảo luận trước qua issue.
- Thêm dependency mới (npm, pip, …) cho `install.sh` mà không justify.

---

## Báo bug hoặc đề xuất feature

Mở **GitHub Issue** trước khi code những thay đổi lớn. Issue giúp tránh trường hợp bạn code xong rồi PR bị reject vì hướng không phù hợp.

---

## License

Khi đóng góp, bạn đồng ý code/docs của bạn được release theo cùng license của repo (xem `LICENSE`).

---

## Liên hệ

- Maintainer: [@chuthuong2004](https://github.com/chuthuong2004) — Đào Văn Thương
- Org: [DAT Software Solutions](https://github.com/DAT-Software-Solutions)
