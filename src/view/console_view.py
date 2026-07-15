from view.colors import pad_badge

TITLE = "반도체 시료 생산주문관리 시스템"


def _display_width(text):
    return sum(2 if ord(ch) > 0x1100 else 1 for ch in text)


def _center(text, width):
    padding = max(0, width - _display_width(text))
    left = padding // 2
    right = padding - left
    return " " * left + text + " " * right


class ConsoleView:
    def show_main_menu(self):
        width = _display_width(TITLE) + 4
        print("\n┌" + "─" * width + "┐")
        print("│" + _center(TITLE, width) + "│")
        print("└" + "─" * width + "┘")
        print("[1] 시료 관리")
        print("[2] 시료 주문")
        print("[3] 주문 승인/거절")
        print("[4] 모니터링")
        print("[5] 생산라인")
        print("[6] 출고 처리")
        print("[0] 종료")

    def read_menu_choice(self):
        return input("선택 > ").strip()

    def show_sample_menu(self):
        print("\n----- 시료 관리 -----")
        print("[1] 시료 등록")
        print("[2] 시료 조회")
        print("[3] 시료 검색")
        print("[0] 뒤로가기")

    def read_sample_registration(self):
        sample_id = input("시료 ID > ").strip()
        name = input("이름 > ").strip()
        avg_production_time = int(input("평균 생산시간 > ").strip())
        yield_rate = float(input("수율 > ").strip())
        return sample_id, name, avg_production_time, yield_rate

    def read_search_keyword(self):
        return input("검색어(이름) > ").strip()

    def show_samples(self, samples):
        if not samples:
            print("표시할 시료가 없습니다.")
            return
        print(f"{'ID':<8}{'이름':<20}{'평균생산시간':<14}{'수율':<8}{'재고':<8}")
        for sample in samples:
            print(
                f"{sample.sample_id:<8}{sample.name:<20}{sample.avg_production_time:<14}"
                f"{sample.yield_rate:<8}{sample.inventory:<8}"
            )

    def show_message(self, message):
        print(message)

    # ----- 시료 주문 / 승인 / 거절 / 출고 -----

    def read_order_placement(self):
        sample_id = input("시료 ID > ").strip()
        customer = input("고객명 > ").strip()
        quantity = int(input("주문 수량 > ").strip())
        return sample_id, customer, quantity

    def read_order_id(self):
        return int(input("주문 ID > ").strip())

    def show_orders(self, orders):
        if not orders:
            print("표시할 주문이 없습니다.")
            return
        print(f"{'ID':<6}{'시료ID':<10}{'고객명':<15}{'수량':<8}{'상태':<12}")
        for order in orders:
            print(
                f"{order.order_id:<6}{order.sample_id:<10}{order.customer:<15}"
                f"{order.quantity:<8}{pad_badge(order.status, 12)}"
            )

    # ----- 생산라인 -----

    def show_production_jobs(self, jobs):
        if not jobs:
            print("대기 중인 생산 작업이 없습니다.")
            return
        print(f"{'주문ID':<8}{'시료ID':<10}{'부족분':<8}{'실생산량':<10}{'총생산시간':<10}")
        for job in jobs:
            print(
                f"{job.order.order_id:<8}{job.sample.sample_id:<10}{job.shortfall:<8}"
                f"{job.actual_quantity:<10}{job.production_time:<10}"
            )

    # ----- 모니터링 -----

    def show_order_counts(self, counts):
        if not counts:
            print("집계할 주문이 없습니다.")
            return
        for status, count in counts.items():
            print(f"{pad_badge(status, 12)}{count}건")

    def show_inventory_status(self, statuses):
        if not statuses:
            print("등록된 시료가 없습니다.")
            return
        print(f"{'시료ID':<10}{'이름':<20}{'재고':<8}{'상태':<8}")
        for sample, status in statuses:
            print(f"{sample.sample_id:<10}{sample.name:<20}{sample.inventory:<8}{pad_badge(status, 8)}")
