# Plan 11 — M7: 콘솔 UI 통합 (메인 메뉴 뼈대 + 시료 관리 화면)

M7은 화면이 6개(시료 관리/주문/승인거절/모니터링/생산라인/출고)라 한 사이클에 다 넣지 않는다. 이번 사이클은 **메인 메뉴 뼈대**와 **시료 관리 화면**(등록/조회/검색)만 연결한다.

## 목표

`ConsoleMVC` POC의 Model/View/Controller 역할 분리를 참고해, 이미 완성된 `SampleRepository`(M1)를 실제 콘솔 메뉴에 연결한다.

## 배경 (CLAUDE.md 근거)

- 메인 메뉴: 기능별 선택 화면 표시, 화면 구성 자유
- 시료 관리: 시료 등록(시료ID/이름/평균생산시간/수율), 시료 조회(재고 포함), 시료 검색(이름)

## 테스트 전략 — View/Controller 경계

TDD 스킬의 "mock은 외부 경계에서만" 원칙에 따라, `input()`/`print()` 자체(진짜 콘솔 I/O)는 외부 경계로 보고 pytest로 자동 검증하지 않는다. 대신:

- **Controller의 라우팅/오케스트레이션 로직**은 실제 `SampleRepository`와, 테스트용 **Fake View**(진짜 콘솔이 아닌 미리 정해둔 응답을 반환하는 단순 테스트 더블)를 사용해 pytest로 검증한다.
- **실제 콘솔 입출력(ConsoleView, main.py 실행)**은 자동화된 테스트 없이, 이번 사이클 완료 후 `python main.py`를 직접 실행해 수동으로 스모크 테스트한다 (ConsoleMVC POC 검증 방식과 동일).

## 범위 (In Scope)

- `src/view/console_view.py` — `SampleView`
  - `show_main_menu()` / `read_menu_choice()`
  - `show_sample_menu()` / `read_sample_menu_choice()`
  - `read_sample_registration()` → (sample_id, name, avg_production_time, yield_rate) 입력받기
  - `read_search_keyword()`
  - `show_samples(samples)` — 목록/조회/검색 결과 출력 (재고 포함)
  - `show_message(message)`
- `src/controller/sample_controller.py` — `SampleController`
  - `run_sample_menu()`: 등록/조회/검색/뒤로가기 라우팅
    - 등록: view로 입력받아 `SampleRepository.register()` 호출
    - 조회: `SampleRepository.list_all()` 결과를 view로 출력
    - 검색: `SampleRepository.search_by_name()` 결과를 view로 출력
- `src/controller/main_controller.py` — 메인 메뉴 뼈대: `[1] 시료 관리`, `[0] 종료`만 우선 연결 (다른 메뉴는 다음 사이클에서 추가)
- `main.py` — 진입점, `SampleRepository` 등 공유 상태 생성 후 `MainController` 실행

## 범위 밖 — 다음 사이클로

- 시료 주문/승인거절/모니터링/생산라인/출고 화면 → plan_12~14
- 여러 저장소(Order/ProductionLine 등)를 아우르는 공유 애플리케이션 상태 설계 확정 → 다음 사이클에서 메뉴 추가하며 함께 확장

## RED 대상 테스트

파일: `tests/controller/test_sample_controller.py` (신규, Fake View 사용)

1. `test_register_reads_input_and_registers_sample`
   - Fake View가 미리 정해둔 등록 입력을 반환하면, `SampleController`가 `SampleRepository`에 해당 시료를 등록한다.
2. `test_list_shows_all_registered_samples`
   - 등록된 시료들이 있을 때 조회 메뉴를 실행하면 Fake View의 `show_samples`가 전체 목록으로 호출된다.
3. `test_search_shows_matching_samples`
   - 검색 키워드를 입력하면 `SampleRepository.search_by_name()` 결과가 Fake View로 전달된다.

## 완료 조건 (Definition of Done)

- [ ] 위 3개 테스트가 RED(실패) 상태를 직접 확인한 뒤 RED 커밋 (`RED: 시료 관리 콘솔 연결 실패하는 테스트 추가`)
- [ ] `SampleView`, `SampleController`, `MainController`, `main.py`를 테스트 통과시키는 최소한의 코드로 구현 (GREEN, 아직 커밋 안 함)
- [ ] 전체 pytest 통과, 출력 깨끗함
- [ ] `python main.py` 수동 실행으로 실제 콘솔에서 시료 등록 → 조회 → 검색이 정상 동작함을 확인 (스모크 테스트, 결과를 리뷰 시 공유)
- [ ] `.claude/skills/clean-code/SKILL.md` 기준 셀프 리뷰 후 사람 파트너 REVIEW 승인
- [ ] GREEN 커밋 (`GREEN: 시료 관리 콘솔 연결 구현 (리뷰 완료)`)

## 다음 사이클 예고

**plan_12.md**: 시료 주문 접수 + 주문 승인/거절 화면을 메인 메뉴에 추가 연결.
