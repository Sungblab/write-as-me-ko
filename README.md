# write-as-me-ko

내 블로그와 포트폴리오 글을 Codex/Claude Code와 함께 분석해, 이후 글 작성에
쓸 글쓰기용 `AGENTS.md`와 말투 프로필을 만드는 로컬 워크플로우입니다.

[`im-not-ai`](https://github.com/epoko77-ai/im-not-ai)가 이미 나온 초안의 한국어 AI 티를 줄이는 후처리 도구에 가깝다면,
`write-as-me-ko`는 초안을 쓰기 전에 "나는 어떤 기준과 형식으로 쓰는가"를
에이전트와 함께 정리해두는 쪽에 가깝습니다.

목표는 AI detector 우회나 완벽한 문체 복제가 아닙니다. 매번 "내 스타일로",
"너무 AI처럼 쓰지 말고", "보고서 톤으로", "교수님께 보내는 말투로"를 반복하지
않게 만드는 재사용 가능한 한국어 글쓰기 환경이 핵심입니다.

## What It Does

- Codex/Claude Code가 대화형 `init` 워크플로우를 진행합니다.
- Python으로 샘플 개수, 문장 길이, 자주 보이는 표현, route별 신호를 먼저 뽑습니다.
- LLM이 실제 샘플과 Python 결과를 함께 보고 말투/판단 패턴을 보강합니다.
- 이후 글 작성에 쓸 `voice-profile.md`, Codex skill, 글쓰기용 `AGENTS.md`를 만듭니다.
- 반복해서 쓰는 글쓰기 상황을 별도 `SKILL.md`로 만들 수 있습니다.
- 원문 샘플을 export 결과에 복사하지 않고, 요약된 규칙과 프로필만 사용합니다.
- synthetic before/after 사례로 사실 보존, 장르 유지, 한국어 자연스러움, 프로필 반영을 점검합니다.

## Quickstart

이 레포는 사용자가 명령어를 외워서 직접 돌리는 도구라기보다, Codex/Claude Code와
대화하면서 글쓰기 환경을 만들어가는 워크플로우입니다.

먼저 이 레포를 Codex 또는 Claude Code에서 엽니다. 그다음 내 블로그, 포트폴리오,
보고서, 메시지, 프로젝트 문서 샘플을 `samples/` 아래에 넣거나 샘플이 있는 로컬
경로를 알려줍니다.

```text
samples/
  blog/
  report/
  message/
  project/
```

에이전트에게 이렇게 말합니다.

```text
이 레포 기준으로 내 블로그/포트폴리오 글을 분석해서 글쓰기용 AGENTS.md를 만들어줘.
Python 분석도 돌리고, 네가 샘플을 읽어서 말투 프로필도 보강해줘.
개인 원문은 git에 올리지 말고 로컬에서만 다뤄줘.
```

에이전트는 다음 흐름으로 진행합니다.

```text
samples or local writing path
  -> Python baseline analysis
  -> LLM interpretation
  -> voice-profile.md
  -> writing AGENTS.md / Codex skill
  -> npm run docs:check
```

직접 확인하거나 디버깅해야 할 때는 아래 명령을 쓸 수 있습니다.

```powershell
python -m scripts.init_writing_workspace --samples samples --repo-root .
.\scripts\install_codex.ps1 -Force
python -m scripts.export_agent_context --output dist\writing\AGENTS.md
```

이후 글을 쓸 때는 생성된 글쓰기용 `AGENTS.md`나 Codex skill을 참고합니다.

```text
$write-as-me-ko 이 메모를 교수님께 보낼 격식체 메시지로 정리해줘.
$write-as-me-ko 이 초안을 내 블로그 글 톤으로 다듬어줘.
```

## Writing Skill Factory

말투 프로필만으로는 부족할 때가 있습니다. 쓰레드 글, 페이스북 글, 링크드인 글,
인스타그램 스토리, 교수님 메시지, 블로그 회고처럼 반복해서 쓰는 글은 각자 다른
규칙을 갖습니다.

이럴 때는 상황별 글쓰기 스킬을 만듭니다.

```text
쓰레드 글쓰기 스킬 만들어줘.
한 시리즈당 500자 이하, 보통 5개, 첫 글은 문제의식 중심,
너무 홍보문처럼 쓰지 말고 내 블로그 말투를 참고해.
```

에이전트는 사용자의 요구를 purpose, audience, constraints, tone, examples,
checklist로 정리한 뒤 `SKILL.md`를 생성합니다. 종류를 Threads/Facebook/LinkedIn
같은 고정 목록으로 제한하지 않습니다. 예시는 starter일 뿐이고, 사용자가 반복해서
쓰는 어떤 글쓰기 상황이든 스킬로 만들 수 있습니다.

직접 생성해야 할 때는 아래 명령을 쓸 수 있습니다.

```powershell
python -m scripts.create_writing_skill --list-presets
python -m scripts.create_writing_skill --preset thread-post --output-root dist\writing-skills --force
```

## Init Workflow

`init`은 두 층으로 동작합니다.

- Python: 샘플 수, 글자 수, 평균 문장 길이, 자주 보이는 표현, route별 신호를 재현 가능하게 뽑습니다.
- LLM: 실제 글을 읽고 "왜 이 사람 글처럼 느껴지는지", 어떤 판단 흐름을 보존해야 하는지 해석합니다.

이렇게 나누면 LLM이 감으로만 말하지 않고, Python이 뽑은 기초 근거를 바탕으로
말투 프로필을 보강할 수 있습니다.

## How It Works

```text
local samples
  -> scripts/init_writing_workspace.py
  -> scripts/build_voice_profile.py
  -> _workspace/writing-init/llm-review.md
  -> codex/skills/write-as-me-ko/references/voice-profile.md
  -> dist/writing/AGENTS.md
  -> Codex skill or Claude Code writing context
```

핵심 reference는 네 가지입니다.

- `voice-profile.md`: Python 기초 분석과 LLM 해석이 합쳐진 말투 프로필
- `judgment-rules.md`: 근거 없는 주장, 과장, 허위 경험을 막는 판단 규칙
- `format-routes.md`: 보고서, 블로그, 메시지, 프로젝트 문서별 작성 형식
- `anti-ai-tells-ko.md`: 번역투, 기계적 구조, 반복 결말 같은 한국어 AI 티 점검표

## Agent Setup Prompt

Codex나 Claude Code에게 설치와 사용 준비를 맡기고 싶다면 아래 프롬프트를 그대로
붙여넣으시면 됩니다.

```text
이 저장소는 한국어 글쓰기용 AGENTS.md와 Codex skill을 만드는 `write-as-me-ko`입니다.

목표:
- 내 로컬 블로그/포트폴리오/보고서/메시지 샘플을 분석해서, 이후 글 작성에 쓸 말투 프로필과 글쓰기용 AGENTS.md를 만들어줘.
- Python 기초 분석과 LLM 문체 해석을 함께 사용해줘.
- AI 탐지 우회나 완벽한 문체 복제를 목표로 하지 말고, 재사용 가능한 작성 기준과 말투 참고 환경을 만드는 데 집중해줘.

해야 할 일:
1. README와 docs를 먼저 읽고 현재 구현된 기능만 기준으로 진행해줘.
2. `samples/` 아래에 실제 개인 글이 있으면 민감한 내용으로 취급하고, git에 새로 추가하지 마.
3. 샘플이 있으면 다음 명령으로 Python 기초 분석, profile 초안, LLM 리뷰 브리프를 만들어줘.
   `python -m scripts.init_writing_workspace --samples samples --repo-root .`
4. `_workspace/writing-init/llm-review.md`를 읽고, 대표 샘플을 확인해서 `voice-profile.md`를 보강해줘.
5. Codex 환경이면 다음 명령으로 skill을 설치해줘.
   `.\scripts\install_codex.ps1 -Force`
6. Claude Code나 일반 에이전트에서 쓸 글쓰기용 AGENTS.md가 필요하면 다음 명령으로 export해줘.
   `python -m scripts.export_agent_context --output dist\writing\AGENTS.md`
7. 마지막에 다음 검증을 실행하고 결과를 알려줘.
   `npm run docs:check`

사용 예시:
- `$write-as-me-ko 이 메모를 교수님께 보낼 격식체 메시지로 정리해줘.`
- `$write-as-me-ko 이 초안을 내 블로그 글 톤으로 다듬어줘.`
```

## Repository Layout

```text
codex/skills/write-as-me-ko/
  SKILL.md
  references/
    anti-ai-tells-ko.md
    format-routes.md
    judgment-rules.md
    voice-profile.md
eval/
  before-after.md
  test-prompts.md
samples/
  README.md
scripts/
  create_writing_skill.py
  build_voice_profile.py
  export_agent_context.py
  init_writing_workspace.py
  install_codex.ps1
  run_eval.py
plugins/write-as-me-ko/
  .codex-plugin/plugin.json
  .claude-plugin/plugin.json
  commands/create-skill.md
  commands/init.md
  skills/create-skill/SKILL.md
  skills/init/SKILL.md
  skills/write/SKILL.md
templates/writing-skill/
  SKILL.md
examples/writing-skills/
tests/
package.json
```

## Evaluation

Stage 4 평가는 private sample을 읽지 않습니다. `eval/before-after.md`에 들어 있는
committed synthetic case를 기준으로 네 가지를 점검합니다.

- 사실 보존
- 장르 유지
- 한국어 자연스러움
- 프로필 신호 반영

```powershell
python -m scripts.run_eval
```

결과는 `_workspace/eval/evaluation-report.md`에 생성됩니다. `_workspace/`는 git에
올라가지 않습니다.

## Verification

```powershell
npm run docs:check
python -m unittest discover -s tests -v
.\scripts\smoke_profile.ps1
python -m scripts.init_writing_workspace --samples samples --profile _workspace\voice-profile.init.md --agents _workspace\writing\AGENTS.md --repo-root .
python -m scripts.export_agent_context --output _workspace\writing\AGENTS.md
python -m scripts.run_eval
```

## Privacy

- `samples/private/`와 `*.local.md`는 gitignore 대상입니다.
- 실제 개인 글은 로컬 입력으로만 쓰고, export된 글쓰기용 `AGENTS.md`에는 원문을 넣지 않습니다.
- 생성된 `voice-profile.md`는 자동 정답이 아니라 사용자가 검토하고 수정할 초안입니다.

## Project Docs

- [Product goal](docs/product-goal.md)
- [Development roadmap](docs/development-roadmap.md)
- [Architecture](docs/architecture.md)
- [Writing skill factory](docs/writing-skill-factory.md)
- [Follow-up thread draft](docs/launch-followup-thread.md)

## Non-Goals

- No fake personal experience generation
- No plagiarism or author impersonation
- No AI-detector bypass guarantee
- No promise that one profile fits every genre
- No hosted storage requirement for private samples
