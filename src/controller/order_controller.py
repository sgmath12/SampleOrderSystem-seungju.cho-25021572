class OrderController:
    def __init__(self, order_repository, sample_repository, production_line, view):
        self.order_repository = order_repository
        self.sample_repository = sample_repository
        self.production_line = production_line
        self.view = view

    def place_order(self):
        samples = self.sample_repository.list_all()
        if not samples:
            self.view.show_message("등록된 시료가 없습니다. 먼저 시료를 등록해주세요.")
            return
        self.view.show_message("[주문 가능한 시료 목록]")
        self.view.show_samples(samples)
        sample_id, customer, quantity = self.view.read_order_placement()
        order = self.order_repository.create(self.sample_repository, sample_id, customer, quantity)
        self.view.show_message(f"주문 접수 완료: {order.order_id}")

    def review_order(self):
        order = self._select_order(
            self.order_repository.list_reserved(),
            "승인 대기 중인 주문이 없습니다.",
            "[승인/거절 대기 중인 주문 목록입니다. 처리할 주문 번호를 선택해주세요.]",
        )
        if order is None:
            return
        self.view.show_message("[1] 승인   [2] 거절   [0] 취소")
        decision = self.view.read_menu_choice()
        if decision == "1":
            self.order_repository.approve(order.order_id, self.sample_repository, self.production_line)
            self.view.show_message(f"주문 승인 처리 완료: {order.order_id}")
        elif decision == "2":
            self.order_repository.reject(order.order_id)
            self.view.show_message(f"주문 거절 완료: {order.order_id}")

    def release_order(self):
        order = self._select_order(
            self.order_repository.list_confirmed(),
            "출고 가능한 주문이 없습니다.",
            "[출고 가능한 주문 목록(CONFIRMED)입니다. 출고할 주문 번호를 선택해주세요.]",
        )
        if order is None:
            return
        self.order_repository.release(order.order_id)
        self.view.show_release_confirmation(order)

    def _select_order(self, candidates, empty_message, list_message):
        if not candidates:
            self.view.show_message(empty_message)
            return None
        self.view.show_message(list_message)
        index = self.view.select_order_number(candidates)
        if index is None or not (1 <= index <= len(candidates)):
            self.view.show_message("잘못된 번호입니다.")
            return None
        return candidates[index - 1]
