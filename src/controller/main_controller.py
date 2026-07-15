class MainController:
    def __init__(self, view, sample_controller):
        self.view = view
        self.sample_controller = sample_controller

    def run(self):
        while True:
            self.view.show_main_menu()
            choice = self.view.read_menu_choice()
            if choice == "0":
                self.view.show_message("종료합니다.")
                break
            if choice == "1":
                self._run_sample_menu()
            else:
                self.view.show_message("잘못된 선택입니다.")

    def _run_sample_menu(self):
        actions = {
            "1": self.sample_controller.register_sample,
            "2": self.sample_controller.list_samples,
            "3": self.sample_controller.search_samples,
        }
        while True:
            self.view.show_sample_menu()
            choice = self.view.read_sample_menu_choice()
            if choice == "0":
                break
            action = actions.get(choice)
            if action is None:
                self.view.show_message("잘못된 선택입니다.")
                continue
            action()
