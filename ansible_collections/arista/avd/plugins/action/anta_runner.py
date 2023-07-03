from __future__ import absolute_import, division, print_function

__metaclass__ = type

import asyncio
import logging

from ansible.errors import AnsibleError
from ansible.plugins.action import ActionBase
from anta.loader import setup_logging
from anta.loader import parse_catalog
from anta.runner import main
from anta.inventory import AntaInventory
from anta.result_manager import ResultManager
from yaml import safe_load
import json

from ansible_collections.arista.avd.plugins.plugin_utils.eos_validate_state_utils import update_tests
from ansible_collections.arista.avd.plugins.plugin_utils.eos_validate_state_utils.models import AnsibleEOSDevice

logger = logging.getLogger(__name__)


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = {}

        result = super().run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        try:
            # Setup ANTA logging
            anta_logging = task_vars.get("anta_logging", 'info')
            setup_logging(level=anta_logging)

            inventory = AntaInventory()

            # Creating the ANTA device object with the HttpApi connection session
            device = AnsibleEOSDevice(name=task_vars.get('inventory_hostname'), connection=self._connection)
            inventory.add_device(device)

            # If anta_catalog is a dict of tests it will take precedence over anta_catalog_path
            if isinstance((anta_catalog := self._task.args.get("anta_catalog")), dict):
                input_catalog = anta_catalog

            # If anta_catalog is defaulted to "unset" or is empty, use the provided or the default anta_catalog_path
            else:
                catalog_path = self._task.args.get("anta_catalog_path")
                with open(catalog_path, "r", encoding="UTF-8") as file:
                    input_catalog = safe_load(file)

                # Raises error if the provided ANTA test catalog is empty
                if not input_catalog:
                    raise AnsibleError(f"The provided test catalog is empty: {catalog_path}")

            # Parsing the updated test catalog to be consumed by ANTA
            tests = parse_catalog(input_catalog)

            # Update the input catalog with AVD structured_config
            tests = update_tests(tests, task_vars)

            # Creating the ANTA ResultManager object
            manager = ResultManager()

            # Run tests
            logger.info(f'Running ANTA Tests for {device.name}')
            asyncio.run(main(manager, inventory, tests, tags=None, established_only=True))

            results = json.loads(manager.get_results(output_format="json"))

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
