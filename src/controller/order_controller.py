class OrderController:
    def __init__(self, order_repository, sample_repository, production_line, view):
        self.order_repository = order_repository
        self.sample_repository = sample_repository
        self.production_line = production_line
        self.view = view

    def place_order(self):
        sample_id, customer, quantity = self.view.read_order_placement()
        order = self.order_repository.create(self.sample_repository, sample_id, customer, quantity)
        self.view.show_message(f"주문 접수 완료: {order.order_id}")

    def approve_order(self):
        order = self._select_order(self.order_repository.list_reserved(), "승인 대기 중인 주문이 없습니다.")
        if order is None:
            return
        self.order_repository.approve(order.order_id, self.sample_repository, self.production_line)
        self.view.show_message(f"주문 승인 처리 완료: {order.order_id}")

    def reject_order(self):
        order = self._select_order(self.order_repository.list_reserved(), "승인 대기 중인 주문이 없습니다.")
        if order is None:
            return
        self.order_repository.reject(order.order_id)
        self.view.show_message(f"주문 거절 완료: {order.order_id}")

    def release_order(self):
        order = self._select_order(self.order_repository.list_confirmed(), "출고 가능한 주문이 없습니다.")
        if order is None:
            return
        self.order_repository.release(order.order_id)
        self.view.show_release_confirmation(order)

    def _select_order(self, candidates, empty_message):
        if not candidates:
            self.view.show_message(empty_message)
            return None
        self.view.show_orders_numbered(candidates)
        index = self.view.read_selection_number()
        if not (1 <= index <= len(candidates)):
            self.view.show_message("잘못된 번호입니다.")
            return None
        return candidates[index - 1]
