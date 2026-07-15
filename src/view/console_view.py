class SampleView:
    def show_main_menu(self):
        print("\n===== 반도체 시료 생산주문관리 시스템 =====")
        print("[1] 시료 관리")
        print("[0] 종료")

    def read_menu_choice(self):
        return input("선택 > ").strip()

    def show_sample_menu(self):
        print("\n----- 시료 관리 -----")
        print("[1] 시료 등록")
        print("[2] 시료 조회")
        print("[3] 시료 검색")
        print("[0] 뒤로가기")

    def read_sample_menu_choice(self):
        return input("선택 > ").strip()

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
