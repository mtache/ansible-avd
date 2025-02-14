=== "Table"

    | Variable | Type | Required | Default | Value Restrictions | Description |
    | -------- | ---- | -------- | ------- | ------------------ | ----------- |
    | [<samp>ipv6_prefix_lists</samp>](## "ipv6_prefix_lists") | List, items: Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;- name</samp>](## "ipv6_prefix_lists.[].name") | String | Required, Unique |  |  | Prefix-list Name |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;sequence_numbers</samp>](## "ipv6_prefix_lists.[].sequence_numbers") | List, items: Dictionary | Required |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- sequence</samp>](## "ipv6_prefix_lists.[].sequence_numbers.[].sequence") | Integer | Required, Unique |  |  | Sequence ID |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;action</samp>](## "ipv6_prefix_lists.[].sequence_numbers.[].action") | String | Required |  |  | Action as string<br>Example: "permit 1b11:3a00:22b0:0082::/64 eq 128" |

=== "YAML"

    ```yaml
    ipv6_prefix_lists:
      - name: <str>
        sequence_numbers:
          - sequence: <int>
            action: <str>
    ```
