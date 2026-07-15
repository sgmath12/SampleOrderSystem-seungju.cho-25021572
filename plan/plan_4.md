# Plan 4 — M2: 시료 주문 (Order 생성)

## 목표

`src/model`에 주문(Order) 도메인을 도입한다. 고객의 시료 요청을 받아 주문 담당자가 주문을 생성하면 `RESERVED` 상태로 저장되도록 한다. 등록되지 않은 시료로는 주문할 수 없다는 제약을 포함한다.

## 배경 (CLAUDE.md 근거)

- 고객이 시료를 요청하면 주문 담당자가 주문을 생성 (시료 예약)
- 고객이 원하는 시료와 수량을 주문 → 이 시점에서 주문 상태는 `RESERVED`
- 예약 시 입력값: 시료 ID, 고객명, 주문 수량
- 시료 관리(M1) 규칙: 시스템에 등록된 시료만 주문 가능

## 범위 (In Scope)

- `Order` 데이터 구조: `order_id`, `sample_id`, `customer`, `quantity`, `status`(기본값 `"RESERVED"`)
- `OrderRepository`
  - `create(sample_repository, sample_id, customer, quantity)`
    - `sample_repository`에 등록된 `sample_id`가 없으면 `ValueError` 발생 (등록된 시료만 주문 가능 규칙)
    - 존재하면 `order_id`를 자동 채번(1부터 증가)하여 `RESERVED` 상태의 Order를 생성·저장
  - `list_all()` — 생성된 모든 주문을 리스트로 반환

## 범위 밖 (Out of Scope) — 다음 사이클로

- 주문 승인/거절 로직 (재고 확인, CONFIRMED/PRODUCING/REJECTED 전환) → M3
- 생산라인/재고 반영 → M4
- 콘솔 View/Controller 연결 → M7

## RED 대상 테스트

파일: `tests/model/test_order_repository.py` (신규)

1. `test_create_order_is_reserved_with_given_fields`
   - 등록된 시료로 주문을 생성하면 `sample_id`, `customer`, `quantity`가 그대로 저장되고 `status == "RESERVED"`이다.
2. `test_create_order_assigns_incrementing_order_id`
   - 주문을 두 번 생성하면 각각 다른 `order_id`가 순차적으로 부여된다.
3. `test_create_order_raises_for_unregistered_sample`
   - `SampleRepository`에 등록되지 않은 `sample_id`로 주문을 생성하면 `ValueError`가 발생한다.
4. `test_list_all_returns_created_orders`
   - 생성한 주문들이 `list_all()`에 모두 포함된다.

## 완료 조건 (Definition of Done)

- [ ] 위 4개 테스트가 RED(실패) 상태를 직접 확인한 뒤 RED 커밋 (`RED: 시료 주문 생성 실패하는 테스트 추가`)
- [ ] `Order`, `OrderRepository`를 테스트 통과시키는 최소한의 코드로 구현 (GREEN, 아직 커밋 안 함)
- [ ] 전체 테스트 통과, 출력 깨끗함
- [ ] `.claude/skills/clean-code/SKILL.md` 기준 셀프 리뷰 후 사람 파트너 REVIEW 승인
- [ ] GREEN 커밋 (`GREEN: 시료 주문 생성 구현 (리뷰 완료)`)

## 다음 사이클 예고

**plan_5.md**: M3 주문 승인/거절 — RESERVED 목록 조회, 승인 시 재고 확인 후 CONFIRMED/PRODUCING 분기, 거절 시 REJECTED.
