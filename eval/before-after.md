# Before / After Log

These cases are synthetic and safe to keep in git. They test whether
`write-as-me-ko` keeps facts, preserves the requested route, avoids common Korean
AI tells, and uses the local profile rules without committing private samples.

### Case: Report intro

Route: report
Prompt: Write a short Korean report introduction about why a local-first AI writing context pack is useful for Korean users.

Expected Facts:
- local-first
- Korean users

Required Profile Signals:
- 근거
- 한계

### Generic Draft

결론적으로 로컬-first AI 글쓰기 컨텍스트 팩은 한국어 사용자에게 혁신적인 가능성을
제시한다. 이 도구는 중요한 역할을 하며, 다양한 가능성을 통해 효율적인 글쓰기를
지원한다.

### write-as-me-ko Draft

로컬-first AI 글쓰기 컨텍스트 팩은 한국어 사용자가 매번 같은 문체 설명을 반복하지
않도록 돕는다. 이 보고서는 샘플을 외부에 올리지 않는다는 전제를 먼저 두고, 그
전제가 어떤 근거로 유용한지와 어떤 한계를 갖는지 나누어 살핀다.

### Notes

- What improved: 근거와 한계를 분리했고, 과장된 표현을 줄였다.
- What still sounds wrong: 실제 사용자 샘플이 없으면 문체 확신은 낮다.
- Profile update needed: 보고서 샘플을 추가하면 더 구체화할 수 있다.

### Case: Blog reflection

Route: blog
Prompt: Write a personal blog-style note about realizing that "AI humanizer" tools solve the problem too late.

Expected Facts:
- AI humanizer
- too late

Required Profile Signals:
- 생각
- 바뀌었다

### Generic Draft

AI humanizer는 매우 의미 있는 도구이며 글쓰기의 새로운 패러다임을 제시한다.
결론적으로 우리는 이러한 도구를 통해 더 나은 결과를 얻을 수 있다.

### write-as-me-ko Draft

나는 AI humanizer를 처음 봤을 때 꽤 실용적이라고 생각했다. 그런데 써볼수록 문제를
too late에 고치고 있다는 느낌이 들었다. 이미 어색한 초안이 나온 뒤에 표면만 다듬는
방식이라면, 처음부터 어떤 문체와 판단 기준을 참고할지 정하는 쪽으로 생각이
바뀌었다.

### Notes

- What improved: 1인칭 판단 변화가 드러난다.
- What still sounds wrong: 영어 표현은 실제 블로그 톤에 맞게 바꿀 수 있다.
- Profile update needed: 회고 샘플이 있으면 문장 리듬을 더 맞출 수 있다.

### Case: Professor message

Route: message
Prompt: Write a concise formal Korean message to a professor explaining that I am submitting an updated project document and asking for review.

Expected Facts:
- 수정한 프로젝트 문서
- 검토

Required Profile Signals:
- 확인
- 검토

### Generic Draft

교수님께서는 바쁘시겠지만, 저는 이번 문서를 통해 프로젝트의 의미 있는 개선 방향을
제시하고자 합니다. 결론적으로 검토를 부탁드립니다.

### write-as-me-ko Draft

교수님, 안녕하세요. 수정한 프로젝트 문서를 다시 제출드립니다. 변경한 부분을 확인해
주시고, 가능하실 때 검토 의견을 부탁드립니다. 감사합니다.

### Notes

- What improved: 배경을 길게 늘리지 않고 요청과 다음 행동을 분리했다.
- What still sounds wrong: 실제 제출 맥락에 맞는 파일명은 사용자가 넣어야 한다.
- Profile update needed: 교수님께 보낸 실제 메시지 샘플이 있으면 높임 표현을 조정할 수 있다.

### Case: Project README copy

Route: project
Prompt: Write README copy that explains this repository without sounding like a marketing landing page.

Expected Facts:
- write-as-me-ko
- local-first

Required Profile Signals:
- 검증
- 한계

### Generic Draft

write-as-me-ko는 혁신적인 AI 시대를 위한 차세대 솔루션입니다. 다양한 가능성을
제시하며 사용자의 글쓰기 경험을 완전히 변화시킵니다.

### write-as-me-ko Draft

`write-as-me-ko`는 한국어 글 샘플과 판단 기준을 local-first 방식으로 정리해 AI
에이전트가 참고할 컨텍스트를 만드는 프로젝트입니다. README에서는 사용 방법, 검증
명령, 현재 한계를 분리해 설명하고, 완전한 문체 복제나 detector 우회처럼 확인되지
않은 주장은 하지 않습니다.

### Notes

- What improved: 프로젝트 설명과 검증, 한계를 분리했다.
- What still sounds wrong: 실제 배포 방식이 바뀌면 README 문구도 갱신해야 한다.
- Profile update needed: 프로젝트 문서 샘플이 늘어나면 문서 톤을 더 좁힐 수 있다.
