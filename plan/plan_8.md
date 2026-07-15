# Plan 8 — 버그 수정: 재고 예약(reservation) 및 잉여 산정

## 배경 — 발견된 모순

사용자가 제시한 시나리오로 기존 구현을 검증한 결과, 두 가지 버그를 발견했다.

> 100개 주문(A) → 실생산량 150개. 생산 중 재고가 70개까지 찼을 때 20개 주문(B)이 들어와도, A의 100개가 아직 안 채워졌으므로 그 70개를 B에게 줄 수 없다. 재고가 120개(≥100)에 도달해야 A가 확정되고, 그 초과분(20)부터 B에게 쓸 수 있다. 150개 다 채우면 A(100)+B(20) 쓰고 30이 잉여로 남는다 — 모순 없이 맞아떨어져야 한다.

### 버그 1 — `complete_next()`가 주문의 소비량을 빼지 않음

현재: `sample.inventory += actual_quantity` (생산량 전체를 그대로 재고에 더함)

PRD.md 수율 예시(부족분16, 수율0.8 → 실생산량20 → **주문이 16 소비 → 잉여 4**)와 불일치. 지금 코드는 완료 후 재고가 20으로 남아 4가 아니다. 기존 테스트 `test_complete_next_adds_ceil_actual_quantity_to_inventory`도 이 잘못된 기대값(20)을 검증하고 있었다.

### 버그 2 — PRODUCING 중인 주문의 기존 재고가 보호되지 않음

현재: `approve()`가 재고 부족 시 `sample.inventory`를 건드리지 않고 그대로 둔다. 그 사이 다른 주문이 `approve()`를 호출하면, 아직 확정되지 않은 원래 주문 몫으로 묶여 있어야 할 재고를 가져가 버릴 수 있다 (재고 유출).

## 수정 설계

- `approve()`가 재고 부족으로 `PRODUCING` 전환할 때: 그 시점의 `sample.inventory`(예: 70)를 **즉시 그 주문 몫으로 소진**시킨다 (`sample.inventory = 0`). 이 재고는 이미 부족(`shortfall = quantity - inventory`)해서 이 주문 하나도 못 채우는 양이므로, 전액이 이 주문에 귀속되고 다른 주문에는 보이지 않아야 한다.
- `complete_next()`가 완료 처리할 때: `잉여 = actual_quantity - shortfall`(수율로 인한 초과분)만 재고에 더한다. `shortfall`은 이미 이 주문에 귀속된 양이므로 재고로 다시 돌아오지 않는다.

### 검증 (PRD.md 예시와 일치하는지)

부족분 16, 수율 0.8 → 실생산량 20 → 잉여 = 20 − 16 = **4** ✅ (PRD.md와 일치)

### 검증 (사용자 시나리오와 일치하는지)

재고 70, 주문 A 수량 100 → 부족분 30 (100−70) → approve 시 재고 0으로 소진 → 실생산량 = ceil(30/수율). 생산 완료 시 잉여 = 실생산량 − 30이 재고에 반영되고 A는 CONFIRMED. 그 사이 도착한 주문 B(20)는 재고가 0이므로(보호됨) 즉시 확정되지 못하고 별도 생산 작업으로 큐에 등록된다 — "70개를 20개한테 못 줌" 규칙 충족.

## 범위 (In Scope)

- `OrderRepository.approve()`: `PRODUCING` 분기에서 `sample.inventory`를 0으로 소진
- `ProductionLine.complete_next()`: `sample.inventory += (actual_quantity - shortfall)`로 변경
- 위 변경으로 인해 깨지는 기존 테스트 2건을 올바른 기대값으로 수정
  - `test_approve_sets_producing_and_keeps_inventory_when_insufficient` → 재고가 0으로 소진되는 것을 검증하도록 수정 (테스트명도 사실에 맞게 변경)
  - `test_complete_next_adds_ceil_actual_quantity_to_inventory` → 잉여(4)만 반영되는 것을 검증하도록 수정

## 범위 밖

- 여러 생산라인 동시 처리, 실시간 부분 진행률 표시 (요구사항에 없음, 단일 라인 FIFO로 충분)
- 콘솔 표기 → M7

## RED 대상 테스트

1. `test_approve_reserves_existing_inventory_when_insufficient` (신규, `test_order_repository.py`)
   - 재고 70에 주문 100 승인 시 `sample.inventory`가 0이 된다.
2. `test_new_order_cannot_consume_inventory_reserved_by_pending_order` (신규, `test_order_repository.py`)
   - 재고 70, 주문 A(100) 승인 후 재고가 0이 됨 → 그 상태에서 주문 B(20)를 승인하면 재고가 없어 `PRODUCING`으로 전환된다 (CONFIRMED로 잘못 확정되지 않음).
3. `test_complete_next_adds_only_surplus_to_inventory` (기존 테스트 대체, `test_production_line.py`)
   - 부족분 16, 수율 0.8 → 완료 후 재고는 **4** (20 − 16).

## 완료 조건 (Definition of Done)

- [ ] 위 신규/수정 테스트가 RED(실패) 상태를 직접 확인한 뒤 RED 커밋 (`RED: 재고 예약/잉여 산정 버그 재현 실패하는 테스트 추가`)
- [ ] `approve()`, `complete_next()` 수정으로 전체 테스트 통과 (GREEN, 아직 커밋 안 함)
- [ ] PRD.md 수율 예시(잉여 4)와 사용자 시나리오(재고 유출 방지) 둘 다 테스트로 커버됨을 확인
- [ ] `.claude/skills/clean-code/SKILL.md` 기준 셀프 리뷰 후 사람 파트너 REVIEW 승인
- [ ] GREEN 커밋 (`GREEN: 재고 예약/잉여 산정 버그 수정 (리뷰 완료)`)

## 다음 사이클 예고

**plan_9.md**: M5 출고 처리 — CONFIRMED 주문 출고 시 RELEASE 전환 (재고는 이미 CONFIRMED 시점에 확정 소비되었으므로 출고 자체는 재고 차감 없이 상태 전환만 하는지 확인).
