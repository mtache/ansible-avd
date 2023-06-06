from __future__ import annotations

import asyncio
import json

from anta.result_manager import ResultManager, TestResult

from ansible_collections.arista.avd.plugins.plugin_utils.eos_validate_state_utils.models import InventoryDeviceHttpApi


async def run_tests(manager: ResultManager, device: InventoryDeviceHttpApi, tests: list[tuple[callable[..., TestResult], dict]]) -> dict:
    """
    Asynchronously runs tests on a device and gathers results.

    Args:
      manager (ResultManager): An instance of ANTA ResultManager to manage test results.
      device (InventoryDeviceHttpApi): An instance of the custom implementation of ANTA InventoryDevice with Ansible HttpApi connection session object.
      tests (list[tuple]): A list of tuples, where each tuple contains a callable test function and a dictionary of test parameters.

    Returns:
      dict: Test result data in a dictionary format.

    This function runs each test on the provided device asynchronously.
    Results are gathered and added to the ResultManager. The results are then outputted in JSON format and converted to a data dictionary.
    """
    tasks = [test_class(device=device).test(**test_params) for test_class, test_params in tests]

    results_list = await asyncio.gather(*tasks)
    [manager.add_test_result(result) for result in results_list]

    data = json.loads(manager.get_results(output_format="json"))

    return data
