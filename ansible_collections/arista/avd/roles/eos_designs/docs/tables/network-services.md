=== "Table"

    | Variable | Type | Required | Default | Value Restrictions | Description |
    | -------- | ---- | -------- | ------- | ------------------ | ----------- |
    | [<samp>&lt;network_services_keys.name&gt;</samp>](## "&lt;network_services_keys.name&gt;") | List, items: Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;- name</samp>](## "&lt;network_services_keys.name&gt;.[].name") | String | Required, Unique |  |  | Specify a tenant name.<br>Tenant provide a construct to group L3 VRFs and L2 VLANs.<br>Networks services can be filtered by tenant name.<br> |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;mac_vrf_vni_base</samp>](## "&lt;network_services_keys.name&gt;.[].mac_vrf_vni_base") | Integer |  |  | Min: 0<br>Max: 16770000 | Base number for MAC VRF VXLAN Network Identifier (required with VXLAN).<br>VXLAN VNI is derived from the base number with simple addition.<br>i.e. mac_vrf_vni_base = 10000, svi 100 = VNI 10100, svi 300 = VNI 10300.<br> |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;mac_vrf_id_base</samp>](## "&lt;network_services_keys.name&gt;.[].mac_vrf_id_base") | Integer |  |  | Min: 0<br>Max: 16770000 | If not set, "mac_vrf_vni_base" will be used.<br>Base number for MAC VRF RD/RT ID (Required unless mac_vrf_vni_base is set)<br>ID is derived from the base number with simple addition.<br>i.e. mac_vrf_id_base = 10000, svi 100 = RD/RT 10100, svi 300 = RD/RT 10300.<br> |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;vlan_aware_bundle_number_base</samp>](## "&lt;network_services_keys.name&gt;.[].vlan_aware_bundle_number_base") | Integer |  | `0` |  | Base number for VLAN aware bundle RD/RT.<br>The "Assigned Number" part of RD/RT is derived from vrf_vni + vlan_aware_bundle_number_base.<br> |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;evpn_l2_multi_domain</samp>](## "&lt;network_services_keys.name&gt;.[].evpn_l2_multi_domain") | Boolean |  | `True` |  | Explicitly extend all VLANs/VLAN-Aware Bundles inside the tenant to remote EVPN domains. |

=== "YAML"

    ```yaml
    <network_services_keys.name>:
      - name: <str>
        mac_vrf_vni_base: <int>
        mac_vrf_id_base: <int>
        vlan_aware_bundle_number_base: <int>
        evpn_l2_multi_domain: <bool>
    ```
