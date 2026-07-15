class ProductionController:
    def __init__(self, production_line, view):
        self.production_line = production_line
        self.view = view

    def show_pending(self):
        self.view.show_production_jobs(self.production_line.list_pending())

    def watch_progress(self):
        jobs = self.production_line.list_pending()
        if not jobs:
            self.view.show_message("대기 중인 생산 작업이 없습니다.")
            return
        self.view.watch_current_progress(jobs[0])

    def complete_next(self):
        self.production_line.complete_next()
        self.view.show_message("생산 완료 처리되었습니다.")

    def count_pending(self):
        return len(self.production_line.list_pending())
