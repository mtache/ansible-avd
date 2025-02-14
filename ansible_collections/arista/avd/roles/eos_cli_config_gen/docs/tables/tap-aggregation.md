=== "Table"

    | Variable | Type | Required | Default | Value Restrictions | Description |
    | -------- | ---- | -------- | ------- | ------------------ | ----------- |
    | [<samp>tap_aggregation</samp>](## "tap_aggregation") | Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;mode</samp>](## "tap_aggregation.mode") | Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;exclusive</samp>](## "tap_aggregation.mode.exclusive") | Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;enabled</samp>](## "tap_aggregation.mode.exclusive.enabled") | Boolean |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;profile</samp>](## "tap_aggregation.mode.exclusive.profile") | String |  |  |  | Profile Name |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;no_errdisable</samp>](## "tap_aggregation.mode.exclusive.no_errdisable") | List, items: String |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- &lt;str&gt;</samp>](## "tap_aggregation.mode.exclusive.no_errdisable.[].&lt;str&gt;") | String |  |  |  | Interface name e.g Ethernet1, Port-Channel1 |
    | [<samp>&nbsp;&nbsp;encapsulation_dot1br_strip</samp>](## "tap_aggregation.encapsulation_dot1br_strip") | Boolean |  |  |  |  |
    | [<samp>&nbsp;&nbsp;encapsulation_vn_tag_strip</samp>](## "tap_aggregation.encapsulation_vn_tag_strip") | Boolean |  |  |  |  |
    | [<samp>&nbsp;&nbsp;protocol_lldp_trap</samp>](## "tap_aggregation.protocol_lldp_trap") | Boolean |  |  |  |  |
    | [<samp>&nbsp;&nbsp;truncation_size</samp>](## "tap_aggregation.truncation_size") | Integer |  |  |  | Allowed truncation_size values vary depending on the platform<br> |
    | [<samp>&nbsp;&nbsp;mac</samp>](## "tap_aggregation.mac") | Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;timestamp</samp>](## "tap_aggregation.mac.timestamp") | Dictionary |  |  |  | mac.timestamp.replace_source_mac and mac.timestamp.header.format are mutually exclsuive. If both are defined, replace_source_mac takes precedence<br> |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;replace_source_mac</samp>](## "tap_aggregation.mac.timestamp.replace_source_mac") | Boolean |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;header</samp>](## "tap_aggregation.mac.timestamp.header") | Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;format</samp>](## "tap_aggregation.mac.timestamp.header.format") | String |  |  | Valid Values:<br>- 48-bit<br>- 64-bit |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;eth_type</samp>](## "tap_aggregation.mac.timestamp.header.eth_type") | Integer |  |  |  | EtherType |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;fcs_append</samp>](## "tap_aggregation.mac.fcs_append") | Boolean |  |  |  | mac.fcs_append and mac.fcs_error are mutually exclusive. If both are defined, mac.fcs_append takes precedence<br> |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;fcs_error</samp>](## "tap_aggregation.mac.fcs_error") | String |  |  | Valid Values:<br>- correct<br>- discard<br>- pass-through |  |

=== "YAML"

    ```yaml
    tap_aggregation:
      mode:
        exclusive:
          enabled: <bool>
          profile: <str>
          no_errdisable:
            - <str>
      encapsulation_dot1br_strip: <bool>
      encapsulation_vn_tag_strip: <bool>
      protocol_lldp_trap: <bool>
      truncation_size: <int>
      mac:
        timestamp:
          replace_source_mac: <bool>
          header:
            format: <str>
            eth_type: <int>
        fcs_append: <bool>
        fcs_error: <str>
    ```
