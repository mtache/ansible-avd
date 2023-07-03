from __future__ import annotations

import json
from json import JSONDecodeError
import logging
from typing import Any, Optional, List

from ansible.errors import AnsibleError
from ansible_collections.ansible.netcommon.plugins.connection.httpapi import Connection
from rich.pretty import pretty_repr

from anta.device import AntaDevice
from anta.models import AntaTestCommand
from anta.tools.misc import exc_to_str, tb_to_str

logger = logging.getLogger(__name__)


class AnsibleEOSDevice(AntaDevice):
    """
    Implementation of an AntaDevice using Ansible HttpApi plugin for EOS.
    """

    def __init__(self,
                 name: str,
                 connection: Connection,
                 tags: Optional[List[str]] = None):
        super().__init__(name, tags)
        if isinstance(connection, Connection) and connection._network_os == 'arista.eos.eos':
            self._connection = connection
        else:
            raise AnsibleError(f"Error while instantiating {self.__class__.__name__}: The provided Ansible connection does not use EOS HttpApi plugin")
        logger.debug(pretty_repr(vars(self)))

    def __eq__(self, other: object) -> bool:
        """
        Two AsyncEOSDevice objects are equal if the hostname and the port are the same.
        This covers the use case of port forwarding when the host is localhost and the devices have different ports.
        """
        if not isinstance(other, AnsibleEOSDevice):
            return False
        return self._connection._options.host == other._connection._options.host and self._connection._options.port == other._connection._options.port

    @property
    def __dict__(self) -> dict[str, Any]:
        """
        Returns a dictionary that represents the AntaDevice object.
        Can be overriden in subclasses.
        """
        connection_vars = vars(self._connection)
        if '_defs' in connection_vars:
            del connection_vars['_defs']
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "hw_model": self.hw_model,
            "tags": self.tags,
            "is_online": self.is_online,
            "established": self.established,
            "_connection": connection_vars,
        }

    async def collect(self, command: AntaTestCommand) -> AntaTestCommand:
        """
        Collect device command result using Ansible HttpApi connection plugin.
        Supports outformat `json` and `text` as output structure.

        Args:
            command: the command to collect

        Raises:
            AnsibleError: Raises an error if the send request failed.
        """
        try:
            # Execute the command and process the response
            response = self._connection.send_request(command.command, version=command.version, output=command.ofmt)
            data = json.loads(response) if command.ofmt == "json" else response
            command.output = data
            logger.debug(f"{self.name}: {command}")
        except ConnectionError as e:
            message = f"Cannot connect to device {self.name}: {e}"
            logger.error(message)
            raise AnsibleError(message) from e
        except JSONDecodeError:
            # Even if the outformat is 'json' send_request() sometimes returns a non-valid JSON depending on the output content
            # https://github.com/ansible-collections/arista.eos/blob/main/plugins/httpapi/eos.py#L194
            command.output = {"messages": [response]}
        except Exception as e:  # pylint: disable=broad-exception-caught
            message = f"Exception raised while collecting command '{command.command}' on device {self.name} - {exc_to_str(e)}"
            logger.critical(message)
            logger.debug(tb_to_str(e))
            logger.debug(command)
            raise AnsibleError(message) from e

    async def refresh(self) -> None:
        """
        Update attributes of an AsyncEOSDevice instance.

        This coroutine must update the following attributes of AsyncEOSDevice:
        - is_online: When a device IP is reachable and a port can be open
        - established: When a command execution succeeds
        - hw_model: The hardware model of the device
        """
        logger.debug(f"Refreshing device {self.name}")
        try:
            device_info = self._connection.get_device_info()
        except ConnectionError as e:
            message = f"Connection error raised while getting the device information: {e}"
            logger.error(message)
            raise AnsibleError(message) from e
        self.is_online = self._connection._connected
        if self.is_online:
            self.hw_model = device_info["network_os_model"]
        else:
            logger.warning(f"Could not connect to device {self.name}")
        self.established = bool(self.is_online and self.hw_model)
        logger.debug(pretty_repr(vars(self)))
