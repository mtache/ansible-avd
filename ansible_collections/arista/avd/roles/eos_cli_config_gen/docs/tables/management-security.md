=== "Table"

    | Variable | Type | Required | Default | Value Restrictions | Description |
    | -------- | ---- | -------- | ------- | ------------------ | ----------- |
    | [<samp>management_security</samp>](## "management_security") | Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;entropy_source</samp>](## "management_security.entropy_source") | String |  |  |  |  |
    | [<samp>&nbsp;&nbsp;password</samp>](## "management_security.password") | Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;minimum_length</samp>](## "management_security.password.minimum_length") | Integer |  |  | Min: 1<br>Max: 32 |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;encryption_key_common</samp>](## "management_security.password.encryption_key_common") | Boolean |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;encryption_reversible</samp>](## "management_security.password.encryption_reversible") | String |  |  |  |  |
    | [<samp>&nbsp;&nbsp;ssl_profiles</samp>](## "management_security.ssl_profiles") | List, items: Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;- name</samp>](## "management_security.ssl_profiles.[].name") | String |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;tls_versions</samp>](## "management_security.ssl_profiles.[].tls_versions") | String |  |  |  | List of allowed TLS versions as string<br>Examples:<br>  - "1.0"<br>  - "1.0 1.1"<br> |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;cipher_list</samp>](## "management_security.ssl_profiles.[].cipher_list") | String |  |  |  | cipher_list syntax follows the openssl cipher strings format.<br>Colon (:) separated list of allowed ciphers as a string<br> |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;trust_certificate</samp>](## "management_security.ssl_profiles.[].trust_certificate") | Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;certificates</samp>](## "management_security.ssl_profiles.[].trust_certificate.certificates") | List, items: String |  |  |  | List of trust certificate names<br>Examples:<br>  - test1.crt<br>  - test2.crt<br> |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- &lt;str&gt;</samp>](## "management_security.ssl_profiles.[].trust_certificate.certificates.[].&lt;str&gt;") | String |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;requirement</samp>](## "management_security.ssl_profiles.[].trust_certificate.requirement") | Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;basic_constraint_ca</samp>](## "management_security.ssl_profiles.[].trust_certificate.requirement.basic_constraint_ca") | Boolean |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;hostname_fqdn</samp>](## "management_security.ssl_profiles.[].trust_certificate.requirement.hostname_fqdn") | Boolean |  |  |  | Enforce hostname to be FQDN without wildcard.<br> |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;policy_expiry_date_ignore</samp>](## "management_security.ssl_profiles.[].trust_certificate.policy_expiry_date_ignore") | Boolean |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;system</samp>](## "management_security.ssl_profiles.[].trust_certificate.system") | Boolean |  |  |  | Use system-supplied trust certificates.<br> |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;chain_certificate</samp>](## "management_security.ssl_profiles.[].chain_certificate") | Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;certificates</samp>](## "management_security.ssl_profiles.[].chain_certificate.certificates") | List, items: String |  |  |  | List of chain certificate names<br>Examples:<br>  - chain1.crt<br>  - chain2.crt<br> |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- &lt;str&gt;</samp>](## "management_security.ssl_profiles.[].chain_certificate.certificates.[].&lt;str&gt;") | String |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;requirement</samp>](## "management_security.ssl_profiles.[].chain_certificate.requirement") | Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;basic_constraint_ca</samp>](## "management_security.ssl_profiles.[].chain_certificate.requirement.basic_constraint_ca") | Boolean |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;include_root_ca</samp>](## "management_security.ssl_profiles.[].chain_certificate.requirement.include_root_ca") | Boolean |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;certificate</samp>](## "management_security.ssl_profiles.[].certificate") | Dictionary |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;file</samp>](## "management_security.ssl_profiles.[].certificate.file") | String |  |  |  |  |
    | [<samp>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;key</samp>](## "management_security.ssl_profiles.[].certificate.key") | String |  |  |  |  |

=== "YAML"

    ```yaml
    management_security:
      entropy_source: <str>
      password:
        minimum_length: <int>
        encryption_key_common: <bool>
        encryption_reversible: <str>
      ssl_profiles:
        - name: <str>
          tls_versions: <str>
          cipher_list: <str>
          trust_certificate:
            certificates:
              - <str>
            requirement:
              basic_constraint_ca: <bool>
              hostname_fqdn: <bool>
            policy_expiry_date_ignore: <bool>
            system: <bool>
          chain_certificate:
            certificates:
              - <str>
            requirement:
              basic_constraint_ca: <bool>
              include_root_ca: <bool>
          certificate:
            file: <str>
            key: <str>
    ```
