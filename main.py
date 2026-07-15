import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from controller.main_controller import MainController
from controller.sample_controller import SampleController
from model.sample import SampleRepository
from view.console_view import SampleView


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")

    sample_repository = SampleRepository()
    view = SampleView()
    sample_controller = SampleController(sample_repository, view)
    main_controller = MainController(view, sample_controller)
    main_controller.run()


if __name__ == "__main__":
    main()
