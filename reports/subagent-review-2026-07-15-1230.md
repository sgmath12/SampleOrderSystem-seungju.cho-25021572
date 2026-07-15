# Subagent Review Report — 2026-07-15

doc-checker(문서-코드 정합성)와 bug-hunter(엣지케이스/로직 모순) 역할의 서브에이전트를 병렬로 실행해 얻은 결과 요약. 두 에이전트 모두 읽기 전용으로 실행했으며 코드/문서는 수정하지 않았다.

## doc-checker 리포트

1. **(중요) PRD.md 수율 예시 서술이 실제 구현 메커니즘과 어긋남**
   - PRD.md는 "재고 0 → 20(생산량 전체 반영) → 주문 16 소비 → 잉여 4"라는 2단계 서술을 하지만, 실제 코드는 `approve()`에서 기존 재고를 이미 0으로 선(先)소진(예약)시키고, `complete_next()`는 잉여(`actual_quantity - shortfall` = 4)만 더한다. 최종 숫자(4)는 같지만 과정 서술이 실제 코드 흐름과 다르다.
   - `plan_8.md`에서 이 계산 방식 자체는 이미 고쳤지만, `PRD.md` 문서 서술은 갱신되지 않은 것으로 보인다.
2. **(확신도 낮음) `docs/설명.md`의 "여러 주문이 하나의 생산 배치를 공유"하는 뉘앙스**가 실제로는 주문마다 독립된 `ProductionJob`을 각자 생산하는 구현과 다르다. 이게 필수 요구사항인지 수율 개념을 설명하기 위한 예시인지 경계가 모호해 PLAUSIBLE 수준으로 분류.
3. **(경미)** PRD.md의 "완료 기준(Definition of Done)" 체크박스가 실제로는 구현이 끝났음에도 전부 미체크(`[ ]`) 상태로 남아있음.
4. 상태 전이, FIFO 큐, 실생산량/총생산시간 공식, 모니터링 여유/부족/고갈 판정 등은 문서와 코드가 정확히 일치함을 확인.

## bug-hunter 리포트

1. **[치명적] 음수/0 주문 수량 검증 누락** — `OrderRepository.create()`가 `quantity`에 대해 어떤 검증도 하지 않아, 음수 수량으로 주문 후 승인하면 `sample.inventory -= (음수)`가 되어 **재고가 오히려 증가**하는 데이터 무결성 훼손이 발생.
2. **[치명적] `approve()`/`reject()`에 상태 가드 부재** — `release()`에는 `CONFIRMED`만 허용하는 가드가 있지만 `approve()`/`reject()`에는 대칭적인 가드가 없어, 이미 `CONFIRMED`/`RELEASE`/`REJECTED`인 주문을 다시 승인/거절하면 재고 이중 차감이나 잘못된 상태 역행이 가능함.
3. **[치명적] 수율(yield_rate) 값 검증 누락** — 시료 등록 시 `yield_rate=0`(또는 음수, 1 초과)을 그대로 허용해, 해당 시료가 생산라인에 들어가면 `production_line.py`에서 `shortfall / yield_rate`가 0으로 나누어져 `ZeroDivisionError`로 콘솔 앱 전체가 크래시됨.
4. **[중간] 존재하지 않는 order_id 처리 누락** — `OrderRepository._find_by_id()`가 `next()`를 기본값 없이 사용해, 없는 ID로 승인/거절/출고를 시도하면 `StopIteration`이 발생하고 Controller/MainController 어디에서도 잡지 않아 앱이 종료됨.
5. **[중간] 생산 큐가 빈 상태에서 "생산 완료 처리" 실행 시 크래시** — `ProductionLine.complete_next()`가 빈 큐에서 `popleft()`를 호출해 `IndexError` 발생, 역시 잡히지 않고 전파됨.
6. **[경미~중간] 콘솔 숫자 입력 파싱 실패 시 크래시** — `int()`/`float()` 파싱을 try/except 없이 사용해 잘못된 입력(숫자가 아닌 문자열 등) 시 `ValueError`로 앱이 죽음.
7. FIFO 큐 순서 보장, `inventory_status`의 경계값(`inventory == reserved_quantity`) 처리 등은 테스트로 이미 검증되어 있어 문제없음으로 확인.

## 다음 조치

1~5번(치명적/중간 등급)을 우선순위로 TDD Red-Green-Review 사이클로 수정한다. 6번(입력 파싱 크래시)은 도메인 예외를 잡아 메시지로 보여주는 콘솔 레벨 방어 로직으로 함께 완화한다. doc-checker의 1번(PRD.md 서술 갱신)은 별도로 문서만 수정한다.
