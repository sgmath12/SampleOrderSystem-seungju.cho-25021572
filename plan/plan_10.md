# Plan 10 — M6: 모니터링

## 목표

상태별 주문 수 집계와 시료별 재고 현황(여유/부족/고갈) 판정 로직을 순수 함수로 구현한다.

## 배경 (CLAUDE.md 근거)

- 주문량 확인: 현재 상태별(RESERVED/CONFIRMED/PRODUCING/RELEASE) 목록을 확인. REJECTED는 유효한 주문이 아니므로 무시.
- 재고량 확인: 각 시료별 현재 재고 수량을 확인. 주문 대비 재고 수량에 따라 상태도 표기
  - 여유: 주문 대비 재고 충분
  - 부족: 주문 대비 재고 수량 부족
  - 고갈: 수량이 0인 상태

## 설계 결정 — "주문 대비"의 기준

CLAUDE.md는 "주문 대비 재고"라고만 되어 있어, 비교 기준을 명확히 할 필요가 있다. 아직 **승인 대기 중(RESERVED)인 주문들의 수량 합**을 그 시료에 대한 수요로 보고, 현재 재고와 비교한다 (승인된 주문은 이미 approve() 시점에 재고에서 처리·예약이 끝난 상태이므로 모니터링 시점의 "대비" 대상에서 제외).

## 범위 (In Scope)

신규 모듈 `src/model/monitoring.py`, 순수 함수 3개:

- `count_orders_by_status(orders)` — 상태별 주문 수 집계 딕셔너리 반환. `REJECTED`는 집계에서 제외.
- `reserved_quantity_for_sample(orders, sample_id)` — 특정 시료에 대한 `RESERVED` 주문들의 수량 합.
- `inventory_status(inventory, reserved_quantity)` — 재고 상태 문자열 반환
  - `inventory == 0` → `"고갈"`
  - `0 < inventory < reserved_quantity` → `"부족"`
  - 그 외 (`inventory >= reserved_quantity`) → `"여유"`

## 범위 밖

- `SampleRepository`/`OrderRepository`를 직접 조회해 리포트를 조립하는 조합 함수 — 콘솔 출력과 함께 M7에서 View/Controller가 이 순수 함수들을 사용해 조립
- 콘솔 출력 포맷 → M7

## RED 대상 테스트

파일: `tests/model/test_monitoring.py` (신규)

1. `test_count_orders_by_status_excludes_rejected`
2. `test_count_orders_by_status_counts_each_status`
3. `test_reserved_quantity_for_sample_sums_matching_reserved_orders`
   - 같은 시료의 `RESERVED` 주문 수량만 합산하고, 다른 시료·다른 상태 주문은 제외한다.
4. `test_inventory_status_is_exhausted_when_zero`
5. `test_inventory_status_is_short_when_less_than_reserved`
6. `test_inventory_status_is_sufficient_when_greater_or_equal`

## 완료 조건 (Definition of Done)

- [ ] 위 6개 테스트가 RED(실패) 상태를 직접 확인한 뒤 RED 커밋 (`RED: 모니터링 집계 실패하는 테스트 추가`)
- [ ] `monitoring.py`를 테스트 통과시키는 최소한의 코드로 구현 (GREEN, 아직 커밋 안 함)
- [ ] 전체 테스트 통과, 출력 깨끗함
- [ ] `.claude/skills/clean-code/SKILL.md` 기준 셀프 리뷰 후 사람 파트너 REVIEW 승인
- [ ] GREEN 커밋 (`GREEN: 모니터링 집계 구현 (리뷰 완료)`)

## 다음 사이클 예고

M1~M6 도메인 로직 전부 완료. **plan_11.md**부터는 M7 콘솔 UI 통합 — ConsoleMVC POC 구조(model/view/controller)를 참고해 메인 메뉴와 각 화면을 실제 콘솔에 연결.
