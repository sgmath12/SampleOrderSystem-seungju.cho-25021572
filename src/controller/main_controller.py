class MainController:
    def __init__(self, view, sample_controller, order_controller, production_controller, monitoring_controller):
        self.view = view
        self.sample_controller = sample_controller
        self.order_controller = order_controller
        self.production_controller = production_controller
        self.monitoring_controller = monitoring_controller

    def run(self):
        top_level_actions = {
            "1": self._run_sample_menu,
            "2": self.order_controller.place_order,
            "3": self.order_controller.review_order,
            "4": self._run_monitoring_menu,
            "5": self._run_production_menu,
            "6": self.order_controller.release_order,
        }
        while True:
            summary = self.monitoring_controller.system_summary()
            summary["pending_production"] = self.production_controller.count_pending()
            self.view.show_main_menu(summary)
            choice = self.view.read_menu_choice()
            if choice == "0":
                self.view.show_message("종료합니다.")
                break
            action = top_level_actions.get(choice)
            if action is None:
                self.view.show_message("잘못된 선택입니다.")
                continue
            self._safe_call(action)

    def _safe_call(self, action):
        try:
            action()
        except ValueError as error:
            self.view.show_message(f"오류: {error}")

    def _run_sample_menu(self):
        actions = {
            "1": self.sample_controller.register_sample,
            "2": self.sample_controller.list_samples,
            "3": self.sample_controller.search_samples,
        }
        while True:
            self.view.show_sample_menu()
            choice = self.view.read_menu_choice()
            if choice == "0":
                break
            action = actions.get(choice)
            if action is None:
                self.view.show_message("잘못된 선택입니다.")
                continue
            self._safe_call(action)

    def _run_monitoring_menu(self):
        self.monitoring_controller.show_order_counts()
        self.monitoring_controller.show_inventory_status()

    def _run_production_menu(self):
        self.production_controller.show_pending()
        self.view.show_message("[1] 생산 완료 처리  [0] 뒤로가기")
        choice = self.view.read_menu_choice()
        if choice == "1":
            self._safe_call(self.production_controller.complete_next)
