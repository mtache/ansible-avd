from __future__ import annotations

from ansible_collections.arista.avd.plugins.plugin_utils.utils import get


def update_catalog(input_catalog: dict, task_vars: dict) -> dict:
    """
    Function to update an ANTA test catalog with parameters from Ansible AVD task_vars.

    Args:
      input_catalog (dict): ANTA test catalog provided as input.
      task_vars (dict): All Ansible AVD task variables.

    Returns:
      dict: The updated ANTA test catalog including the mapped parameters from task_vars.


    The mapping (dict) variable inside this function needs to be updated if new test cases requiring AVD input parameters are added in ANTA.

    Ex:
      mapping: dict = {
        'anta.tests.management': [{'VerifyBannerMOTD': {'banner': get(task_vars, 'banners.motd')}}]
      }
    """
    mapping: dict = {"anta.tests.security": [{"VerifyAPIHttpsSSL": {"profile": get(task_vars, "management_api_http.https_ssl_profile")}}]}

    input_catalog.update(mapping)

    return input_catalog
