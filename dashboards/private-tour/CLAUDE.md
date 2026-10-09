# Webuy Project - AI Collaboration Rules

> This file is automatically loaded by Claude Code, Cursor, and compatible AI tools.
> **Do not delete or modify without architecture owner approval.**

---

## 🤖 Identity & Context

You are an AI assistant working on a **Webuy** project.

Webuy Global Ltd. (NASDAQ: WBUY) is a Singapore-based travel and lifestyle group
operating multiple brands including WeTrip, Webuy Travel SG, Webuy Travel ID,
Golden Circle, Altitude, and MICE.

This project MUST comply with **Webuy Infrastructure Architecture V1.2**.

---

## 📋 Mandatory Reading

Before suggesting any infrastructure decision, you MUST have read:

1. `ARCHITECTURE.md` (in this repo or in `ai-project-template`)
2. `.ai-context/forbidden-actions.md`
3. `.ai-context/webuy-infra-map.md`
4. `.ai-context/company-resources.md` (公司账户与凭据治理 - **MUST READ**)
5. `REGISTRY/company-accounts.yaml` (公司账号清单)
6. `.ai-context/llm-model-selection.md` (LLM 分层选型策略 — **MUST READ if your project uses LLM**)
7. The PLAYBOOK matching this project's type

If you have not read these, **stop and read them first**.

---

## 🚫 Hard Rules (Never Violate)

### Rule 1: Default Deployment Targets

- Display websites → **Vercel** or **Cloudflare Pages**
- Marketing H5 → **Cloudflare Pages**
- AI jobs → **AI Job Platform** (Serverless / Worker / Queue)
- Internal tools → **Vercel + Supabase**
- Data pipelines → **Worker + Queue + Object Storage**
- Agents → **OpenClaw** ecosystem

### Rule 2: No New ECS

Do not suggest creating a new Huawei Cloud ECS, AWS EC2, or any equivalent
virtual machine without first directing the user to `PLAYBOOKS/99-when-need-ecs.md`.

### Rule 3: Secrets — Risk-Tiered Pragmatic Handling

Webuy uses **4-tier risk classification** instead of blanket bans:

- **Tier 0 Breakglass** (cloud root accounts / domain EPP codes / bank / NASDAQ IR): AI never handles. Kept **offline** (sealed envelope / encrypted USB), Boss Bin + IT lead only. Never in any SaaS.
- **Tier 1 Production active** (prod API keys, prod DB, prod admin tokens): Configure once into Vercel / Cloudflare / Supabase UI. Don't commit to git, don't echo back unsolicited in chat. AI may help configure but doesn't repeat values.
- **Tier 2 Dev / Test / Sandbox** (test01, dev keys, sandbox API, admin shared tokens — **99% of daily work**): OK to use in local `.env.local` (gitignored) AND OK to share with AI in chat for debugging. Only hard rule: don't commit to git.
- **Tier 3 Public / Demo** (`NEXT_PUBLIC_*`, demo tokens, localhost defaults): No restriction.

**Universal hard rules (regardless of tier)**:
- Never write any secret into code or `.env` committed to git
- Never echo Tier 0/1 secrets in AI responses unprompted
- If user pastes a Tier 0/1 secret in chat, remind them once to rotate it after the task — don't refuse to continue helping

The goal: **enable AI debugging on Tier 2/3 (99% case) while keeping Tier 0/1 strict**.

### Rule 4: Data Region Separation

- SG production data must stay in SG region
- ID production data must stay in ID region
- Do not suggest combining SG/ID databases without compliance review

### Rule 5: PII Handling

If the project touches PII (personally identifiable information):
- Default to data minimization (only collect what's needed)
- Mask / anonymize before sending to AI APIs when possible
- Never log raw PII to console / Sentry / analytics
- Use Supabase Row Level Security (RLS) for any user data

### Rule 7: Company Accounts Are Mandatory

For any SaaS / cloud resource listed in `REGISTRY/company-accounts.yaml`:

- **Never** suggest the user sign up a new personal / company-not-listed account.
- **Always** point user to `COMPLIANCE/access-request.md` to request credentials through the existing company account.
- Credentials live in the platform they run on (Vercel UI / Cloudflare UI / Supabase Vault / GitHub Secrets); person-to-person transfer uses one-time burn-after-read links (see `COMPLIANCE/secrets-workflow.md`) — **never** in `.env` committed to git, **never** plaintext in IM, **never** in AI chat.

If the user pastes a secret in chat, refuse and ask them to rotate immediately.

### Rule 8: Resource Naming Conventions

When the user requests new resources under company accounts (R2 bucket / Supabase project / Vercel project / Worker / etc.), enforce naming from `.ai-context/company-resources.md`:

- R2 bucket: `webuy-<project>-<purpose>`
- Worker: `webuy-<project>-<env>`
- Supabase project: `webuy-<project>-<env>`
- Vercel project: `<project>-<part>`

Prefer existing **shared buckets** for cross-project data (recordings / transcripts / content assets) — don't create per-project buckets when one shared bucket suffices.

### Rule 6: Cost Awareness

- Any AI API integration must include usage tracking
- Any cron job / scheduled task must have a max budget configured
- Alert the user if your proposed solution might exceed USD 200/month
- Prefer batched API calls over per-request calls when possible

---

### Rule 9: LLM Model Selection — Layered Strategy

Webuy uses **layered model selection** instead of one-size-fits-all. See `.ai-context/llm-model-selection.md` for the full standard.

**Quick decision tree**:
- **Transcribing audio** → L1: Groq Whisper Large v3 Turbo (fallback OpenAI Whisper)
- **Writing to Supabase / SkyBear / CRM / production tables** → L3: OpenAI GPT-5.4 mini
- **Complex / high-value / low-frequency tasks** (PDF parse, CEO reports, complaint review, prompt+schema design) → L4: Claude Sonnet 4.6 (Opus for hardest cases)
- **Large-scale batch / staging / drafts / history backfill** → L2: Gemini 3.1 Flash-Lite (Vertex AI Singapore)
- **Coding assistants** (Z.ai CodingPlan / Cowork / Codex) → development time only, **NEVER as production LLM API**

**5 Hard Gates for any LLM output going to production DB** (none can be skipped):

1. JSON Schema validation (zod / pydantic / json-schema)
2. Field completeness check (null / missing / wrong type → fail-fast)
3. Confidence score (LLM returns confidence; below threshold → staging, not prod)
4. Fallback (main model fails or low-confidence → automatic downgrade/upgrade)
5. Audit log (every LLM call → `audit_log.skill_run_events`: model / prompt / response / confidence / fail-reason / target table)

> **Never write LLM output directly to a production table. Not even one field.**

Reference implementation: `webuytravel/webuy-data-platform` lark digest pipeline.


## 📝 Project Classification (Fill This Out)

When this project is initialized, fill in below.
AI: if these are not filled, ask the user to complete `TEMPLATES/PROJECT.md.template` first.

```yaml
project_name: private-tour-dashboard
project_type: INTERNAL_TOOL
region: SG   # 看板托管与访问;按市场(sg / id / wetrip)分别授权读取
has_pii: NO  # 只读聚合结果;函数不输出任何客户字段
production_impact: NO
owner: Jerry <jerry@webuy.global>
estimated_monthly_cost: "< USD 5(复用公司 Vercel Pro + 数据平台 Supabase)"
```

---

## ✅ Allowed Stacks for This Project Type

(AI: load the appropriate section based on `project_type` above)

### If project_type = DISPLAY

**Allowed:**
- Frontend: Next.js 14+, Astro, Vite + React
- Hosting: Vercel (priority) / Cloudflare Pages
- DB (if needed): Supabase
- Storage: Cloudflare R2 / Huawei OBS
- Analytics: Cloudflare Web Analytics / Vercel Analytics

**Forbidden:**
- Java / Spring Boot
- Self-hosted MySQL
- Direct Huawei Cloud ECS deployment
- WordPress / PHP backends
- Long-running Node.js servers (use Edge Functions instead)

### If project_type = AI_JOB

**Allowed:**
- Runtime: Vercel Cron, Supabase Edge Functions, Cloudflare Workers
- Queue: Cloudflare Queues, Upstash QStash
- Worker: Cloudflare Workers, Hono on Workers
- DB: Supabase Postgres
- AI APIs: Anthropic, OpenAI, z.ai, Gemini (always log usage)

**Forbidden:**
- Running jobs inside Travel backend Java services
- Long-running Python scripts on shared servers
- Cron jobs on Boss Bin's Mac mini (personal workstation, not company infra)

### If project_type = INTERNAL_TOOL

**Allowed:**
- Frontend: Next.js 14+ with App Router
- Backend: Next.js API Routes / Server Actions, Supabase Edge Functions
- DB: Supabase Postgres with RLS
- Auth: Supabase Auth / Google Workspace SSO / Lark SSO
- Hosting: Vercel

**Forbidden:**
- Custom auth implementations (use Supabase Auth or SSO)
- Storing passwords in DB (use Auth providers)
- Exposing internal tools to public internet without auth

### If project_type = CORE_BACKEND

**Default:**
- Project must be extending existing Travel backend, not a new one
- Stay in Huawei Cloud SG or ID region
- Java + Spring Boot is acceptable here (legacy compatibility)

**Note:** New core backend projects are rare. If you're starting a new one,
verify with architecture owner.

### If project_type = CHINA_FACING

**See `PLAYBOOKS/07-china-facing.md` for full guidance.**

Key points:
- Vercel / Cloudflare may have inconsistent China mainland access
- Consider Aliyun International or Tencent Cloud International
- ICP filing required for in-country hosting
- Separate from SG / ID production environments

---

## 🔧 Code Style & Conventions

### TypeScript / JavaScript

- Use TypeScript by default for new projects
- Strict mode enabled (`"strict": true`)
- Prefer `async/await` over `.then()`
- Use Zod for runtime validation of external inputs

### Database

- Use Supabase migrations for schema changes
- Enable Row Level Security (RLS) on all tables containing user data
- Index foreign keys
- Use UUIDs for primary keys on user-facing tables

### Git & Commits

- Conventional Commits format: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`
- One logical change per commit
- Reference issue numbers when applicable

### Environment Variables

- `.env.local` for local development (gitignored)
- `.env.example` for documenting required vars (committed, no values)
- Production secrets managed in Vercel / Cloudflare dashboard
- Never log environment variables

---

## 📊 Required Files in Every Webuy Project

Every project repo must contain:

```
project-root/
├── CLAUDE.md                  # This file
├── README.md                  # Project description
├── PROJECT.md                 # Project metadata (filled from template)
├── .env.example               # Required env vars documented
├── .gitignore                 # Includes .env, .env.local
└── package.json (or equiv)   # Dependencies
```

Optional but recommended:
```
├── .cursorrules               # Symlink or copy of CLAUDE.md for Cursor
├── .github/copilot-instructions.md  # Symlink or copy for Copilot
```

---

## 🔍 Pre-Commit Self-Check

Before any commit, AI should verify:

- [ ] No hardcoded API keys, tokens, or passwords
- [ ] No real PII in test data or seed scripts
- [ ] No `console.log` with sensitive data
- [ ] `.env` is in `.gitignore`
- [ ] PROJECT.md is up to date
- [ ] Cost estimates haven't changed materially

---

## 🚨 When in Doubt

If a user asks you to do something that:
- Violates any Hard Rule above → **Refuse and explain why**
- Falls outside your project type's allowed stacks → **Ask for confirmation**
- Could exceed cost budgets → **Warn and ask for explicit approval**
- Touches production data in a risky way → **Stop and escalate**

Escalate to: Boss Bin / AI 研发负责人 via Lark.

---

## 📞 Quick Reference

- Architecture owner: Boss Bin
- Template repo: `webuytravel/ai-project-template`
- Architecture doc: `ARCHITECTURE.md` in template
- ECS review process: `PLAYBOOKS/99-when-need-ecs.md`
- Lark group: 架构治理群

---

**Remember:**
> Webuy 的 AI 工作流不是让 AI 自由发挥,而是让 AI 严格执行已经制定好的架构原则。
> 你不需要重新发明基础设施,只需要按 PLAYBOOK 执行。
