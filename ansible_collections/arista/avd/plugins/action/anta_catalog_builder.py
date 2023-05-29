from __future__ import absolute_import, division, print_function

__metaclass__ = type

from typing import Any, Dict, List, Tuple

from ansible.plugins.action import ActionBase
from anta.loader import parse_catalog

TestTuple = Tuple[str, Dict[str, str]]
Catalog = Dict[str, List[Dict[str, Any]]]


AVD_MAPPING: Dict[str, List[TestTuple]] = {
    "management_api_http": [("anta.tests.security.VerifyAPIHttpStatus", {}), ("anta.tests.security.VerifyAPIHttpsSSL", {"profile": "https_ssl_profile"})]
}


def _get_package_name(test_name: str) -> str:
    """Extracts the package name from a fully qualified test name."""
    return test_name.rsplit(".", 1)[0]


def _get_test_name(test_name: str) -> str:
    """Extracts the test name from a fully qualified test name."""
    return test_name.rsplit(".", 1)[1]


def _update_test_parameters(value: Any, test_parameters: Dict[str, str]) -> Dict[str, Any]:
    """Updates the test parameters based on the provided structured configuration values."""
    return {param_key: value.get(structured_config_key) for param_key, structured_config_key in test_parameters.items()}


def _build_new_catalog(task_vars: Dict[str, Any], test_mapping: Dict[str, List[TestTuple]]) -> Catalog:
    """
    Constructs package tests from the structured configuration and the test mapping.

    Returns:
        A dictionary containing package tests.
    """
    new_catalog: Catalog = {}
    for key, value in task_vars.items():
        if key in test_mapping:
            for test in test_mapping[key]:
                full_test_name, test_parameters = test
                package_name = _get_package_name(full_test_name)
                test_name = _get_test_name(full_test_name)
                test_parameters_updated = _update_test_parameters(value, test_parameters)
                if package_name not in new_catalog:
                    new_catalog[package_name] = []
                new_catalog[package_name].append({test_name: test_parameters_updated})

    return new_catalog


def _merge_catalogs(new_catalog: Catalog, existing_catalog: Catalog) -> Catalog:
    """
    Merges the new catalog with the existing catalog, overwriting existing tests in the process.

    Args:
        new_catalog: A dictionary representing the new test catalog.

    Returns:
        A dictionary representing the merged catalog.
    """
    for package, tests in new_catalog.items():
        if package in existing_catalog:
            for new_test in tests:
                new_test_name, new_test_params = list(new_test.items())[0]
                existing_catalog[package] = [test for test in existing_catalog[package] if list(test.keys())[0] != new_test_name]
                existing_catalog[package].append(new_test)
        else:
            existing_catalog[package] = tests

    return existing_catalog


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = {}

        result = super().run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        existing_catalog = self._task.args.get("input_catalog", None)

        try:
            new_catalog = _build_new_catalog(task_vars, AVD_MAPPING)

            if existing_catalog:
                new_catalog = _merge_catalogs(new_catalog, existing_catalog)

            tests_catalog = parse_catalog(new_catalog)

            result["changed"] = True
            # FIXME: Return a list of tuples instead of list of lists
            result["anta_catalog"] = tests_catalog

        except Exception as e:
            result["failed"] = True
            result["message"] = str(e)

        return result
