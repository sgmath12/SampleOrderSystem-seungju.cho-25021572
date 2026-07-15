# Plan 9 — M5: 출고 처리

## 목표

`CONFIRMED` 상태의 주문에 대해 출고를 실행하면 `RELEASE`로 전환한다.

## 배경 (CLAUDE.md 근거)

- 재고가 충분해진 CONFIRMED 주문에 대해 출고를 처리
- 특정 주문에 대해 출고를 실행
- 주문 상태가 RELEASE로 전환

## 재고 처리 여부 확인 (plan_7 예고에서 이어짐)

`approve()`(재고 충분)와 `ProductionLine.complete_next()`(생산 완료) 두 경로 모두, `CONFIRMED`로 전환되는 시점에 이미 해당 주문의 수량만큼 재고가 소비 완료된 상태다 (재고 충분 경로: `sample.inventory -= order.quantity`, 생산 경로: 부족분은 예약 시 소진, 잉여만 재고에 반영). 즉 **출고 처리 시점에는 재고를 추가로 차감하지 않는다** — 순수 상태 전환(`CONFIRMED` → `RELEASE`)만 수행한다.

## 범위 (In Scope)

- `OrderRepository.release(order_id)`
  - 주문이 `CONFIRMED` 상태면 `RELEASE`로 전환
  - `CONFIRMED`가 아니면 `ValueError` 발생 (예: `RESERVED`/`PRODUCING`/`REJECTED` 상태인 주문은 출고 불가)

## 범위 밖

- 재고 재차감 로직 (위에서 확인했듯 불필요)
- 콘솔 View/Controller 연결 → M7

## RED 대상 테스트

파일: `tests/model/test_order_repository.py`에 추가

1. `test_release_sets_status_to_release_when_confirmed`
2. `test_release_raises_when_order_not_confirmed`
   - `RESERVED` 상태인 주문을 출고 처리하려 하면 `ValueError`가 발생한다.

## 완료 조건 (Definition of Done)

- [ ] 위 2개 테스트가 RED(실패) 상태를 직접 확인한 뒤 RED 커밋 (`RED: 출고 처리 실패하는 테스트 추가`)
- [ ] `release()`를 테스트 통과시키는 최소한의 코드로 구현 (GREEN, 아직 커밋 안 함)
- [ ] 전체 테스트 통과, 출력 깨끗함
- [ ] `.claude/skills/clean-code/SKILL.md` 기준 셀프 리뷰 후 사람 파트너 REVIEW 승인
- [ ] GREEN 커밋 (`GREEN: 출고 처리 구현 (리뷰 완료)`)

## 다음 사이클 예고

**plan_10.md**: M6 모니터링 — 상태별 주문 수 집계(REJECTED 제외), 시료별 재고 현황(여유/부족/고갈) 판정.
