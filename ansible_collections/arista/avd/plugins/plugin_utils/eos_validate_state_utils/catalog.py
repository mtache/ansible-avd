from __future__ import annotations

from ansible.errors import AnsibleError

from ansible_collections.arista.avd.plugins.plugin_utils.utils.get import get

AVD_MAPPING = {"VerifyAPIHttpsSSL": {"profile": "management_api_http.https_ssl_profile"}}
"""
This is where we map AVD structured_config variables to ANTA tests input parameters.

The mapping (dict) constant needs to be updated if new test cases requiring AVD structured_config variables are added in ANTA.

The parameters must be entered in dot notation (foo.bar) according to AVD structured_config.

Ex:

  AVD_MAPPING = {
        'VerifyBannerMOTD': {
            'banner': 'banners.motd'
        }
      }

ANTA tests definitions are available at https://www.anta.ninja/api/tests/
"""


def _render_mapping(task_vars: dict, mapping: AVD_MAPPING) -> dict:
    """
    Private function to render the AVD_MAPPING with the appropriate task_vars variables.

    Returns:
      mapping (dict): The updated mapping dictionary with the right parameters.

    Raises:
      AnsibleError: Raises AnsibleError if a required parameter for a provided test is not found in task_vars.

    """
    for test, params in mapping.items():
        for param, value in params.items():
            if (param_value := get(task_vars, value)) is None:
                raise AnsibleError(f"{test} parameter {param} was not found in AVD structured_config.")
            else:
                mapping[test][param] = param_value

    return mapping


def update_catalog(input_catalog: dict, task_vars: dict) -> dict:
    """
    Function to update an ANTA test catalog with parameters from Ansible AVD task_vars.

    Args:
      input_catalog (dict): ANTA test catalog provided as input.
      task_vars (dict): All Ansible AVD task variables.

    Returns:
      input_catalog (dict): The updated ANTA test catalog including the mapped parameters from task_vars.

    """
    mapping = _render_mapping(task_vars, AVD_MAPPING)

    for tests in input_catalog.values():
        for test in tests:
            if (test_name := list(test.keys())[0]) in mapping:
                if test[test_name] is None:
                    test[test_name] = {}
                for param, value in mapping[test_name].items():
                    test[test_name][param] = value

    return input_catalog
