# Plan 1 — M0: 프로젝트 뼈대 & Harness

## 목표

TDD 사이클(RED-GREEN-REVIEW)을 시작하기 위한 최소한의 프로젝트 구조와 테스트 실행 환경(Harness: pytest)을 갖춘다. 이 사이클은 도메인 동작(behavior)을 구현하는 것이 아니라 **설정(configuration) 성격**이므로, TDD 스킬의 예외 항목("설정 파일")에 해당한다 — RED/GREEN 테스트 사이클 없이 진행하고, 대신 사람 파트너 리뷰를 거쳐 커밋한다.

## 범위 (In Scope)

1. 패키지 구조 생성

   ```text
   SampleOrderSystem/
     src/
       model/         # 도메인 로직 (Sample, Order, ProductionLine 등) — 순수 파이썬, 콘솔 의존성 없음
       view/          # 콘솔 입출력 전담
       controller/    # model-view 연결, 메뉴 흐름 제어
     tests/           # pytest 테스트
     PRD.md
     pytest.ini (또는 pyproject.toml [tool.pytest])
   ```

2. `pytest` 실행 환경 구성
   - `pytest.ini`: `testpaths = tests`, `pythonpath` 설정으로 `src` 임포트 가능하게 함
   - 더미 테스트 1개(`tests/test_smoke.py`)로 하네스 자체가 정상 동작하는지만 확인 (`assert True` 수준, 도메인 로직 아님)
3. `PRD.md` 작성
   - 제품 목표, 사용자(주문 담당자/생산 담당자), 핵심 시나리오(주문 접수→승인→생산→출고), 완료 기준(Definition of Done: 6개 기능 명세 전부 동작 + 테스트 그린)
   - 수율(yield) 규칙을 구체 예시로 명시 (아래 참고)
4. `__init__.py` 등 패키지 초기 파일

### 수율(Yield) 규칙 예시 — PRD.md에 포함할 내용

- 수율 80% 시료에 주문 16개가 들어오고 재고가 0이라 부족분이 16개인 경우:
  - 실생산량 = ceil(부족분 / 수율) = ceil(16 / 0.8) = **20개**
  - 생산은 20개 단위로 진행되며, 20개가 **전부 완성되어야** 생산 완료로 처리된다 (부분 완료 없음)
  - 생산 완료 시 재고에 생산량 20개가 그대로 반영된다
  - 해당 주문은 16개만 소비하고 CONFIRMED로 전환되며, 나머지 **4개는 잉여 재고로 남는다**
  - 즉 수율은 "생산량 대비 실제 주문 충족량의 비율"이며, 남는 초과분은 폐기되지 않고 다음 주문을 위한 재고로 누적된다 (실제 반도체 공정의 수율/불량 개념이 아니라, 본 시스템에서의 단순화된 규칙)

## 범위 밖 (Out of Scope) — 다음 사이클로

- Sample/Order 등 실제 도메인 클래스 구현 → **plan_2.md**부터 정식 RED-GREEN 사이클로 진행
- 콘솔 메뉴 UI 구현 → M7에서 진행

## 완료 조건 (Definition of Done)

- [ ] `pytest` 명령이 프로젝트 루트에서 정상 실행되고 smoke 테스트가 통과한다
- [ ] `src/model`, `src/view`, `src/controller`, `tests` 폴더 및 `__init__.py` 존재
- [ ] `PRD.md` 작성 완료
- [ ] 사람 파트너 리뷰 승인 후 단일 커밋 (`SETUP: 프로젝트 뼈대 및 pytest 하네스 구성`)

## 다음 사이클 예고

**plan_2.md**: M1 시료 관리 — "시료를 등록하면 시료 목록 조회 시 나타난다"를 첫 RED 테스트로 시작.
