from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible.plugins.action import ActionBase
from anta.inventory.models import InventoryDevice
from anta.result_manager import ResultManager


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = {}

        result = super().run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

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
            tests_catalog = task_vars["anta_catalog"]["anta_catalog"]
            results = ResultManager()

            for test_class, test_params in tests_catalog:
                test_instance = test_class(device=anta_device, from_ansible=True)
                for index, command in enumerate(test_instance.instance_commands):
                    response = anta_device.session.send_request(command.command, version=command.version, output=command.ofmt)
                    data = json.loads(response) if command.ofmt == "json" else response
                    test_instance.instance_commands[index].output = data

                results.add_test_result(test_instance.test(**test_params))

            result["changed"] = True
            result["results"] = json.loads(results.get_results(output_format="json"))

        except Exception as e:
            result["failed"] = True
            result["message"] = str(e)

        return result
