=== "Table"

    | Variable | Type | Required | Default | Value Restrictions | Description |
    | -------- | ---- | -------- | ------- | ------------------ | ----------- |
    | [<samp>radius_servers</samp>](## "radius_servers") <span style="color:red">deprecated</span> | List, items: Dictionary |  |  |  | <span style="color:red">This key is deprecated. Support will be removed in AVD version v5.0.0. Use <samp>radius_server.hosts</samp> instead.</span> |
    | [<samp>&nbsp;&nbsp;- host</samp>](## "radius_servers.[].host") | String |  |  |  | Host IP address or name |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;vrf</samp>](## "radius_servers.[].vrf") | String |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;key</samp>](## "radius_servers.[].key") | String |  |  |  | Encrypted key |

=== "YAML"

    ```yaml
    radius_servers:
      - host: <str>
        vrf: <str>
        key: <str>
    ```
