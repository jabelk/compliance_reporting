# Compliance Reporting

Used within DevNet Sandbox. 
Assumes config template and compliance report already exists on the NSO instance. 

Sample config present:

```
devices template MOTD-BANNER
ned-id cisco-ios-cli-6.67
config
banner motd 
This is a MOTD abnner.
commit
compliance reports report check-motd
compare-template MOTD-BANNER IOS-DEVICES
commit
```

The script has three functions:
    - create_report: use RESTCONF to run a report, saving as XML format
    -  translate_json_report: translate the XML report to JSON and write to file in reports, and save the Python Dictionary object as a return value
    - extract_report_values: navigate the nested tree to extract values and put them in new, simpler objects. 

**Note** The filenames that NSO creates from the report in `create_report` break the Python file reading functions, so I manually rename them to something without `:` characters. 

Sample output:

```
(py3venv) [developer@devbox compliance_reporting]$ python builtin_compliance.py
Report Meta Data


{
    "report_creation_date": "2021-9-24 12:24:52",
    "user_id": "admin"
}
Report Summary


{
    "list_of_devices_not_compliant": [
        "dist-rtr01",
        "dist-rtr02",
        "internet-rtr01"
    ],
    "summary_result": "dist-rtr01 dist-rtr02 internet-rtr01",
    "which_compliance_report": "MOTD-BANNER"
}
Report Details


{
    "device_details": [
        {
            "config_result": "config {\n     banner {\n+        motd \"This is a MOTD abnner.\";\n     }\n }",
            "device_name": "Device dist-rtr01"
        },
        {
            "config_result": "config {\n     banner {\n+        motd \"This is a MOTD abnner.\";\n     }\n }",
            "device_name": "Device dist-rtr02"
        },
        {
            "config_result": "config {\n     banner {\n+        motd \"This is a MOTD abnner.\";\n     }\n }",
            "device_name": "Device internet-rtr01"
        }
    ],
    "which_compliance_report": "MOTD-BANNER"
}
(py3venv) [developer@devbox compliance_reporting]$
```