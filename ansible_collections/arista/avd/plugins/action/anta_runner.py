from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible.errors import AnsibleActionFail
from ansible.plugins.action import ActionBase
from anta.inventory.models import InventoryDevice
from anta.loader import parse_catalog
from anta.result_manager import ResultManager
from yaml import safe_load


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = {}

        result = super().run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        """
        NOTE: For now, these parameters are needed to instantiate InventoryDevice
        but only "name" and "session" are actually used by the class instance when using httpapi connection.
        """
        device_params = {
            "name": task_vars["inventory_hostname"],
            "host": task_vars["ansible_host"],
            "username": task_vars["ansible_user"],
            "password": task_vars["ansible_httpapi_password"],
            "port": 443,
            "session": self._connection.httpapi,
        }

        try:
            anta_device = InventoryDevice(**device_params)

            catalog_path = self._task.args.get("catalog_path")
            with open(catalog_path, "r", encoding="UTF-8") as file:
                input_catalog = safe_load(file)

            if not input_catalog:
                raise AnsibleActionFail(f"No tests were provided in the catalog: {catalog_path}")

            tests_catalog = parse_catalog(input_catalog)

            results = ResultManager()

            for test_class, test_params in tests_catalog:
                # from_ansible is a new attribute to run the appropriate decorator depending if the class is instantiated from Ansible or not.
                test_instance = test_class(device=anta_device, from_ansible=True)

                # NOTE: This part will be integrated in ANTA when it will support an httpapi session object.
                for index, command in enumerate(test_instance.instance_commands):
                    response = anta_device.session.send_request(command.command, version=command.version, output=command.ofmt)
                    data = json.loads(response) if command.ofmt == "json" else response
                    test_instance.instance_commands[index].output = data

                # Tests requiring input parameters will extract them from task_vars.
                # If ALL parameters are not found in task_vars, tests will run with the parameters from the input_catalog file.
                # In ANTA, tests requiring parameters are "skipped" if any of the parameters are not provided.
                if hasattr(test_class, "extract_parameters"):
                    extracted_params = test_class.extract_parameters(task_vars)
                    if not all(v is None for v in extracted_params.values()):
                        results.add_test_result(test_instance.test(**extracted_params))
                    else:
                        results.add_test_result(test_instance.test(**test_params))
                # Run remaining catalog tests that don't require any parameters
                else:
                    results.add_test_result(test_instance.test())

            result["changed"] = True
            result["results"] = json.loads(results.get_results(output_format="json"))

        except Exception as e:
            result["failed"] = True
            result["message"] = str(e)

        return result
