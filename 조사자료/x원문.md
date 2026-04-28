# LLM Knowledge Bases — Andrej Karpathy

> 5:42 AM · Apr 3, 2026 · 20.6M Views

---

## 원문 (English)

Something I'm finding very useful recently: using LLMs to build personal knowledge bases for various topics of research interest. In this way, a large fraction of my recent token throughput is going less into manipulating code, and more into manipulating knowledge (stored as markdown and images). The latest LLMs are quite good at it. So:

**Data ingest:** I index source documents (articles, papers, repos, datasets, images, etc.) into a `raw/` directory, then I use an LLM to incrementally "compile" a wiki, which is just a collection of `.md` files in a directory structure. The wiki includes summaries of all the data in `raw/`, backlinks, and then it categorizes data into concepts, writes articles for them, and links them all. To convert web articles into `.md` files I like to use the Obsidian Web Clipper extension, and then I also use a hotkey to download all the related images to local so that my LLM can easily reference them.

**IDE:** I use Obsidian as the IDE "frontend" where I can view the raw data, the compiled wiki, and the derived visualizations. Important to note that the LLM writes and maintains all of the data of the wiki, I rarely touch it directly. I've played with a few Obsidian plugins to render and view data in other ways (e.g. Marp for slides).

**Q&A:** Where things get interesting is that once your wiki is big enough (e.g. mine on some recent research is ~100 articles and ~400K words), you can ask your LLM agent all kinds of complex questions against the wiki, and it will go off, research the answers, etc. I thought I had to reach for fancy RAG, but the LLM has been pretty good about auto-maintaining index files and brief summaries of all the documents and it reads all the important related data fairly easily at this ~small scale.

**Output:** Instead of getting answers in text/terminal, I like to have it render markdown files for me, or slide shows (Marp format), or matplotlib images, all of which I then view again in Obsidian. You can imagine many other visual output formats depending on the query. Often, I end up "filing" the outputs back into the wiki to enhance it for further queries. So my own explorations and queries always "add up" in the knowledge base.

**Linting:** I've run some LLM "health checks" over the wiki to e.g. find inconsistent data, impute missing data (with web searchers), find interesting connections for new article candidates, etc., to incrementally clean up the wiki and enhance its overall data integrity. The LLMs are quite good at suggesting further questions to ask and look into.

**Extra tools:** I find myself developing additional tools to process the data, e.g. I vibe coded a small and naive search engine over the wiki, which I both use directly (in a web ui), but more often I want to hand it off to an LLM via CLI as a tool for larger queries.

**Further explorations:** As the repo grows, the natural desire is to also think about synthetic data generation + finetuning to have your LLM "know" the data in its weights instead of just context windows.

**TLDR:** raw data from a given number of sources is collected, then compiled by an LLM into a `.md` wiki, then operated on by various CLIs by the LLM to do Q&A and to incrementally enhance the wiki, and all of it viewable in Obsidian. You rarely ever write or edit the wiki manually, it's the domain of the LLM. I think there is room here for an incredible new product instead of a hacky collection of scripts.

---

## 한국어 번역 (요약 없음 · 전문)

# LLM 기반 지식 베이스

최근 내가 매우 유용하다고 느끼고 있는 것 중 하나는, 다양한 연구 주제에 대해 개인용 지식 베이스를 구축하는 데 LLM을 사용하는 것이다.

이 방식에서는 최근 내가 사용하는 토큰의 상당 부분이 코드 조작이 아니라, 지식 조작(마크다운과 이미지 형태로 저장된)에 쓰이고 있다. 최신 LLM들은 이 작업을 꽤 잘 해낸다.

### 데이터 수집 (Data ingest)

나는 원본 문서들(기사, 논문, 레포지토리, 데이터셋, 이미지 등)을 `raw/` 디렉토리에 인덱싱한다.

그 다음 LLM을 사용해서 점진적으로 위키를 "컴파일"한다. 이 위키는 단순히 디렉토리 구조 안에 있는 `.md` 파일들의 집합이다.

이 위키에는 다음이 포함된다:

- `raw/` 안에 있는 모든 데이터의 요약
- 백링크(backlinks)
- 개념별 카테고리화
- 개념별 아티클 작성
- 전체 문서 간 링크 연결

웹 아티클을 `.md` 파일로 변환할 때는 Obsidian Web Clipper 확장 프로그램을 사용한다.

또한 관련 이미지들을 로컬로 다운로드하는 단축키도 함께 사용한다. 이렇게 하면 LLM이 이미지까지 쉽게 참조할 수 있다.

### IDE

나는 **Obsidian**을 IDE 프론트엔드처럼 사용한다.

여기서 할 수 있는 것:

- raw 데이터 확인
- 컴파일된 위키 확인
- 파생된 시각화 결과 확인

중요한 점은, **위키의 모든 데이터는 LLM이 작성하고 유지한다**는 것이다.
나는 직접 수정하는 일이 거의 없다.

또한 몇몇 Obsidian 플러그인을 사용해서 다양한 방식으로 데이터를 렌더링해봤다.
예를 들어 슬라이드를 만들 때는 Marp를 사용한다.

### Q&A

재미있는 부분은 여기서 시작된다.

위키가 충분히 커지면 (예: 최근 연구 기준으로 약 100개 문서, 40만 단어 수준),
LLM 에이전트에게 다양한 복잡한 질문을 던질 수 있다.

그러면 LLM은:

- 관련 데이터를 찾아 읽고
- 조사하고
- 답을 구성한다

나는 원래 RAG 같은 복잡한 구조가 필요할 줄 알았는데,
이 정도 규모에서는 LLM이 다음을 스스로 꽤 잘 해낸다:

- 인덱스 파일 자동 유지
- 문서 요약 유지
- 관련 데이터 탐색 및 읽기

### 출력 (Output)

나는 단순 텍스트나 터미널 출력 대신, 다음과 같은 형식을 선호한다:

- 마크다운 파일
- 슬라이드 (Marp 형식)
- matplotlib 이미지

이 모든 결과를 다시 Obsidian에서 확인한다.

쿼리에 따라 더 다양한 시각적 출력도 가능하다.

또한 자주 하는 작업은:

→ 생성된 결과를 다시 위키에 "파일링"하는 것

이렇게 하면:

- 나의 탐색과 질문이
- 지식 베이스에 누적된다

### Linting (정합성 점검)

나는 LLM을 사용해서 위키의 "헬스 체크"도 수행한다. 예를 들면:

- 데이터 불일치 탐지
- 누락된 데이터 보완 (웹 검색 활용)
- 새로운 아티클 후보 연결 발견

이 과정을 통해 위키를 점진적으로 정제하고 데이터 품질을 높인다.

LLM은 추가로 탐색할 질문을 제안하는 데도 매우 뛰어나다.

### 추가 도구 (Extra tools)

나는 데이터 처리를 위한 추가 도구도 직접 만들고 있다.

예를 들어:

- 간단한 검색 엔진을 위키 위에 구현
- 웹 UI로 직접 사용
- 혹은 CLI를 통해 LLM에게 도구로 제공

대규모 질의에서는 이 방식이 더 유용하다.

### 추가 탐색 (Further explorations)

레포지토리가 커질수록 자연스럽게 드는 생각은 다음이다:

- 합성 데이터 생성 (synthetic data generation)
- 파인튜닝

즉, 단순히 context window로 읽는 것이 아니라
LLM이 가중치(weight) 자체에 지식을 내재화하도록 하는 방향이다.

### 요약 (TLDR)

- 여러 소스에서 raw 데이터를 수집하고
- LLM이 이를 `.md` 위키로 컴파일하고
- 다양한 CLI 도구를 통해 Q&A 및 위키 개선을 수행하며
- 모든 결과는 Obsidian에서 확인

그리고 중요한 점:

→ 위키는 거의 사람이 직접 수정하지 않는다
→ LLM이 유지 관리하는 영역이다

나는 이 방향에서
단순한 스크립트 묶음이 아니라
훨씬 더 뛰어난 새로운 제품이 나올 수 있다고 생각한다.
