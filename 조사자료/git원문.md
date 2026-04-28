# LLM Wiki

> A pattern for building personal knowledge bases using LLMs.

This is an idea file, it is designed to be copy pasted to your own LLM Agent (e.g. OpenAI Codex, Claude Code, OpenCode / Pi, or etc.). Its goal is to communicate the high level idea, but your agent will build out the specifics in collaboration with you.

---

## The core idea

Most people's experience with LLMs and documents looks like RAG: you upload a collection of files, the LLM retrieves relevant chunks at query time, and generates an answer. This works, but the LLM is rediscovering knowledge from scratch on every question. There's no accumulation. Ask a subtle question that requires synthesizing five documents, and the LLM has to find and piece together the relevant fragments every time. Nothing is built up. NotebookLM, ChatGPT file uploads, and most RAG systems work this way.

The idea here is different. Instead of just retrieving from raw documents at query time, the LLM incrementally builds and maintains a persistent wiki — a structured, interlinked collection of markdown files that sits between you and the raw sources. When you add a new source, the LLM doesn't just index it for later retrieval. It reads it, extracts the key information, and integrates it into the existing wiki — updating entity pages, revising topic summaries, noting where new data contradicts old claims, strengthening or challenging the evolving synthesis. The knowledge is compiled once and then kept current, not re-derived on every query.

This is the key difference: the wiki is a persistent, compounding artifact. The cross-references are already there. The contradictions have already been flagged. The synthesis already reflects everything you've read. The wiki keeps getting richer with every source you add and every question you ask.

You never (or rarely) write the wiki yourself — the LLM writes and maintains all of it. You're in charge of sourcing, exploration, and asking the right questions. The LLM does all the grunt work — the summarizing, cross-referencing, filing, and bookkeeping that makes a knowledge base actually useful over time. In practice, I have the LLM agent open on one side and Obsidian open on the other. The LLM makes edits based on our conversation, and I browse the results in real time — following links, checking the graph view, reading the updated pages. **Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.**

This can apply to a lot of different contexts. A few examples:

- **Personal:** tracking your own goals, health, psychology, self-improvement — filing journal entries, articles, podcast notes, and building up a structured picture of yourself over time.
- **Research:** going deep on a topic over weeks or months — reading papers, articles, reports, and incrementally building a comprehensive wiki with an evolving thesis.
- **Reading a book:** filing each chapter as you go, building out pages for characters, themes, plot threads, and how they connect. By the end you have a rich companion wiki. Think of fan wikis like Tolkien Gateway — thousands of interlinked pages covering characters, places, events, languages, built by a community of volunteers over years. You could build something like that personally as you read, with the LLM doing all the cross-referencing and maintenance.
- **Business/team:** an internal wiki maintained by LLMs, fed by Slack threads, meeting transcripts, project documents, customer calls. Possibly with humans in the loop reviewing updates. The wiki stays current because the LLM does the maintenance that no one on the team wants to do.
- **Other:** competitive analysis, due diligence, trip planning, course notes, hobby deep-dives — anything where you're accumulating knowledge over time and want it organized rather than scattered.

## Architecture

There are three layers:

1. **Raw sources** — your curated collection of source documents. Articles, papers, images, data files. These are immutable — the LLM reads from them but never modifies them. This is your source of truth.

2. **The wiki** — a directory of LLM-generated markdown files. Summaries, entity pages, concept pages, comparisons, an overview, a synthesis. The LLM owns this layer entirely. It creates pages, updates them when new sources arrive, maintains cross-references, and keeps everything consistent. You read it; the LLM writes it.

3. **The schema** — a document (e.g. `CLAUDE.md` for Claude Code or `AGENTS.md` for Codex) that tells the LLM how the wiki is structured, what the conventions are, and what workflows to follow when ingesting sources, answering questions, or maintaining the wiki. This is the key configuration file — it's what makes the LLM a disciplined wiki maintainer rather than a generic chatbot. You and the LLM co-evolve this over time as you figure out what works for your domain.

## Operations

**Ingest.** You drop a new source into the raw collection and tell the LLM to process it. An example flow: the LLM reads the source, discusses key takeaways with you, writes a summary page in the wiki, updates the index, updates relevant entity and concept pages across the wiki, and appends an entry to the log. A single source might touch 10-15 wiki pages. Personally I prefer to ingest sources one at a time and stay involved — I read the summaries, check the updates, and guide the LLM on what to emphasize. But you could also batch-ingest many sources at once with less supervision. It's up to you to develop the workflow that fits your style and document it in the schema for future sessions.

**Query.** You ask questions against the wiki. The LLM searches for relevant pages, reads them, and synthesizes an answer with citations. Answers can take different forms depending on the question — a markdown page, a comparison table, a slide deck (Marp), a chart (matplotlib), a canvas. The important insight: good answers can be filed back into the wiki as new pages. A comparison you asked for, an analysis, a connection you discovered — these are valuable and shouldn't disappear into chat history. This way your explorations compound in the knowledge base just like ingested sources do.

**Lint.** Periodically, ask the LLM to health-check the wiki. Look for: contradictions between pages, stale claims that newer sources have superseded, orphan pages with no inbound links, important concepts mentioned but lacking their own page, missing cross-references, data gaps that could be filled with a web search. The LLM is good at suggesting new questions to investigate and new sources to look for. This keeps the wiki healthy as it grows.

## Indexing and logging

Two special files help the LLM (and you) navigate the wiki as it grows. They serve different purposes:

- **`index.md`** is content-oriented. It's a catalog of everything in the wiki — each page listed with a link, a one-line summary, and optionally metadata like date or source count. Organized by category (entities, concepts, sources, etc.). The LLM updates it on every ingest. When answering a query, the LLM reads the index first to find relevant pages, then drills into them. This works surprisingly well at moderate scale (~100 sources, ~hundreds of pages) and avoids the need for embedding-based RAG infrastructure.

- **`log.md`** is chronological. It's an append-only record of what happened and when — ingests, queries, lint passes. A useful tip: if each entry starts with a consistent prefix (e.g. `## [2026-04-02] ingest | Article Title`), the log becomes parseable with simple unix tools — `grep "^## \[" log.md | tail -5` gives you the last 5 entries. The log gives you a timeline of the wiki's evolution and helps the LLM understand what's been done recently.

## Optional: CLI tools

At some point you may want to build small tools that help the LLM operate on the wiki more efficiently. A search engine over the wiki pages is the most obvious one — at small scale the index file is enough, but as the wiki grows you want proper search. **qmd** is a good option: it's a local search engine for markdown files with hybrid BM25/vector search and LLM re-ranking, all on-device. It has both a CLI (so the LLM can shell out to it) and an MCP server (so the LLM can use it as a native tool). You could also build something simpler yourself — the LLM can help you vibe-code a naive search script as the need arises.

## Tips and tricks

- **Obsidian Web Clipper** is a browser extension that converts web articles to markdown. Very useful for quickly getting sources into your raw collection.
- **Download images locally.** In Obsidian Settings → Files and links, set "Attachment folder path" to a fixed directory (e.g. `raw/assets/`). Then in Settings → Hotkeys, search for "Download" to find "Download attachments for current file" and bind it to a hotkey (e.g. Ctrl+Shift+D). After clipping an article, hit the hotkey and all images get downloaded to local disk. This is optional but useful — it lets the LLM view and reference images directly instead of relying on URLs that may break. Note that LLMs can't natively read markdown with inline images in one pass — the workaround is to have the LLM read the text first, then view some or all of the referenced images separately to gain additional context. It's a bit clunky but works well enough.
- **Obsidian's graph view** is the best way to see the shape of your wiki — what's connected to what, which pages are hubs, which are orphans.
- **Marp** is a markdown-based slide deck format. Obsidian has a plugin for it. Useful for generating presentations directly from wiki content.
- **Dataview** is an Obsidian plugin that runs queries over page frontmatter. If your LLM adds YAML frontmatter to wiki pages (tags, dates, source counts), Dataview can generate dynamic tables and lists.
- **Git.** The wiki is just a git repo of markdown files. You get version history, branching, and collaboration for free.

## Why this works

The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping. Updating cross-references, keeping summaries current, noting when new data contradicts old claims, maintaining consistency across dozens of pages. Humans abandon wikis because the maintenance burden grows faster than the value. LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass. **The wiki stays maintained because the cost of maintenance is near zero.**

The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else.

The idea is related in spirit to **Vannevar Bush's Memex (1945)** — a personal, curated knowledge store with associative trails between documents. Bush's vision was closer to this than to what the web became: private, actively curated, with the connections between documents as valuable as the documents themselves. The part he couldn't solve was who does the maintenance. The LLM handles that.

## Note

This document is intentionally abstract. It describes the idea, not a specific implementation. The exact directory structure, the schema conventions, the page formats, the tooling — all of that will depend on your domain, your preferences, and your LLM of choice. Everything mentioned above is optional and modular — pick what's useful, ignore what isn't. For example: your sources might be text-only, so you don't need image handling at all. Your wiki might be small enough that the index file is all you need, no search engine required. You might not care about slide decks and just want markdown pages. You might want a completely different set of output formats. The right way to use this is to share it with your LLM agent and work together to instantiate a version that fits your needs. The document's only job is to communicate the pattern. Your LLM can figure out the rest.

---

# LLM Wiki — 한국어

LLM을 사용해 개인 지식 베이스를 구축하는 하나의 패턴이다. 이 문서는 아이디어 파일로, OpenAI Codex, Claude Code, OpenCode / Pi 같은 LLM 에이전트에 그대로 복사해 사용하는 것을 전제로 한다. 여기서의 목적은 구체적인 구현이 아니라 상위 수준의 개념을 전달하는 것이며, 실제 세부 구현은 당신과 LLM이 협업하며 점진적으로 만들어가게 된다.

## 기존 RAG 방식의 한계

대부분 사람들이 LLM과 문서를 사용하는 방식은 RAG 형태다. 여러 파일을 업로드하면 LLM이 질의 시점에 관련된 내용을 검색해 답을 생성하는 방식이다. 이 접근은 분명 작동하지만, 본질적인 한계가 있다. LLM은 매 질문마다 지식을 처음부터 다시 찾아야 하며, 그 과정에서 어떤 것도 축적되지 않는다. 예를 들어 다섯 개 이상의 문서를 종합해야 하는 복잡한 질문이 들어오면, LLM은 매번 관련 조각들을 찾아 다시 조립해야 한다. 이전에 했던 작업이 남지 않기 때문에 매번 동일한 과정을 반복하게 된다. NotebookLM이나 ChatGPT의 파일 업로드 기능, 그리고 대부분의 RAG 시스템이 이런 방식으로 동작한다.

## 핵심 아이디어

여기서 제안하는 접근은 다르다. 질의 시점에 원본 문서를 단순히 조회하는 대신, LLM이 점진적으로 하나의 지속적인 위키를 구축하고 유지하도록 한다. 이 위키는 구조화되고 서로 연결된 마크다운 파일들의 집합으로, 원본 데이터와 사용자 사이에 위치하는 중간 계층이다. 새로운 소스를 추가하면 LLM은 단순히 이를 인덱싱하는 데 그치지 않고, 내용을 읽고 핵심 정보를 추출한 뒤 기존 위키에 통합한다. 이 과정에서 엔티티 페이지를 업데이트하고, 주제 요약을 수정하며, 새로운 정보가 기존 주장과 충돌하는 경우 이를 기록하고, 전체적인 지식 구조를 강화하거나 수정한다. 즉, 지식은 매번 다시 생성되는 것이 아니라 한 번 컴파일된 뒤 지속적으로 업데이트되는 형태로 유지된다.

이것이 핵심적인 차이다. 이 위키는 일회성 결과물이 아니라 지속적으로 누적되는 산출물이다. 교차 참조는 이미 형성되어 있고, 모순은 사전에 표시되어 있으며, 전체적인 종합 내용은 지금까지 읽은 모든 자료를 반영하고 있다. 새로운 소스를 추가하고 질문을 반복할수록 위키는 점점 더 풍부해진다. 사용자는 위키를 직접 작성하지 않는다. 대신 소스를 수집하고 탐색하며 적절한 질문을 던지는 역할을 맡는다. LLM은 요약, 교차 참조, 정리, 분류, 그리고 장기적으로 지식 베이스를 유지하는 데 필요한 모든 북키핑 작업을 수행한다.

실제 사용 방식은 비교적 단순하다. 한쪽에는 LLM 에이전트를 띄워두고, 다른 한쪽에는 Obsidian을 열어둔다. LLM은 대화를 기반으로 위키를 수정하고, 사용자는 그 결과를 실시간으로 탐색한다. 링크를 따라 이동하고, 그래프 뷰를 확인하고, 업데이트된 페이지를 읽는다. 이 구조를 비유하면 **Obsidian은 IDE이고, LLM은 프로그래머이며, 위키는 코드베이스다.**

## 적용 영역

이 접근은 다양한 영역에 적용할 수 있다.

- **개인:** 목표, 건강, 심리, 자기계발 등을 추적하면서 일기나 아티클, 팟캐스트 노트를 정리해 자신에 대한 구조화된 이해를 축적할 수 있다.
- **연구:** 몇 주 혹은 몇 달 동안 특정 주제를 깊이 탐구하며 논문과 보고서를 읽고, 점진적으로 하나의 일관된 위키를 구축할 수 있다.
- **독서:** 각 장을 정리하고 등장인물, 주제, 플롯을 연결하면서 하나의 보조 위키를 만들어갈 수 있다. 이는 Tolkien Gateway 같은 팬 위키와 유사한 구조인데, 수천 개의 페이지가 서로 연결되어 캐릭터, 장소, 사건 등을 설명하는 형태다. 차이점은 이러한 작업을 사람이 아니라 LLM이 수행한다는 점이다.
- **비즈니스:** Slack 대화, 회의 기록, 프로젝트 문서, 고객 통화 등을 기반으로 LLM이 내부 위키를 유지하도록 할 수 있으며, 필요하다면 사람이 검토 과정에 참여할 수 있다.
- **기타:** 경쟁 분석, 실사, 여행 계획, 강의 노트, 취미 탐구 등 시간에 따라 지식이 축적되는 모든 영역에 적용할 수 있다.

## 아키텍처 (3-Layer)

이 시스템은 세 가지 레이어로 구성된다.

1. **Raw sources** — 기사, 논문, 이미지, 데이터 파일 등 사용자가 선별한 원본 자료들이다. 이 레이어는 변경되지 않으며 LLM은 읽기만 수행한다. 즉, 단일 진실의 원천 역할을 한다.

2. **Wiki** — LLM이 생성하고 유지하는 마크다운 파일들의 집합이다. 여기에는 요약, 엔티티 페이지, 개념 설명, 비교, 종합 등이 포함된다. LLM이 이 레이어를 전적으로 관리하며, 사용자는 이를 읽기만 한다.

3. **Schema** — 위키의 구조와 규칙, 그리고 LLM이 어떤 방식으로 소스를 처리하고 질문에 응답하며 위키를 유지해야 하는지를 정의하는 문서다. 예를 들어 Claude Code에서는 `CLAUDE.md`, Codex에서는 `AGENTS.md` 같은 파일이 이에 해당한다. 이 스키마는 LLM을 단순한 챗봇이 아니라 체계적인 위키 관리자로 만드는 핵심 요소이며, 사용자와 LLM이 함께 지속적으로 개선해 나간다.

## 운영 사이클

운영 측면에서는 세 가지 주요 작업이 있다.

- **Ingest:** 새로운 소스를 추가하고 LLM이 이를 처리하도록 하는 과정이다. LLM은 소스를 읽고 핵심 내용을 사용자와 논의한 뒤, 위키에 요약 페이지를 작성하고 인덱스를 업데이트하며 관련 페이지들을 수정하고 로그를 기록한다. 하나의 소스가 10~15개의 페이지에 영향을 줄 수도 있다.
- **Query:** 사용자가 위키를 기반으로 질문을 하면 LLM이 관련 페이지를 찾아 읽고 인용과 함께 답변을 생성하는 과정이다. 이 답변은 마크다운 문서, 비교표, 슬라이드, 차트 등 다양한 형태로 생성될 수 있으며, 중요한 점은 이러한 결과 역시 다시 위키에 저장되어 지식으로 축적된다는 것이다.
- **Lint:** 위키의 상태를 점검하는 작업이다. 페이지 간 모순, 오래된 정보, 연결되지 않은 페이지, 누락된 개념, 부족한 데이터 등을 점검하고 개선한다.

## 인덱스와 로그

위키가 커지면 탐색을 돕기 위한 구조도 필요하다. 이를 위해 `index.md`와 `log.md`라는 두 파일을 사용한다.

- **`index.md`** 는 위키의 전체 구조를 보여주는 카탈로그로, 각 페이지의 링크와 요약, 그리고 필요에 따라 메타데이터를 포함한다. LLM은 질의에 답하기 전에 이 파일을 먼저 읽고 관련 페이지를 찾는다.
- **`log.md`** 는 시간 순으로 작업 내역을 기록하는 로그로, 수집, 질의, 점검 등의 이력이 누적된다. 일정한 형식을 유지하면 간단한 명령어로도 쉽게 조회할 수 있다.

## CLI 도구

규모가 더 커지면 CLI 도구를 추가할 수도 있다. 예를 들어 마크다운 파일을 대상으로 검색을 수행하는 **qmd** 같은 로컬 검색 엔진을 사용할 수 있으며, 필요하다면 간단한 검색 스크립트를 직접 작성하는 것도 가능하다.

## 운용 팁

- **Obsidian Web Clipper** 를 사용해 웹 문서를 마크다운으로 저장
- **이미지를 로컬로 다운로드** 해 LLM이 직접 참조할 수 있도록 함
- **Obsidian 그래프 뷰** 로 위키 구조를 한눈에 파악
- **Marp** 로 위키 내용 기반 슬라이드 생성
- **Dataview** 플러그인으로 메타데이터 기반 동적 테이블 생성
- **Git** 저장소로 관리되어 버전 관리와 협업 가능

## 왜 이 접근이 효과적인가

이 접근이 효과적인 이유는 명확하다. 지식 관리에서 가장 어려운 부분은 읽거나 생각하는 것이 아니라 정리와 유지보수다. 교차 참조를 업데이트하고, 요약을 최신 상태로 유지하고, 서로 다른 페이지 간 일관성을 유지하는 작업은 시간이 갈수록 부담이 커진다. 그래서 대부분의 사람은 위키를 유지하지 못하고 포기한다. 그러나 LLM은 이런 작업을 부담 없이 수행할 수 있으며, 여러 파일을 동시에 수정하고 일관성을 유지할 수 있다. **유지 비용이 거의 0에 가까워지면서 위키는 지속적으로 유지될 수 있다.**

결국 인간의 역할은 소스를 선별하고 분석 방향을 설정하며 의미를 해석하는 것이고, LLM의 역할은 그 외의 모든 것이다.

이 개념은 **Vannevar Bush가 제안한 Memex (1945)** 와도 유사하다. 문서 간 연결을 중심으로 하는 개인 지식 시스템이라는 점에서 그렇다. 다만 당시에는 유지보수를 수행할 주체가 없었지만, 이제는 LLM이 그 역할을 담당할 수 있다.

## 마무리

마지막으로 이 문서는 의도적으로 추상적으로 작성되어 있다. 특정 구현 방법을 제시하기보다는 패턴을 설명하는 데 목적이 있다. 디렉토리 구조, 스키마, 페이지 형식, 도구 선택은 모두 사용자 환경에 따라 달라질 수 있다. 필요한 요소만 선택적으로 적용하면 된다. 이 문서를 LLM과 공유하고 함께 자신에게 맞는 형태로 구체화해 나가는 것이 올바른 사용 방식이다.
