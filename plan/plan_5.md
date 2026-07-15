# Plan 5 — M3: 주문 승인/거절

## 목표

접수된(`RESERVED`) 주문을 조회하고, 재고 상황에 따라 승인(`CONFIRMED`/`PRODUCING` 분기) 또는 거절(`REJECTED`)할 수 있게 한다.

## 배경 (CLAUDE.md 근거)

- 접수된 주문(RESERVED) 목록을 확인, 특정 주문에 대해 승인 또는 거절
- 주문 승인: 재고 상황에 따라 자동으로 2가지 방식으로 처리
  - 재고 충분 → 주문을 즉시 CONFIRMED 상태로 전환
  - 재고 부족 → 생산라인에 자동 등록, 주문 상태를 PRODUCING으로 전환
- 주문 거절: 즉시 REJECTED 상태로 전환

## 범위 (In Scope)

- `SampleRepository.find_by_id(sample_id)` — 승인 로직이 재고를 조회하기 위해 필요한 최소 조회 기능 (없으면 `None` 반환)
- `OrderRepository.list_reserved()` — `RESERVED` 상태 주문만 반환
- `OrderRepository.approve(order_id, sample_repository)`
  - 재고(`sample.inventory`) ≥ 주문 수량 → 재고에서 수량만큼 차감하고 주문 상태 `CONFIRMED`
  - 재고 < 주문 수량 → 주문 상태 `PRODUCING` (재고는 변경하지 않음, 실제 생산 큐 등록은 M4에서 다룸)
- `OrderRepository.reject(order_id)` — 주문 상태를 즉시 `REJECTED`로 전환

## 범위 밖 (Out of Scope) — 다음 사이클로

- 생산 큐(FIFO) 등록, 실생산량/생산시간 계산, 생산 완료 처리 → M4
- 출고 처리(CONFIRMED → RELEASE) → M5
- 모니터링 집계(상태별 카운트, 재고 여유/부족/고갈 표기) → M6
- 콘솔 View/Controller 연결 → M7

## RED 대상 테스트

### `tests/model/test_sample_repository.py`에 추가

1. `test_find_by_id_returns_matching_sample`
2. `test_find_by_id_returns_none_when_not_found`

### `tests/model/test_order_repository.py`에 추가

3. `test_approve_confirms_order_and_deducts_inventory_when_sufficient`
   - 재고가 주문 수량 이상이면 승인 시 `CONFIRMED`로 전환되고 재고가 주문 수량만큼 줄어든다.
4. `test_approve_sets_producing_and_keeps_inventory_when_insufficient`
   - 재고가 주문 수량 미만이면 승인 시 `PRODUCING`으로 전환되고 재고는 그대로다.
5. `test_reject_sets_status_to_rejected`
   - 거절하면 주문 상태가 `REJECTED`로 전환된다.
6. `test_list_reserved_returns_only_reserved_orders`
   - 승인/거절 처리된 주문은 제외하고 `RESERVED` 상태인 주문만 반환된다.

## 완료 조건 (Definition of Done)

- [ ] 위 6개 테스트가 RED(실패) 상태를 직접 확인한 뒤 RED 커밋 (`RED: 주문 승인/거절 실패하는 테스트 추가`)
- [ ] `find_by_id`, `list_reserved`, `approve`, `reject`를 테스트 통과시키는 최소한의 코드로 구현 (GREEN, 아직 커밋 안 함)
- [ ] 전체 테스트 통과, 출력 깨끗함
- [ ] `.claude/skills/clean-code/SKILL.md` 기준 셀프 리뷰 후 사람 파트너 REVIEW 승인
- [ ] GREEN 커밋 (`GREEN: 주문 승인/거절 구현 (리뷰 완료)`)

## 다음 사이클 예고

**plan_6.md**: M4 생산라인 — FIFO 생산 큐, 실생산량(ceil(부족분/수율))·총생산시간 계산, 생산 완료 시 PRODUCING → CONFIRMED 전환 및 재고 반영.
