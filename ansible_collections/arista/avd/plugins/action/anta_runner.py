from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible.errors import AnsibleActionFail
from ansible.plugins.action import ActionBase
from anta.inventory.models import InventoryDeviceHttpApi
from anta.loader import parse_catalog
from anta.result_manager import ResultManager
from yaml import safe_load


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = {}

        result = super().run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        play_context = self._play_context
        connection = self._connection.httpapi

        # Need to set the right become_context to the _connection.httpapi object
        connection.set_become(play_context)

        device_params = {
            "name": task_vars["inventory_hostname"],
            "session": connection,
        }

        try:
            # Creating the ANTA device object with the HttpApi interface
            anta_device = InventoryDeviceHttpApi(**device_params)

            # Creating the catalog from Ansible task
            catalog_path = self._task.args.get("catalog_path")
            with open(catalog_path, "r", encoding="UTF-8") as file:
                input_catalog = safe_load(file)

            if not input_catalog:
                raise AnsibleActionFail(f"No tests were provided in the catalog: {catalog_path}")

            tests_catalog = parse_catalog(input_catalog)

            results = ResultManager()

            for test_class, test_params in tests_catalog:
                # sync is a new attribute to run ANTA tests synchronously.
                test_instance = test_class(device=anta_device, sync=True)

                # Tests requiring input parameters will extract them from task_vars.
                # If ALL parameters are not found in task_vars, tests will run with the parameters from the input_catalog file.
                # In ANTA, tests requiring parameters are "skipped" if any of the parameters are not provided.
                if hasattr(test_class, "extract_parameters"):
                    extracted_params = test_class.extract_parameters(task_vars)
                    if not all(v is None for v in extracted_params.values()):
                        results.add_test_result(test_instance.test(**extracted_params))
                else:
                    results.add_test_result(test_instance.test(**test_params))

            result["changed"] = True
            # FIXME: Need to parse the results for the report
            result["results"] = json.loads(results.get_results(output_format="json"))

        except Exception as e:
            result["failed"] = True
            result["message"] = str(e)

        return result
