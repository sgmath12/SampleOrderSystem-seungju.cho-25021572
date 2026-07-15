# Plan 6 — M4: 생산라인 (FIFO 큐, 실생산량/생산시간 계산)

## 목표

`ProductionLine` 도메인을 도입해, 재고 부족으로 생산이 필요한 주문을 FIFO 큐로 관리하고, 완료 처리 시 수율을 반영한 실생산량을 계산해 재고에 반영하고 주문을 `CONFIRMED`로 전환한다.

이번 사이클은 **ProductionLine 자체의 메커니즘**에 집중한다. `OrderRepository.approve()`가 재고 부족 시 자동으로 이 큐에 등록하도록 연결하는 작업은 **plan_7.md**에서 다룬다 (좁은 목표 유지).

## 배경 (CLAUDE.md 근거)

- 생산라인에 대한 정보 표시
- 주문량에 대한 부족분을 생산하되, 수율 및 오차를 고려하여 시료를 생산
  - 실생산량 = ceil(부족분 / 수율)
  - 총생산시간 = 평균 생산시간 × 실생산량
- 생산 완료 시 주문 상태 PRODUCING → CONFIRMED 로 변경
- 대기 주문 확인: 생산라인의 대기열(생산 큐), 스케줄링 전략 FIFO
- PRD.md 수율 예시: 부족분 16, 수율 0.8 → 실생산량 20 → 재고 20 반영 → 주문 16 소비 → 잉여 4

## 범위 (In Scope)

- `ProductionJob` 데이터 구조: `order`(Order 객체), `sample`(Sample 객체), `shortfall`(등록 시점의 부족분)
- `ProductionLine`
  - `enqueue(order, sample, shortfall)` — 큐 맨 뒤에 작업 등록
  - `list_pending()` — 대기 중인 작업을 등록 순서(FIFO) 그대로 반환
  - `complete_next()`
    - 큐 맨 앞의 작업을 꺼내 처리(FIFO)
    - 실생산량 = `ceil(shortfall / sample.yield_rate)`
    - 총생산시간 = `sample.avg_production_time * 실생산량` (계산만 하고 반환값에 포함, 실제 대기 없음)
    - `sample.inventory += 실생산량`
    - `order.status = "CONFIRMED"`
    - 처리된 작업은 대기 큐에서 제거됨

## 범위 밖 (Out of Scope) — 다음 사이클로

- `OrderRepository.approve()`가 재고 부족 시 `ProductionLine.enqueue()`를 자동 호출하도록 연결 → **plan_7.md**
- "현재 생산 중" 표기, 콘솔 출력 포맷 → M7
- 여러 생산라인/동시 생산 (요구사항상 단일 라인이므로 불필요)

## RED 대상 테스트

파일: `tests/model/test_production_line.py` (신규)

1. `test_enqueue_adds_job_to_pending_queue`
2. `test_list_pending_preserves_fifo_order`
   - 두 작업을 등록한 순서대로 `list_pending()`이 반환한다.
3. `test_complete_next_adds_ceil_actual_quantity_to_inventory`
   - 부족분 16, 수율 0.8인 작업 완료 시 재고가 20만큼 증가한다 (ceil(16/0.8)=20, PRD.md 예시와 일치).
4. `test_complete_next_sets_order_status_confirmed`
   - 완료 처리된 작업의 주문 상태가 `CONFIRMED`로 바뀐다.
5. `test_complete_next_removes_job_from_pending_queue`
   - 완료 처리 후 해당 작업은 `list_pending()`에서 사라지고, 다음 `complete_next()` 호출 시 그 다음 작업(FIFO)이 처리된다.

## 완료 조건 (Definition of Done)

- [ ] 위 5개 테스트가 RED(실패) 상태를 직접 확인한 뒤 RED 커밋 (`RED: 생산라인 FIFO 큐 실패하는 테스트 추가`)
- [ ] `ProductionJob`, `ProductionLine`을 테스트 통과시키는 최소한의 코드로 구현 (GREEN, 아직 커밋 안 함)
- [ ] 전체 테스트 통과, 출력 깨끗함
- [ ] `.claude/skills/clean-code/SKILL.md` 기준 셀프 리뷰 후 사람 파트너 REVIEW 승인
- [ ] GREEN 커밋 (`GREEN: 생산라인 FIFO 큐 구현 (리뷰 완료)`)

## 다음 사이클 예고

**plan_7.md**: `OrderRepository.approve()`가 재고 부족 시 `ProductionLine.enqueue()`를 자동 호출하도록 연결 (CLAUDE.md의 "생산라인에 자동으로 등록" 요구 충족).
