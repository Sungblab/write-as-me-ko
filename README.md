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

Codex나 Claude Code에게 설치와 사용 준비를 맡기고 싶다면 아래 프롬프트를 그대로 붙여넣습니다.

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
