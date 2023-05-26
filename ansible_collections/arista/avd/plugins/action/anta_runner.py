from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible.plugins.action import ActionBase
from anta.inventory.models import InventoryDevice
from anta.result_manager import ResultManager
from anta.tests.software import VerifyEOSExtensions


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = {}

        result = super().run(tmp, task_vars)

        # tests_catalog = task_vars["anta_catalog"]["anta_catalog"]

        params = {
            "name": task_vars["inventory_hostname"],
            "host": task_vars["ansible_host"],
            "username": task_vars["ansible_user"],
            "password": task_vars["ansible_httpapi_password"],
            "port": 443,
            "session": self._connection.httpapi,
        }

        try:
            anta_device = InventoryDevice(**params)
            test = VerifyEOSExtensions(device=anta_device, from_ansible=True)

            for index, command in enumerate(test.instance_commands):
                response = anta_device.session.send_request(command.command, version=command.version, output=command.ofmt)
                data = json.loads(response)
                test.instance_commands[index].output = data

            test_results = []
            test_results.append(test.test())

            results = ResultManager()

            results.add_test_results(test_results)

            result["changed"] = True
            result["anta_results"] = json.loads(results.get_results(output_format="json"))

        except Exception as e:
            result["failed"] = True
            result["message"] = str(e)

        return result
