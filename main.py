import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from controller.main_controller import MainController
from controller.monitoring_controller import MonitoringController
from controller.order_controller import OrderController
from controller.production_controller import ProductionController
from controller.sample_controller import SampleController
from model.order import OrderRepository
from model.production_line import ProductionLine
from model.sample import SampleRepository
from view.console_view import ConsoleView


def _enable_windows_ansi():
    import ctypes

    STD_OUTPUT_HANDLE = -11
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004

    kernel32 = ctypes.windll.kernel32
    handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    mode = ctypes.c_uint32()
    if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
        return
    kernel32.SetConsoleMode(handle, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")
    if os.name == "nt":
        _enable_windows_ansi()

    sample_repository = SampleRepository()
    order_repository = OrderRepository()
    production_line = ProductionLine()
    view = ConsoleView()

    sample_controller = SampleController(sample_repository, view)
    order_controller = OrderController(order_repository, sample_repository, production_line, view)
    production_controller = ProductionController(production_line, view)
    monitoring_controller = MonitoringController(sample_repository, order_repository, view)

    main_controller = MainController(
        view, sample_controller, order_controller, production_controller, monitoring_controller
    )
    main_controller.run()


if __name__ == "__main__":
    main()
