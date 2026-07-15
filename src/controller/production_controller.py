class ProductionController:
    def __init__(self, production_line, view):
        self.production_line = production_line
        self.view = view

    def show_pending(self):
        self.view.show_production_jobs(self.production_line.list_pending())

    def complete_next(self):
        self.production_line.complete_next()
        self.view.show_message("생산 완료 처리되었습니다.")
