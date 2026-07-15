# Plan 3 — M1: 시료 관리 (검색)

## 목표

`plan_2.md`에서 만든 `SampleRepository`에 이름 등 속성으로 특정 시료를 검색하는 기능을 추가한다. M1(시료 관리)의 마지막 사이클이다.

## 배경 (CLAUDE.md 근거)

- 시료 검색: 이름 등 속성으로 특정 시료를 검색

## 범위 (In Scope)

- `SampleRepository.search_by_name(keyword)` — 이름에 `keyword`가 포함된 시료들을 리스트로 반환
  - 부분 일치(substring) 검색
  - 일치하는 시료가 없으면 빈 리스트 반환

## 범위 밖 (Out of Scope)

- 이름 외 다른 속성(ID, 수율 등) 기준 검색 — CLAUDE.md에 "이름 등"으로만 언급되어 있어 우선 이름 검색만 구현하고, 추가 속성 검색은 필요 시 별도 요청받아 진행
- 대소문자 무시/자모 분리 검색 등 고급 매칭 — 요구사항에 없으므로 미포함
- 콘솔 View/Controller 연결 → M7

## RED 대상 테스트

파일: `tests/model/test_sample_repository.py` (기존 파일에 추가)

1. `test_search_by_name_returns_matching_samples`
   - "웨이퍼"로 검색하면 이름에 "웨이퍼"가 포함된 시료만 반환된다 (포함되지 않는 시료는 제외).
2. `test_search_by_name_returns_empty_when_no_match`
   - 어떤 시료 이름에도 없는 키워드로 검색하면 빈 리스트를 반환한다.

## 완료 조건 (Definition of Done)

- [ ] 위 2개 테스트가 RED(실패) 상태를 직접 확인한 뒤 RED 커밋 (`RED: 시료 이름 검색 실패하는 테스트 추가`)
- [ ] `search_by_name`을 테스트 통과시키는 최소한의 코드로 구현 (GREEN, 아직 커밋 안 함)
- [ ] 전체 테스트 통과, 출력 깨끗함
- [ ] `.claude/skills/clean-code/SKILL.md` 기준으로 셀프 리뷰 후 사람 파트너 REVIEW 승인
- [ ] GREEN 커밋 (`GREEN: 시료 이름 검색 구현 (리뷰 완료)`)

## 다음 사이클 예고

M1 완료. **plan_4.md**부터는 M2 시료 주문 — 주문 접수 시 RESERVED 상태로 Order 생성 (존재하지 않는 시료 ID로 주문 시 에러 처리 포함).
