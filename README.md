# write-as-me-ko

한국어 사용자를 위한 로컬-first 개인 문체 컨텍스트 팩입니다.

이 프로젝트는 [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai)의 한국어 AI 문체 탐지/윤문 접근에서 영감을 받았습니다. `im-not-ai`가 이미 생성된 글의 AI 티를 줄이는 후처리 도구에 가깝다면, `write-as-me-ko`는 사용자의 글 샘플, 판단 기준, 산출물 형식을 에이전트가 처음부터 참고하도록 만드는 것을 목표로 합니다.

목표는 AI 글을 사람 글처럼 속이는 것이 아닙니다. 매번 같은 말투 설명을 반복하지 않아도 보고서, 에세이, 블로그, 메시지, 프로젝트 문서가 사용자의 실제 한국어 습관에 더 가까워지게 만드는 것입니다.

## Quickstart

샘플 글을 넣습니다.

```text
samples/
  blog/
  report/
  message/
```

프로필 초안을 생성합니다.

```powershell
python -m scripts.build_voice_profile --samples samples --output codex\skills\write-as-me-ko\references\voice-profile.md
```

Codex skill로 설치합니다.

```powershell
.\scripts\install_codex.ps1 -Force
```

일반 에이전트용 컨텍스트 파일이 필요하면 export 합니다.

```powershell
python -m scripts.export_agent_context --output dist\AGENTS.write-as-me-ko.md
```

이후 Codex에서 다음처럼 사용합니다.

```text
$write-as-me-ko 이 메모를 교수님께 보낼 격식체 메시지로 정리해줘.
$write-as-me-ko 이 초안을 내 블로그 글 톤으로 다듬어줘.
```

## MVP Scope

현재 버전은 Codex skill과 프로필 생성 스크립트를 제공합니다.

```text
codex/skills/write-as-me-ko/
  SKILL.md
  references/
    anti-ai-tells-ko.md
    format-routes.md
    judgment-rules.md
    voice-profile.md
scripts/
  build_voice_profile.py
  export_agent_context.py
  install_codex.ps1
  run_eval.py
package.json
```

할 수 있는 일:

- 한국어 보고서, 에세이, 블로그, 메시지 초안 작성
- 일반적인 AI 초안을 로컬 voice profile 기준으로 재작성
- 격식체는 격식체로, 구어체는 구어체로 유지
- 번역투, 기계적 전환, 과장된 주장, 반복적인 결말 같은 한국어 AI 티 점검

## Repository Layout

```text
samples/
  blog/       # user's blog or reflective writing samples
  report/     # reports, essays, assignment-style writing
  message/    # emails, team messages, professor-facing notes
eval/
  test-prompts.md
  before-after.md
codex/skills/write-as-me-ko/
```

실제 샘플을 `samples/` 아래에 넣고 `scripts.build_voice_profile`을 실행하면 `codex/skills/write-as-me-ko/references/voice-profile.md` 초안이 갱신됩니다. 생성된 프로필은 그대로 믿기보다 한 번 읽고 수정하는 것을 전제로 합니다.

## Project Docs

- [Product goal](docs/product-goal.md)
- [Development roadmap](docs/development-roadmap.md)
- [Architecture](docs/architecture.md)

## Verification

```powershell
npm run docs:check
python -m unittest discover -s tests -v
.\scripts\smoke_profile.ps1
python -m scripts.export_agent_context --output _workspace\AGENTS.write-as-me-ko.smoke.md
python -m scripts.run_eval
```

## Non-goals

- No fake personal experience generation
- No plagiarism or author impersonation
- No AI-detector bypass guarantee
- No promise that one profile fits every genre
