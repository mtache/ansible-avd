from __future__ import absolute_import, division, print_function

__metaclass__ = type

import asyncio

from ansible.errors import AnsibleError
from ansible.plugins.action import ActionBase
from anta.cli.utils import setup_logging
from anta.loader import parse_catalog
from anta.result_manager import ResultManager
from yaml import safe_load

from ansible_collections.arista.avd.plugins.plugin_utils.eos_validate_state_utils import run_tests, update_catalog
from ansible_collections.arista.avd.plugins.plugin_utils.eos_validate_state_utils.models import InventoryDeviceHttpApi


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

        try:
            # Setup ANTA logging
            anta_logging = task_vars.get("anta_logging")
            if anta_logging:
                setup_logging(level=anta_logging)

            # Creating the ANTA device object with the HttpApi connection session
            device = InventoryDeviceHttpApi(session=connection)

            # Creating the catalog from the Ansible task
            catalog_path = self._task.args.get("catalog_path")
            with open(catalog_path, "r", encoding="UTF-8") as file:
                input_catalog = safe_load(file)

            # Raises error if the provided ANTA test catalog is empty
            if not input_catalog:
                raise AnsibleError(f"The provided test catalog is empty: {catalog_path}")

            # Update the input catalog with AVD structured_config
            updated_catalog = update_catalog(input_catalog, task_vars)

            # Parsing the updated test catalog to be consumed by ANTA
            tests = parse_catalog(updated_catalog)

            # Creating the ANTA ResultManager object
            manager = ResultManager()

            # Run tests
            results = asyncio.run(run_tests(manager=manager, device=device, tests=tests))

            # Format the data properly for the eos_validate_state report
            for item in results:
                item["test_category"] = ", ".join([category.upper() if len(category) <= 5 else category.title() for category in item["test_category"]])
                item["messages"] = "\n".join(item["messages"])

            result["changed"] = True
            result["results"] = results

        except Exception as e:
            result["failed"] = True
            result["message"] = str(e)

        return result
