"""
agentP - DevOps & Remote Controller
Handles Android AVD control, Mobile Remote QR Pairing, and Enterprise KPI/Excel Reports.
Author: Liam (DevOps Lead) & Sophia (Compliance/Excel)
"""

import sys
import os
from typing import Dict, Any, Tuple
try:
    from .base_controller import BaseController
except ImportError:
    from base_controller import BaseController

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'services')))
from avd_controller import AvdControllerService
from remote_controller import MobileRemoteService
from excel_reporter import ExcelCorporateReporter

class DevOpsController(BaseController):
    """Manages DevOps lifecycle, AVD machine control, and Corporate KPI Reports."""

    @staticmethod
    def get_avd_status() -> Tuple[int, Dict[str, str], bytes]:
        status = AvdControllerService.get_status()
        return BaseController.json_response(status, 200)

    @staticmethod
    def launch_avd(data: Dict[str, Any]) -> Tuple[int, Dict[str, str], bytes]:
        mode = data.get('mode', 'gui')
        res = AvdControllerService.launch_emulator(mode=mode)
        return BaseController.json_response(res, 200)

    @staticmethod
    def reload_avd() -> Tuple[int, Dict[str, str], bytes]:
        res = AvdControllerService.trigger_hot_reload()
        return BaseController.json_response(res, 200)

    @staticmethod
    def screenshot_avd() -> Tuple[int, Dict[str, str], bytes]:
        res = AvdControllerService.capture_screenshot()
        return BaseController.json_response(res, 200)

    @staticmethod
    def get_remote_pairing() -> Tuple[int, Dict[str, str], bytes]:
        pairing = MobileRemoteService.get_pairing_info()
        return BaseController.json_response(pairing, 200)

    @staticmethod
    def export_excel_report() -> Tuple[int, Dict[str, str], bytes]:
        report = ExcelCorporateReporter.generate_acceptance_data()
        return BaseController.json_response(report, 200)
