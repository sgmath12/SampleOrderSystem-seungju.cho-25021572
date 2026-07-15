# Plan 2 — M1: 시료 관리 (등록 / 목록 조회)

첫 정식 TDD Red-Green-Review 사이클. `.claude/skills/tdd/SKILL.md`를 그대로 따른다.

## 목표

`src/model`에 시료(Sample) 도메인을 도입한다. 이번 사이클의 범위는 **등록**과 **목록 조회**로 한정한다. 검색 기능은 다음 사이클(`plan_3.md`)에서 다룬다.

## 배경 (CLAUDE.md 근거)

- 시료(Sample)는 시스템의 가장 기본이 되는 단위. 각 시료는 고유한 이름과 속성을 가지며, 시스템에 등록된 시료만 주문 가능.
- 시료 등록 속성값: 시료 ID, 이름, 평균 생산 시간, 수율
- 시료 조회: 등록된 모든 시료 목록 확인, **현재 재고 수량도 함께 표시**

## 범위 (In Scope)

- `Sample` 데이터 구조: `sample_id`, `name`, `avg_production_time`, `yield_rate`, `inventory`(초기값 0)
- `SampleRepository`
  - `register(sample_id, name, avg_production_time, yield_rate)` — 새 시료 등록, 초기 재고 0
  - `list_all()` — 등록된 모든 시료를 리스트로 반환 (재고 포함)

## 범위 밖 (Out of Scope) — 다음 사이클로

- 이름/속성으로 검색하는 기능 → `plan_3.md`
- 중복 시료 ID 등록 시 에러 처리 → 필요성이 확인되면 별도 사이클에서 다룬다 (현재 CLAUDE.md에 명시적 요구 없음)
- 재고 증감 로직(생산 완료/출고 시 반영) → M4, M5에서 Order/ProductionLine과 함께 다룬다
- 콘솔 View/Controller 연결 → M7

## RED 대상 테스트 (각각 하나의 behavior)

파일: `tests/model/test_sample_repository.py`

1. `test_register_sample_appears_in_list`
   - 시료 하나를 등록하면 `list_all()`에 해당 시료(ID/이름/평균생산시간/수율)가 포함된다.
2. `test_registered_sample_starts_with_zero_inventory`
   - 새로 등록한 시료의 초기 재고는 0이다.
3. `test_list_all_returns_empty_when_nothing_registered`
   - 아무것도 등록하지 않았으면 `list_all()`은 빈 리스트를 반환한다.

## 완료 조건 (Definition of Done)

- [ ] 위 3개 테스트가 각각 RED(실패) 상태를 직접 확인한 뒤 RED 커밋 (`RED: 시료 등록/목록조회 실패하는 테스트 추가`)
- [ ] `Sample`, `SampleRepository`를 테스트를 통과시키는 최소한의 코드로 구현 (GREEN, 아직 커밋 안 함)
- [ ] 전체 테스트(`pytest`) 통과, 출력 깨끗함
- [ ] 사람 파트너 REVIEW 승인
- [ ] GREEN 커밋 (`GREEN: 시료 등록/목록조회 구현 (리뷰 완료)`)

## 다음 사이클 예고

**plan_3.md**: M1 나머지 — 이름 등 속성으로 시료 검색.
