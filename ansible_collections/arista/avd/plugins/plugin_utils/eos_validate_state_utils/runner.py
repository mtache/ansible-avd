from __future__ import annotations

import asyncio
import json


# TODO: Add annotations, docstring
async def run_tests(manager, device, tests):
    tasks = [test_class(device=device).test(**test_params) for test_class, test_params in tests]

    results_list = await asyncio.gather(*tasks)
    [manager.add_test_result(result) for result in results_list]

    data = json.loads(manager.get_results(output_format="json"))

    return data
