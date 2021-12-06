# Compliance Reporting

need xmltodict package, can't install on prod server. 

```
 
ncs-setup --package nso/packages/neds/cisco-ios-cli-6.67 \
--package nso/packages/neds/cisco-nx-cli-5.20 \
--package nso/packages/neds/cisco-iosxr-cli-7.32 \
--package nso/packages/neds/cisco-asa-cli-6.12 \
--dest nso-instance
 
cd ~/nso-instance
ncs


 
ncs_cli -C -u admin

config
devices authgroups group labadmin
default-map remote-name cisco
default-map remote-password cisco
default-map remote-secondary-password cisco
commit

devices device edge-sw01
address 10.10.20.172
authgroup labadmin
device-type cli ned-id cisco-ios-cli-6.67
device-type cli protocol telnet
ssh host-key-verification none
state admin-state unlocked
commit
devices device core-rtr01
address   10.10.20.173
ssh host-key-verification none
authgroup labadmin
device-type cli ned-id cisco-iosxr-cli-7.32
device-type cli protocol telnet
state admin-state unlocked
!
devices device core-rtr02
address   10.10.20.174
ssh host-key-verification none
authgroup labadmin
device-type cli ned-id cisco-iosxr-cli-7.32
device-type cli protocol telnet
state admin-state unlocked
!
devices device dist-rtr01
address   10.10.20.175
ssh host-key-verification none
authgroup labadmin
device-type cli ned-id cisco-ios-cli-6.67
device-type cli protocol telnet
state admin-state unlocked
!
devices device dist-rtr02
address   10.10.20.176
ssh host-key-verification none
authgroup labadmin
device-type cli ned-id cisco-ios-cli-6.67
device-type cli protocol telnet
state admin-state unlocked
!
devices device dist-sw01
address   10.10.20.177
ssh host-key-verification none
authgroup labadmin
device-type cli ned-id cisco-nx-cli-5.20
device-type cli protocol telnet
ned-settings cisco-nx behaviours show-interface-all enable
state admin-state unlocked
!
devices device dist-sw02
address   10.10.20.178
ssh host-key-verification none
authgroup labadmin
device-type cli ned-id cisco-nx-cli-5.20
device-type cli protocol telnet
ned-settings cisco-nx behaviours show-interface-all enable
state admin-state unlocked
!
devices device edge-firewall01
address   10.10.20.171
ssh host-key-verification none
authgroup labadmin
device-type cli ned-id cisco-asa-cli-6.12
device-type cli protocol telnet
state admin-state unlocked
!
devices device edge-sw01
address   10.10.20.172
ssh host-key-verification none
authgroup labadmin
device-type cli ned-id cisco-ios-cli-6.67
device-type cli protocol telnet
state admin-state unlocked
!
devices device internet-rtr01
address   10.10.20.181
ssh host-key-verification none
authgroup labadmin
device-type cli ned-id cisco-ios-cli-6.67
device-type cli protocol telnet
state admin-state unlocked
!
commit
end
config
devices device-group IOS-DEVICES
device-name internet-rtr01
device-name dist-rtr01
device-name dist-rtr02
devices device-group XR-DEVICES
device-name core-rtr01
device-name core-rtr02
devices device-group NXOS-DEVICES
device-name dist-sw01
device-name dist-sw02
devices device-group ASA-DEVICES
device-name edge-firewall01
devices device-group ALL
device-group ASA-DEVICES
device-group IOS-DEVICES
device-group NXOS-DEVICES
device-group XR-DEVICES
commit
end

devices connect
devices sync-from
```

```
(py3venv) [developer@devbox ~]$ pip3 install xmltodict
Collecting xmltodict
  Downloading xmltodict-0.12.0-py2.py3-none-any.whl (9.2 kB)
Installing collected packages: xmltodict
Successfully installed xmltodict-0.12.0
WARNING: You are using pip version 20.3.3; however, version 21.3.1 is available.
You should consider upgrading via the '/home/developer/py3venv/bin/python3.6 -m pip install --upgrade pip' command.
(py3venv) [developer@devbox ~]$ git clone https://github.com/jabelk/compliance_reporting.git
Cloning into 'compliance_reporting'...
remote: Enumerating objects: 22, done.
remote: Counting objects: 100% (22/22), done.
remote: Compressing objects: 100% (16/16), done.
remote: Total 22 (delta 3), reused 18 (delta 2), pack-reused 0
Unpacking objects: 100% (22/22), done.
(py3venv) [developer@devbox ~]$
(py3venv) [developer@devbox ~]$ ncs-setup --package nso/packages/neds/cisco-ios-cli-6.67 \
> --package nso/packages/neds/cisco-nx-cli-5.20 \
> --package nso/packages/neds/cisco-iosxr-cli-7.32 \
> --package nso/packages/neds/cisco-asa-cli-6.12 \
> --dest nso-instance
(py3venv) [developer@devbox ~]$
(py3venv) [developer@devbox ~]$ cd ~/nso-instance
(py3venv) [developer@devbox nso-instance]$ ncs
(py3venv) [developer@devbox nso-instance]$
(py3venv) [developer@devbox nso-instance]$
(py3venv) [developer@devbox nso-instance]$ ncs_cli -C -u admin

admin connected from 192.168.254.11 using ssh on devbox
admin@ncs#
admin@ncs#
admin@ncs#
admin@ncs#
admin@ncs# config
Entering configuration mode terminal
admin@ncs(config)# devices authgroups group labadmin
admin@ncs(config-group-labadmin)# default-map remote-name cisco
admin@ncs(config-group-labadmin)# default-map remote-password cisco
admin@ncs(config-group-labadmin)# default-map remote-secondary-password cisco
admin@ncs(config-group-labadmin)# commit
Commit complete.
admin@ncs(config-group-labadmin)#
admin@ncs(config-group-labadmin)# devices device edge-sw01
admin@ncs(config-device-edge-sw01)# address 10.10.20.172
admin@ncs(config-device-edge-sw01)# authgroup labadmin
admin@ncs(config-device-edge-sw01)# device-type cli ned-id cisco-ios-cli-6.67
admin@ncs(config-device-edge-sw01)# device-type cli protocol telnet
admin@ncs(config-device-edge-sw01)# ssh host-key-verification none
admin@ncs(config-device-edge-sw01)# state admin-state unlocked
admin@ncs(config-device-edge-sw01)# commit
Commit complete.
admin@ncs(config-device-edge-sw01)# devices device core-rtr01
admin@ncs(config-device-core-rtr01)# address   10.10.20.173
admin@ncs(config-device-core-rtr01)# ssh host-key-verification none
admin@ncs(config-device-core-rtr01)# authgroup labadmin
admin@ncs(config-device-core-rtr01)# device-type cli ned-id cisco-iosxr-cli-7.32
admin@ncs(config-device-core-rtr01)# device-type cli protocol telnet
admin@ncs(config-device-core-rtr01)# state admin-state unlocked
admin@ncs(config-device-core-rtr01)# !
admin@ncs(config-device-core-rtr01)# devices device core-rtr02
admin@ncs(config-device-core-rtr02)# address   10.10.20.174
admin@ncs(config-device-core-rtr02)# ssh host-key-verification none
admin@ncs(config-device-core-rtr02)# authgroup labadmin
admin@ncs(config-device-core-rtr02)# device-type cli ned-id cisco-iosxr-cli-7.32
admin@ncs(config-device-core-rtr02)# device-type cli protocol telnet
admin@ncs(config-device-core-rtr02)# state admin-state unlocked
admin@ncs(config-device-core-rtr02)# !
admin@ncs(config-device-core-rtr02)# devices device dist-rtr01
admin@ncs(config-device-dist-rtr01)# address   10.10.20.175
admin@ncs(config-device-dist-rtr01)# ssh host-key-verification none
admin@ncs(config-device-dist-rtr01)# authgroup labadmin
admin@ncs(config-device-dist-rtr01)# device-type cli ned-id cisco-ios-cli-6.67
admin@ncs(config-device-dist-rtr01)# device-type cli protocol telnet
admin@ncs(config-device-dist-rtr01)# state admin-state unlocked
admin@ncs(config-device-dist-rtr01)# !
admin@ncs(config-device-dist-rtr01)# devices device dist-rtr02
admin@ncs(config-device-dist-rtr02)# address   10.10.20.176
admin@ncs(config-device-dist-rtr02)# ssh host-key-verification none
admin@ncs(config-device-dist-rtr02)# authgroup labadmin
admin@ncs(config-device-dist-rtr02)# device-type cli ned-id cisco-ios-cli-6.67
admin@ncs(config-device-dist-rtr02)# device-type cli protocol telnet
admin@ncs(config-device-dist-rtr02)# state admin-state unlocked
admin@ncs(config-device-dist-rtr02)# !
admin@ncs(config-device-dist-rtr02)# devices device dist-sw01
admin@ncs(config-device-dist-sw01)# address   10.10.20.177
admin@ncs(config-device-dist-sw01)# ssh host-key-verification none
admin@ncs(config-device-dist-sw01)# authgroup labadmin
admin@ncs(config-device-dist-sw01)# device-type cli ned-id cisco-nx-cli-5.20
admin@ncs(config-device-dist-sw01)# device-type cli protocol telnet
admin@ncs(config-device-dist-sw01)# ned-settings cisco-nx behaviours show-interface-all enable
admin@ncs(config-device-dist-sw01)# state admin-state unlocked
admin@ncs(config-device-dist-sw01)# !
admin@ncs(config-device-dist-sw01)# devices device dist-sw02
admin@ncs(config-device-dist-sw02)# address   10.10.20.178
admin@ncs(config-device-dist-sw02)# ssh host-key-verification none
admin@ncs(config-device-dist-sw02)# authgroup labadmin
admin@ncs(config-device-dist-sw02)# device-type cli ned-id cisco-nx-cli-5.20
admin@ncs(config-device-dist-sw02)# device-type cli protocol telnet
admin@ncs(config-device-dist-sw02)# ned-settings cisco-nx behaviours show-interface-all enable
admin@ncs(config-device-dist-sw02)# state admin-state unlocked
admin@ncs(config-device-dist-sw02)# !
admin@ncs(config-device-dist-sw02)# devices device edge-firewall01
admin@ncs(config-device-edge-firewall01)# address   10.10.20.171
admin@ncs(config-device-edge-firewall01)# ssh host-key-verification none
admin@ncs(config-device-edge-firewall01)# authgroup labadmin
admin@ncs(config-device-edge-firewall01)# device-type cli ned-id cisco-asa-cli-6.12
admin@ncs(config-device-edge-firewall01)# device-type cli protocol telnet
admin@ncs(config-device-edge-firewall01)# state admin-state unlocked
admin@ncs(config-device-edge-firewall01)# !
admin@ncs(config-device-edge-firewall01)# devices device edge-sw01
admin@ncs(config-device-edge-sw01)# address   10.10.20.172
admin@ncs(config-device-edge-sw01)# ssh host-key-verification none
admin@ncs(config-device-edge-sw01)# authgroup labadmin
admin@ncs(config-device-edge-sw01)# device-type cli ned-id cisco-ios-cli-6.67
admin@ncs(config-device-edge-sw01)# device-type cli protocol telnet
admin@ncs(config-device-edge-sw01)# state admin-state unlocked
admin@ncs(config-device-edge-sw01)# !
admin@ncs(config-device-edge-sw01)# devices device internet-rtr01
admin@ncs(config-device-internet-rtr01)# address   10.10.20.181
admin@ncs(config-device-internet-rtr01)# ssh host-key-verification none
admin@ncs(config-device-internet-rtr01)# authgroup labadmin
admin@ncs(config-device-internet-rtr01)# device-type cli ned-id cisco-ios-cli-6.67
admin@ncs(config-device-internet-rtr01)# device-type cli protocol telnet
admin@ncs(config-device-internet-rtr01)# state admin-state unlocked
admin@ncs(config-device-internet-rtr01)# !
admin@ncs(config-device-internet-rtr01)# commit
Commit complete.
admin@ncs(config-device-internet-rtr01)# end
admin@ncs# config
Entering configuration mode terminal
admin@ncs(config)# devices device-group IOS-DEVICES
admin@ncs(config-device-group-IOS-DEVICES)# device-name internet-rtr01
admin@ncs(config-device-group-IOS-DEVICES)# device-name dist-rtr01
admin@ncs(config-device-group-IOS-DEVICES)# device-name dist-rtr02
admin@ncs(config-device-group-IOS-DEVICES)# devices device-group XR-DEVICES
admin@ncs(config-device-group-XR-DEVICES)# device-name core-rtr01
admin@ncs(config-device-group-XR-DEVICES)# device-name core-rtr02
admin@ncs(config-device-group-XR-DEVICES)# devices device-group NXOS-DEVICES
admin@ncs(config-device-group-NXOS-DEVICES)# device-name dist-sw01
admin@ncs(config-device-group-NXOS-DEVICES)# device-name dist-sw02
admin@ncs(config-device-group-NXOS-DEVICES)# devices device-group ASA-DEVICES
admin@ncs(config-device-group-ASA-DEVICES)# device-name edge-firewall01
admin@ncs(config-device-group-ASA-DEVICES)# devices device-group ALL
admin@ncs(config-device-group-ALL)# device-group ASA-DEVICES
admin@ncs(config-device-group-ALL)# device-group IOS-DEVICES
admin@ncs(config-device-group-ALL)# device-group NXOS-DEVICES
admin@ncs(config-device-group-ALL)# device-group XR-DEVICES
admin@ncs(config-device-group-ALL)# commit
Commit complete.
admin@ncs(config-device-group-ALL)# end
admin@ncs#
admin@ncs# devices connect
connect-result {
    device core-rtr01
    result true
    info (admin) Connected to core-rtr01 - 10.10.20.173:23
}
connect-result {
    device core-rtr02
    result true
    info (admin) Connected to core-rtr02 - 10.10.20.174:23
}
connect-result {
    device dist-rtr01
    result true
    info (admin) Connected to dist-rtr01 - 10.10.20.175:23
}
connect-result {
    device dist-rtr02
    result true
    info (admin) Connected to dist-rtr02 - 10.10.20.176:23
}
connect-result {
    device dist-sw01
    result true
    info (admin) Connected to dist-sw01 - 10.10.20.177:23
}
connect-result {
    device dist-sw02
    result true
    info (admin) Connected to dist-sw02 - 10.10.20.178:23
}
connect-result {
    device edge-firewall01
    result true
    info (admin) Connected to edge-firewall01 - 10.10.20.171:23
}
connect-result {
    device edge-sw01
    result true
    info (admin) Connected to edge-sw01 - 10.10.20.172:23
}
connect-result {
    device internet-rtr01
    result true
    info (admin) Connected to internet-rtr01 - 10.10.20.181:23
}
admin@ncs# devices sync-from
sync-result {
    device core-rtr01
    result true
}
sync-result {
    device core-rtr02
    result true
}
sync-result {
    device dist-rtr01
    result true
}
sync-result {
    device dist-rtr02
    result true
}
sync-result {
    device dist-sw01
    result true
}
sync-result {
    device dist-sw02
    result true
}
sync-result {
    device edge-firewall01
    result true
}
sync-result {
    device edge-sw01
    result true
}
sync-result {
    device internet-rtr01
    result true
}
admin@ncs#
admin@ncs#
admin@ncs# conf
Entering configuration mode terminal
admin@ncs(config)# devices template MOTD-BANNER
admin@ncs(config-template-MOTD-BANNER)# ned-id cisco-ios-cli-6.67
admin@ncs(config-ned-id-cisco-ios-cli-6.67)# config
admin@ncs(config-config)# banner motd
(<string>): This is a MOTD abnner.
admin@ncs(config-config)# commit
Commit complete.
admin@ncs(config-config)# compliance reports report check-motd
admin@ncs(config-report-check-motd)# compare-template MOTD-BANNER IOS-DEVICES
admin@ncs(config-compare-template-MOTD-BANNER/IOS-DEVICES)# commit
Commit complete.
admin@ncs(config-compare-template-MOTD-BANNER/IOS-DEVICES)# end
admin@ncs# exit
(py3venv) [developer@devbox nso-instance]$
```


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

```
(py3venv) [developer@devbox nso-instance]$
(py3venv) [developer@devbox nso-instance]$
(py3venv) [developer@devbox nso-instance]$ cd
(py3venv) [developer@devbox ~]$ cd compliance_reporting/
(py3venv) [developer@devbox compliance_reporting]$ python
builtin_compliance.py  .gitignore             reports/
.git/                  README.md
(py3venv) [developer@devbox compliance_reporting]$ python builtin_compliance.py
{
  "tailf-ncs:output": {
    "id": 1,
    "compliance-status": "violations",
    "info": "Checking 3 devices and no services",
    "location": "http://localhost:8080/compliance-reports/report_1_admin_1_2021-12-6T13:10:6:0.html"
  }
}

Traceback (most recent call last):
  File "builtin_compliance.py", line 98, in <module>
    dict_report = translate_json_report(report_name="test_audit_1.xml", output_report_name="audit_convert.json")
  File "builtin_compliance.py", line 41, in translate_json_report
    with open("/home/developer/nso-instance/state/compliance-reports/{}".format(report_name)) as xml_file:
FileNotFoundError: [Errno 2] No such file or directory: '/home/developer/nso-instance/state/compliance-reports/test_audit_1.xml'
(py3venv) [developer@devbox compliance_reporting]$ ls
builtin_compliance.py  README.md  reports
(py3venv) [developer@devbox compliance_reporting]$
```

The script has three functions:
    - create_report: use RESTCONF to run a report, saving as XML format
    -  translate_json_report: translate the XML report to JSON and write to file in reports, and save the Python Dictionary object as a return value
    - extract_report_values: navigate the nested tree to extract values and put them in new, simpler objects. 

**Note** The filenames that NSO creates from the report in `create_report` break the Python file reading functions, so I manually rename them to something without `:` characters. 

```
(py3venv) [developer@devbox compliance_reporting]$
(py3venv) [developer@devbox compliance_reporting]$
(py3venv) [developer@devbox compliance_reporting]$
(py3venv) [developer@devbox compliance_reporting]$
(py3venv) [developer@devbox compliance_reporting]$ python builtin_compliance.py
{
  "tailf-ncs:output": {
    "id": 1,
    "compliance-status": "violations",
    "info": "Checking 3 devices and no services",
    "location": "http://localhost:8080/compliance-reports/report_1_admin_1_2021-12-6T13:18:16:0.xml"
  }
}

Traceback (most recent call last):
  File "builtin_compliance.py", line 98, in <module>
    dict_report = translate_json_report(report_name="test_audit_1.xml", output_report_name="audit_convert.json")
  File "builtin_compliance.py", line 41, in translate_json_report
    with open("/home/developer/nso-instance/state/compliance-reports/{}".format(report_name)) as xml_file:
FileNotFoundError: [Errno 2] No such file or directory: '/home/developer/nso-instance/state/compliance-reports/test_audit_1.xml'
(py3venv) [developer@devbox compliance_reporting]$
(py3venv) [developer@devbox compliance_reporting]$
(py3venv) [developer@devbox compliance_reporting]$ ls ~/nso-instance/state/compliance-reports/
report_1_admin_1_2021-12-6T13:18:16:0.xml
(py3venv) [developer@devbox compliance_reporting]$ cp ~/nso-instance/state/compliance-reports/report_1_admin_1_2021-12-6T13:18:16:0.xml ~/nso-instance/state/compliance-reports/test_audit_1.xml
(py3venv) [developer@devbox compliance_reporting]$
(py3venv) [developer@devbox compliance_reporting]$
(py3venv) [developer@devbox compliance_reporting]$
(py3venv) [developer@devbox compliance_reporting]$ python builtin_compliance.py
{
  "tailf-ncs:output": {
    "id": 2,
    "compliance-status": "violations",
    "info": "Checking 3 devices and no services",
    "location": "http://localhost:8080/compliance-reports/report_2_admin_1_2021-12-6T13:21:8:0.xml"
  }
}

Report Meta Data


{
    "report_creation_date": "2021-12-6 13:18:16",
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