# write-as-me-ko

한국어 글 샘플을 로컬에서 분석해 AI 에이전트가 참고할 author context를
만드는 작은 도구입니다.

[`im-not-ai`](https://github.com/epoko77-ai/im-not-ai)가 이미 나온 초안의 한국어 AI 티를 줄이는 후처리 도구에 가깝다면,
`write-as-me-ko`는 초안을 쓰기 전에 "나는 어떤 기준과 형식으로 쓰는가"를
에이전트에게 먼저 알려주는 쪽에 가깝습니다.

목표는 AI detector 우회나 완벽한 문체 복제가 아닙니다. 매번 "내 스타일로",
"너무 AI처럼 쓰지 말고", "보고서 톤으로", "교수님께 보내는 말투로"를 반복하지
않게 만드는 재사용 가능한 한국어 작성 컨텍스트가 핵심입니다.

## What It Does

- `samples/` 아래의 한국어 `.md`, `.txt` 샘플을 읽습니다.
- blog, report, message, project 같은 글의 route를 나눠 봅니다.
- 자주 보이는 표현, 문장 길이, route별 작성 신호를 `voice-profile.md`로 정리합니다.
- Codex skill 또는 일반 에이전트용 `AGENTS.write-as-me-ko.md`로 사용할 수 있게 합니다.
- 원문 샘플을 portable context에 복사하지 않고, 요약된 규칙과 프로필만 export합니다.
- synthetic before/after 사례로 사실 보존, 장르 유지, 한국어 자연스러움, 프로필 반영을 점검합니다.

## Quickstart

샘플 글을 route별로 넣습니다.

```text
samples/
  blog/
  report/
  message/
  project/
```

프로필 초안을 생성합니다.

```powershell
python -m scripts.build_voice_profile --samples samples --output codex\skills\write-as-me-ko\references\voice-profile.md
```

생성된 `voice-profile.md`를 읽고 필요한 부분을 직접 고칩니다. 실제 샘플이 적으면
프로필은 보수적으로 동작해야 합니다.

Codex skill로 설치합니다.

```powershell
.\scripts\install_codex.ps1 -Force
```

Codex에서 사용합니다.

```text
$write-as-me-ko 이 메모를 교수님께 보낼 격식체 메시지로 정리해줘.
$write-as-me-ko 이 초안을 내 블로그 글 톤으로 다듬어줘.
```

다른 에이전트에서 쓸 단일 컨텍스트 파일이 필요하면 export합니다.

```powershell
python -m scripts.export_agent_context --output dist\AGENTS.write-as-me-ko.md
```

## How It Works

```text
local samples
  -> scripts/build_voice_profile.py
  -> codex/skills/write-as-me-ko/references/voice-profile.md
  -> Codex skill or exported AGENTS.write-as-me-ko.md
```

핵심 reference는 네 가지입니다.

- `voice-profile.md`: 샘플에서 뽑은 문체, route, confidence, privacy note
- `judgment-rules.md`: 근거 없는 주장, 과장, 허위 경험을 막는 판단 규칙
- `format-routes.md`: 보고서, 블로그, 메시지, 프로젝트 문서별 작성 형식
- `anti-ai-tells-ko.md`: 번역투, 기계적 구조, 반복 결말 같은 한국어 AI 티 점검표

## Agent Setup Prompt

Codex나 Claude Code에게 설치와 사용 준비를 맡기고 싶다면 아래 프롬프트를 그대로
붙여넣으시면 됩니다.

```text
이 저장소는 한국어 개인 문체 컨텍스트 팩 `write-as-me-ko`입니다.

목표:
- 내 로컬 샘플 글을 바탕으로 한국어 글쓰기용 author context를 설치하고, 바로 사용할 수 있게 준비해줘.
- AI 탐지 우회나 완벽한 문체 복제를 목표로 하지 말고, 재사용 가능한 작성 기준과 말투 참고 컨텍스트를 만드는 데 집중해줘.

해야 할 일:
1. README와 docs를 먼저 읽고 현재 구현된 기능만 기준으로 진행해줘.
2. `samples/` 아래에 실제 개인 글이 있으면 민감한 내용으로 취급하고, git에 새로 추가하지 마.
3. 샘플이 있으면 다음 명령으로 voice profile 초안을 만들어줘.
   `python -m scripts.build_voice_profile --samples samples --output codex\skills\write-as-me-ko\references\voice-profile.md`
4. Codex 환경이면 다음 명령으로 skill을 설치해줘.
   `.\scripts\install_codex.ps1 -Force`
5. Claude Code나 일반 에이전트에서 쓸 컨텍스트가 필요하면 다음 명령으로 AGENTS 파일을 export해줘.
   `python -m scripts.export_agent_context --output dist\AGENTS.write-as-me-ko.md`
6. 마지막에 다음 검증을 실행하고 결과를 알려줘.
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
  build_voice_profile.py
  export_agent_context.py
  install_codex.ps1
  run_eval.py
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
python -m scripts.export_agent_context --output _workspace\AGENTS.write-as-me-ko.smoke.md
python -m scripts.run_eval
```

## Privacy

- `samples/private/`와 `*.local.md`는 gitignore 대상입니다.
- 실제 개인 글은 로컬 입력으로만 쓰고, export된 agent context에는 원문을 넣지 않습니다.
- 생성된 `voice-profile.md`는 자동 정답이 아니라 사용자가 검토하고 수정할 초안입니다.

## Project Docs

- [Product goal](docs/product-goal.md)
- [Development roadmap](docs/development-roadmap.md)
- [Architecture](docs/architecture.md)

## Non-Goals

- No fake personal experience generation
- No plagiarism or author impersonation
- No AI-detector bypass guarantee
- No promise that one profile fits every genre
- No hosted storage requirement for private samples
