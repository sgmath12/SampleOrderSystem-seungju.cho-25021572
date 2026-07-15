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

    def list_reserved_orders(self):
        self.view.show_orders(self.order_repository.list_reserved())

    def approve_order(self):
        order_id = self.view.read_order_id()
        self.order_repository.approve(order_id, self.sample_repository, self.production_line)
        self.view.show_message(f"주문 승인 처리 완료: {order_id}")

    def reject_order(self):
        order_id = self.view.read_order_id()
        self.order_repository.reject(order_id)
        self.view.show_message(f"주문 거절 완료: {order_id}")

    def release_order(self):
        order_id = self.view.read_order_id()
        self.order_repository.release(order_id)
        self.view.show_message(f"출고 처리 완료: {order_id}")
