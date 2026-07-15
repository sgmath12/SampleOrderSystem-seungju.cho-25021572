# 개발 방법론 적용 요약

`CLAUDE.md`의 Agentic Engineering 5원칙을 실제로 어떻게 적용했는지 정리한 요약. 대표 커밋만 표기 (전체 이력은 `git log` 참고).

## 1. 문서 관리

- `CLAUDE.md`(방법론) / `PRD.md`(요구사항) / `plan/`(계획)을 역할별로 분리했고, 후반부에 CLAUDE.md와 PRD.md 내용이 겹치는 걸 발견해 CLAUDE.md를 오케스트레이션 전용으로 축소했다 (`ad1c20f`).
- `plan/전체플랜.md` + `plan_1.md`~`plan_12.md`로 M0(뼈대)부터 M8(마무리)까지 사이클을 쪼개 진행 (`3d54729` SETUP → `f9f0b15` M7 완료).

## 2. Harness

- 매 사이클을 좁은 목표의 `plan_N.md`로 쪼개고, 사람 승인 없이는 GREEN을 커밋하지 않는 게이트를 지켰다. RED/GREEN 커밋을 분리해 체크포인트를 남겼다 (예: `0a26a8e` RED → `89eb31f` GREEN, 생산라인 FIFO 큐).
- 다만 UI 반복 수정 구간(M7 이후)에서는 사용자가 "fast-fix"를 명시적으로 허용해, RED만 정식 커밋하고 GREEN을 fast-fix로 우회한 경우가 있었다 (`3d12eab` RED → `a95a696` fast-fix). 이후 doc-checker가 이 불일치를 지적했다.

## 3. Test — TDD Red-Green-Review

- 도메인 로직은 전 구간 RED→GREEN 쌍으로 진행: 시료 등록(`715ce35`→`8584a3e`), 주문 승인/거절(`142f076`→`e3d13a3`), 재고 예약 버그(`258b2ab`→`79771fd`) 등.
- 콘솔 View/Controller는 `input()`/`print()`가 외부 경계라 판단해 pytest 대상에서 제외하고 수동 스모크 테스트로 검증 (`plan_11.md`에서 이 원칙을 명문화).
- 사용자가 "fast-fix"를 지시한 이후로는 UI 조정(페이지네이션, clear 화면, 로고, 번호 선택 방식 등)을 테스트+구현을 한 커밋에 묶어 빠르게 반영 (`8c36e90`, `6b2307f`, `7850459` 등 다수).

## 4. Clean Code

- 코드 중복 발견 시 즉시 정리 (`8cf4cdc` 중복 메서드 제거, `68654e3` 상태 검증 가드 헬퍼 추출).
- **서브에이전트 활용**: `.claude/agents/doc-checker.md`(문서-코드 정합성), `bug-hunter.md`(엣지케이스), `refactor-expert.md`(리팩터링) 3개를 정의하고, doc-checker+bug-hunter를 **병렬로 2회 실행**했다. 결과는 `reports/subagent-review-2026-07-15-1230.md`, `-1313.md`에 저장. 1차 실행에서 재고 예약 버그·예외 미처리 등을, 2차 실행(UI 재설계 후 재점검)에서 시료 중복등록 허용·평균생산시간 음수 미검증(치명적 2건) 등을 발견했고, 전부 RED-GREEN 사이클로 수정 (`8aa36fd`→`a3c7239`, `46190cc`→`d59186b`). refactor-expert는 리팩터링 전후 pytest 79개 통과를 확인하며 `order.py` 중복 제거를 수행 (`68654e3`).

## 5. Commit 이력

- RED/GREEN/fast-fix 접두사로 커밋 메시지를 일관되게 남겨, 이력만 봐도 "계획→실패→구현→리뷰→통과" 흐름이 드러나도록 관리했다.
