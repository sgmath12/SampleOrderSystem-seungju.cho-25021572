# Plan 7 — M4 마무리: approve() ↔ 생산라인 자동 등록 + 총생산시간

## 목표

`OrderRepository.approve()`가 재고 부족 시 `ProductionLine`에 자동으로 작업을 등록하도록 연결한다 (CLAUDE.md "생산라인에 자동으로 등록" 요구 충족). 또한 생산 현황 표기에 쓰일 **총생산시간**(= 평균 생산시간 × 실생산량)을 작업 등록 시점에 계산해 job에 보관한다.

## 배경 (CLAUDE.md 근거)

- 승인 시 재고가 부족한 경우 → 생산라인에 자동으로 등록, 주문 상태를 PRODUCING으로 전환
- 생산라인: 실생산량 = ceil(부족분 / 수율), 총생산시간 = 평균 생산시간 × 실생산량
- 생산 현황 표기: 현재 생산 중인 시료에 대한 정보 표기 (표기 수준 자율 결정, ex. 주문 정보, 현재까지의 생산량 등)

## 범위 (In Scope)

1. `ProductionJob`에 `actual_quantity`, `production_time` 필드 추가
   - `ProductionLine.enqueue()` 호출 시점에 즉시 계산·저장 (완료 전에도 "예상 정보"를 조회할 수 있어야 생산 현황 표기가 가능하므로)
   - `complete_next()`는 새로 계산하지 않고 저장된 `actual_quantity`를 재고에 반영 (기존 테스트 결과는 동일하게 유지)
2. `OrderRepository.approve(order_id, sample_repository, production_line=None)`
   - 기본값 `None`으로 하위 호환 유지 (기존 테스트 3건 변경 없이 통과)
   - 재고 부족으로 `PRODUCING` 전환이 발생하고 `production_line`이 주어진 경우, `shortfall = quantity - inventory`를 계산해 `production_line.enqueue(order, sample, shortfall)` 자동 호출
   - 재고 충분(CONFIRMED)이거나 `production_line`이 없으면 큐에 등록하지 않음

## 범위 밖 (Out of Scope)

- `complete_next()`를 자동으로 트리거하는 스케줄러/타이머 (실제 "생산 완료"는 콘솔에서 수동 명령으로 처리 — M7)
- 콘솔 출력 포맷("생산 현황", "대기 주문" 화면) → M7

## RED 대상 테스트

### `tests/model/test_production_line.py`에 추가

1. `test_enqueue_computes_actual_quantity_immediately`
   - `enqueue()` 직후(=`complete_next()` 호출 전) `job.actual_quantity`가 `ceil(shortfall / yield_rate)`로 이미 계산되어 있다.
2. `test_enqueue_computes_production_time_immediately`
   - `enqueue()` 직후 `job.production_time`이 `avg_production_time * actual_quantity`로 계산되어 있다.

### `tests/model/test_order_repository.py`에 추가

3. `test_approve_enqueues_job_to_production_line_when_insufficient`
   - 재고 부족 상태에서 `production_line`을 전달해 승인하면, `production_line.list_pending()`에 해당 주문의 작업이 (부족분과 함께) 등록된다.
4. `test_approve_does_not_enqueue_when_inventory_sufficient`
   - 재고 충분 상태에서 `production_line`을 전달해 승인해도 `production_line.list_pending()`은 비어 있다.

## 완료 조건 (Definition of Done)

- [ ] 위 4개 테스트가 RED(실패) 상태를 직접 확인한 뒤 RED 커밋 (`RED: approve-생산라인 자동 등록 실패하는 테스트 추가`)
- [ ] 최소한의 코드로 구현, 기존 21개 테스트 전부 그대로 통과 확인 (GREEN, 아직 커밋 안 함)
- [ ] 전체 테스트 통과, 출력 깨끗함
- [ ] `.claude/skills/clean-code/SKILL.md` 기준 셀프 리뷰 후 사람 파트너 REVIEW 승인
- [ ] GREEN 커밋 (`GREEN: approve-생산라인 자동 등록 구현 (리뷰 완료)`)

## 다음 사이클 예고

M4 완료. **plan_8.md**: M5 출고 처리 — CONFIRMED 주문에 대해 출고 실행 시 RELEASE 전환 (+ 재고 차감 여부 확정: CLAUDE.md상 출고는 이미 CONFIRMED 시점에 재고가 확보된 상태이므로 추가 차감이 필요한지 검토).
