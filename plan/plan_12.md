# Plan 12 — M7: 콘솔 UI 통합 (나머지 전체 화면 한 번에)

plan_11에서 분리했던 나머지 화면(시료 주문 접수 / 주문 승인·거절 / 생산라인 조회 / 출고 처리 / 모니터링)을 한 사이클로 묶어 진행한다.

## 목표

이미 완성된 도메인 로직(Order, ProductionLine, monitoring 함수들)을 메인 메뉴에 전부 연결해 M7(콘솔 UI 통합)을 마무리한다.

## 배경 (CLAUDE.md 근거)

메인 메뉴: 시료 관리(완료) / 주문(접수·승인·거절) / 모니터링 / 출고 처리 / 생산라인

## 테스트 전략

plan_11과 동일 — Controller 오케스트레이션은 Fake View로 pytest 검증, 실제 콘솔 I/O(`main.py` 전체 실행)는 사이클 마지막에 한 번의 종단(end-to-end) 수동 스모크 테스트로 확인.

## 범위 (In Scope)

- 공유 상태: `main.py`에서 `SampleRepository`, `OrderRepository`, `ProductionLine`을 한 번씩 생성해 모든 Controller가 공유
- `src/controller/order_controller.py` — `OrderController`
  - `place_order()` — 시료ID/고객명/수량 입력받아 `OrderRepository.create()` 호출 (RESERVED)
  - `list_reserved_orders()` — `list_reserved()` 결과를 view로 출력
  - `approve_order()` — 주문ID 입력받아 `OrderRepository.approve(order_id, sample_repository, production_line)` 호출
  - `reject_order()` — 주문ID 입력받아 `reject()` 호출
  - `release_order()` — 주문ID 입력받아 `release()` 호출
- `src/controller/production_controller.py` — `ProductionController`
  - `show_pending()` — `ProductionLine.list_pending()` 결과를 view로 출력 (각 job의 order/실생산량/총생산시간)
  - `complete_next()` — `ProductionLine.complete_next()` 호출
- `src/controller/monitoring_controller.py` — `MonitoringController`
  - `show_order_counts()` — `count_orders_by_status(order_repository.list_all())` 결과를 view로 출력
  - `show_inventory_status()` — 등록된 시료마다 `reserved_quantity_for_sample` + `inventory_status`를 계산해 view로 출력
- `src/view/console_view.py`에 위 기능들을 위한 View 메서드 추가 (`OrderView`/`ProductionView`/`MonitoringView` 또는 기존 파일에 클래스 추가 — 구현 시 자연스러운 쪽으로 결정)
- `MainController`에 메뉴 `[2] 시료 주문`, `[3] 주문 승인/거절`, `[4] 모니터링`, `[5] 생산라인`, `[6] 출고 처리` 추가 연결

## 범위 밖

- 실시간/자동 생산 완료 트리거 (콘솔에서 수동으로 "생산 완료 처리" 선택 시에만 `complete_next()` 실행)
- 여러 생산라인 (요구사항상 단일 라인)

## RED 대상 테스트

파일: `tests/controller/test_order_controller.py`, `tests/controller/test_production_controller.py`, `tests/controller/test_monitoring_controller.py` (신규, 각각 Fake View 사용)

1. `test_place_order_creates_reserved_order`
2. `test_approve_order_delegates_to_order_repository`
3. `test_reject_order_delegates_to_order_repository`
4. `test_release_order_delegates_to_order_repository`
5. `test_show_pending_displays_queued_jobs`
6. `test_complete_next_advances_production_queue`
7. `test_show_order_counts_displays_status_counts`
8. `test_show_inventory_status_displays_per_sample_status`

## 완료 조건 (Definition of Done)

- [ ] 위 8개 테스트가 RED(실패) 상태를 직접 확인한 뒤 RED 커밋 (`RED: 나머지 콘솔 화면 실패하는 테스트 추가`)
- [ ] 모든 Controller/View/main.py 연결을 테스트 통과시키는 최소한의 코드로 구현 (GREEN, 아직 커밋 안 함)
- [ ] 전체 pytest 통과, 출력 깨끗함
- [ ] `python main.py`로 **전체 시나리오 종단 수동 스모크 테스트**: 시료 등록 → 주문 접수 → 승인(재고부족 유도) → 생산라인 조회 → 생산 완료 처리 → 출고 처리 → 모니터링 확인
- [ ] `.claude/skills/clean-code/SKILL.md` 기준 셀프 리뷰 후 사람 파트너 REVIEW 승인
- [ ] GREEN 커밋 (`GREEN: 나머지 콘솔 화면 구현 (리뷰 완료)`)

## 다음 사이클 예고

M7 완료. **plan_13.md**: M8 마무리 — 전체 테스트/Clean Code 리뷰, README 작성.
