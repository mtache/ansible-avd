from __future__ import annotations

import json
from functools import cached_property

from ansible.errors import AnsibleError
from ansible_collections.arista.eos.plugins.httpapi.eos import HttpApi
from anta.models import AntaTestCommand


class InventoryDeviceHttpApi:
    """
    Custom implementation of an ANTA InventoryDevice with Ansible HttpApi connection session object.
    """

    def __init__(self, session: HttpApi):
        if isinstance(session, HttpApi):
            self.session = session
        else:
            raise AnsibleError(f"Error while instantiating {self.__class__.__name__}. Session object must be an instance of HttpApi connection plugin.")

    @cached_property
    def device_info(self) -> dict:
        """
        Get the device information once and cache it.

        Raises:
            AnsibleError: Raises an error if the send request failed.
        """
        try:
            return self.session.get_device_info()
        except ConnectionError as e:
            raise AnsibleError(f"Connection error raised while getting the device information: {e}") from e

    @cached_property
    def name(self) -> str:
        # Set the device name attribute
        return self.device_info.get("network_os_hostname")

    @cached_property
    def hw_model(self) -> str:
        # Set the device hw_model attribute
        return self.device_info.get("network_os_model")

    async def collect(self, command: AntaTestCommand) -> AntaTestCommand:
        """
        Collect device command result using Ansible HttpApi connection plugin.

        Args:
            command (AntaTestCommand): Command to execute on the device.

        Returns:
            AntaTestCommand: The command that was executed, including its output data.

        Raises:
            AnsibleError: Raises an error if the send request failed.
        """

        try:
            # Execute the command and process the response
            response = self.session.send_request(command.command, version=command.version, output=command.ofmt)
            command.output = json.loads(response) if command.ofmt == "json" else response

        except ConnectionError as e:
            raise AnsibleError(f"Connection error raised while collecting data for test {self.name} (on device {self.name}): {e}") from e

        return command
