import time
from datetime import datetime

from model.production_line import estimated_completion_at, progress_percent
from view.colors import pad_badge

TITLE = "반도체 시료 생산주문관리 시스템"

LOGO = r"""
  ____        ____                  _
 / ___|      / ___|  ___ _ __ ___  (_)
 \___ \ ___  \___ \ / _ \ '_ ` _ \ | |
  ___) |___|  ___) |  __/ | | | | || |
 |____/     |____/ \___|_| |_| |_|/ |
                                 |__/
"""


def _display_width(text):
    return sum(2 if ord(ch) > 0x1100 else 1 for ch in text)


def _center(text, width):
    padding = max(0, width - _display_width(text))
    left = padding // 2
    right = padding - left
    return " " * left + text + " " * right


class ConsoleView:
    def show_main_menu(self, summary):
        width = _display_width(TITLE) + 4
        print(LOGO)
        print("┌" + "─" * width + "┐")
        print("│" + _center(TITLE, width) + "│")
        print("└" + "─" * width + "┘")
        print(f"시스템 현황  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(
            f"등록 시료 {summary['sample_count']}종   총 재고 {summary['total_inventory']:,} ea   "
            f"전체 주문 {summary['order_count']}건   생산라인 {summary['pending_production']}건 대기"
        )
        print("-" * width)
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

    def show_orders_numbered(self, orders):
        print(f"{'번호':<6}{'주문번호':<20}{'고객명':<15}{'시료ID':<10}{'수량':<8}{'상태':<12}")
        for index, order in enumerate(orders, start=1):
            print(
                f"[{index}]{'':<3}{order.order_id:<20}{order.customer:<15}{order.sample_id:<10}"
                f"{order.quantity:<8}{pad_badge(order.status, 12)}"
            )

    def read_selection_number(self):
        return int(input("번호 > ").strip())

    def show_release_confirmation(self, order):
        print("\n출고 처리 완료.\n")
        print(f"주문번호   {order.order_id}")
        print(f"출고수량   {order.quantity} ea")
        print(f"처리일시   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"상태       CONFIRMED → {pad_badge('RELEASE', 0)}")

    # ----- 생산라인 -----

    def show_production_jobs(self, jobs):
        if not jobs:
            print("대기 중인 생산 작업이 없습니다.")
            return

        now = time.time()
        current = jobs[0]
        percent = progress_percent(current, now)
        bar_width = 20
        filled = int(bar_width * percent / 100)
        bar = "█" * filled + "░" * (bar_width - filled)
        eta = datetime.fromtimestamp(estimated_completion_at(current)).strftime("%H:%M")

        print("\n----- 현재 처리 중 -----")
        print(f"주문번호 {current.order.order_id}   시료 {current.sample.name}")
        print(
            f"주문량 {current.order.quantity}ea   부족 {current.shortfall}ea   "
            f"실생산량 {current.actual_quantity}ea (수율 {current.sample.yield_rate} / {current.production_time:.0f}min)"
        )
        print(f"진행 {bar} {percent:.0f}%   완료 예정 {eta}")

        waiting = jobs[1:]
        if waiting:
            print("\n----- 대기 중인 주문 (FIFO 순) -----")
            print(f"{'순서':<6}{'주문번호':<20}{'시료ID':<10}{'주문량':<8}{'부족분':<8}{'실생산량':<10}{'예상완료':<8}")
            for order_index, job in enumerate(waiting, start=1):
                job_eta = datetime.fromtimestamp(estimated_completion_at(job)).strftime("%H:%M")
                print(
                    f"{order_index:<6}{job.order.order_id:<20}{job.sample.sample_id:<10}"
                    f"{job.order.quantity:<8}{job.shortfall:<8}{job.actual_quantity:<10}{job_eta:<8}"
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
