# Learn by Doing: Compliance Reporting and the Python API on MOTD Banner

NSO has a ton of features. This repository is the first of a series which will show a simple use case, along with a feature. The purpose is dual:

1. See NSO applied to a variety of configuration situations and see how versatile it is.
1. Learn something new and have an example to follow

This example is using:

**MOTD Banner**

and the features I am showcasing are:

**Compliance Reporting**
AND
**Python API**

This example assumes a working knowledge of Python and NSO. 

## Installation

[Reserve the NSO Reservable Sandbox](https://devnetsandbox.cisco.com/RM/Diagram/Index/43964e62-a13c-4929-bde7-a2f68ad6b27c?diagramType=Topology)

If you need to revisit some of the NSO Basics, you can [start here](https://developer.cisco.com/learning/lab/learn-nso-the-easy-way/step/1). 

Use some type of file transfer program or [VS Code has remote SSH](https://code.visualstudio.com/docs/remote/ssh) (drag and drop the package into the packages directory)

### Problem Statement

NSO has a built-in compliance reporting feature, which uses configuration templates to compare the intended state in the template against the actual state on the device. It will then tell you the difference in lines of configuration, and you can use NSO to push the templated desired config to the device. 

This example will focus on using the Python API to extract information from the compliance report data structure. You could then take that data and put it in an email, a Jinja2 Template report or something else. 


### Set Up

Log into the **devbox** (IP: 10.10.20.50), even though the system install would have less set up, we need to install a Python package for our example and the devbox allows us to do that and the system install server does not have internet access. 

After logging in, you will need to set up an NSO instance with the devices in the network. These commands will do the set up:

```
 
ncs-setup --package nso/packages/neds/cisco-ios-cli-6.67 \
--package nso/packages/neds/cisco-nx-cli-5.20 \
--package nso/packages/neds/cisco-iosxr-cli-7.32 \
--package nso/packages/neds/cisco-asa-cli-6.12 \
--dest nso-instance
 
cd ~/nso-instance
ncs
```

and now enter in the NSO CLI to configure NSO. 

```
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
exit
```

Now exit back to the Linux prompt to install the required Python package using the `pip3 install xmltodict` command, and clone down this example

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
```

Now enter back into the NSO CLI to create a create a device template and a compliance report with the following commands:

```
config
devices template MOTD-BANNER
ned-id cisco-ios-cli-6.67
config
banner motd
This is a MOTD abnner.
commit
compliance reports report check-motd
compare-template MOTD-BANNER IOS-DEVICES
commit
end
```

The output should look like this:

```
(py3venv) [developer@devbox nso-instance]$ ncs_cli -C -u admin

admin connected from 192.168.254.11 using ssh on devbox
admin@ncs#
admin@ncs#
admin@ncs#
admin@ncs#
admin@ncs# config
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

Now in order to run the Python code, navigate to the `compliance_reporting` directory you cloned earlier and execute the script `python builtin_compliance.py`. The code will throw an error because it creates a file that has an invalid name, you will need to go in and rename it. 

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

You may want to look at the script code and see how it works:

```python
import json
import xmltodict
import requests
from requests.auth import HTTPBasicAuth

def create_report(report_format, server_name, report_name, user, password):
    """
    Assumes config template and compliance report already exists on the NSO instance. 
    
    Sample config present:
    
    devices template MOTD-BANNER
    ned-id cisco-ios-cli-6.67
    config
    banner motd 
    This is a MOTD abnner.
    commit
    compliance reports report check-motd
    compare-template MOTD-BANNER IOS-DEVICES
    commit
    """
    url = "{}/restconf/data/tailf-ncs:compliance/reports/report={}/run".format(server_name,report_name)

    payload = "<input>\n\t<outformat>{}</outformat>\n</input>".format(report_format)
    headers = {
    'Content-Type': 'application/yang-data+xml',
    'Accept': 'application/yang-data+json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, auth=HTTPBasicAuth(user, password))

    print(response.text)
    return response.text

def translate_json_report(report_name, output_report_name):
    """
    Reads in a report file in XML format. Filename must be cleaned up to remove ":" characters from auto-generated report
    Converts report to JSON for easier Python consumption, writing to file
    Returns Data dictionary data of the conversion
    """
    with open("/home/developer/nso-instance/state/compliance-reports/{}".format(report_name)) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())

    json_data = json.dumps(data_dict)

    # Putting it in a folder
    output_report_name = "reports/{}".format(output_report_name)

    with open(output_report_name, "w") as json_file:
        json_file.write(json_data)
    
    return data_dict

def extract_report_values(dict_report):
    report_meta_data = {
        "report_creation_date" : dict_report.get("article").get("info").get("pubdate"),
        "user_id" : dict_report.get("article").get("info").get("author").get("firstname"),
    }


    summary_result = dict_report.get("article").get("sect1")[0].get("sect2").get("sect3").get("para")
    # remove the first list entry which does not have a device name
    summary_result.pop(0)
    summary_result = " ".join(summary_result)

    report_summary = {
        "which_compliance_report" : dict_report.get("article").get("sect1")[1].get("sect2").get("sect3").get("title"),
        "summary_result" : summary_result,
        "list_of_devices_not_compliant" :  dict_report.get("article").get("sect1")[0].get("sect2").get("sect3").get("para")
    }

    # extract list of device details
    details_list = dict_report.get("article").get("sect1")[1].get("sect2").get("sect3").get("sect4")

    compliance_details_result = []

    for config_snippet in details_list:
        compliance_details_result.append(
            {
                "device_name" : config_snippet.get("title"),
                "config_result" : config_snippet.get("informalexample").get("screen")
            }
        )

    report_details = {
        "which_compliance_report" : dict_report.get("article").get("sect1")[1].get("sect2").get("sect3").get("title"),
        "device_details" : compliance_details_result
    }
    

    return report_meta_data, report_summary, report_details



if __name__ == "__main__":
    create_report(report_format="xml", server_name="http://10.10.20.50:8080", report_name="check-motd", user="admin", password="admin")
    # Manually rename file to remove special characters. Then re-run the script. Put report_name= new name of file
    dict_report = translate_json_report(report_name="test_audit_1.xml", output_report_name="audit_convert.json")
    report_meta_data, report_summary, report_details = extract_report_values(dict_report)

    print("Report Meta Data \n \n")
    print(json.dumps(report_meta_data, indent=4, sort_keys=True))

    print("Report Summary \n \n")
    print(json.dumps(report_summary, indent=4, sort_keys=True))

    print("Report Details \n \n")
    print(json.dumps(report_details, indent=4, sort_keys=True))
```


**Note** The filenames that NSO creates from the report in `create_report` break the Python file reading functions, so I manually rename them to something without `:` characters. The file will be in the path `/home/developer/nso-instance/state/compliance-reports/`

```
(py3venv) [developer@devbox compliance_reporting]$
(py3venv) [developer@devbox compliance_reporting]$ ls ~/nso-instance/state/compliance-reports/
report_1_admin_1_2021-12-6T13:18:16:0.xml
(py3venv) [developer@devbox compliance_reporting]$ cp ~/nso-instance/state/compliance-reports/report_1_admin_1_2021-12-6T13:18:16:0.xml ~/nso-instance/state/compliance-reports/test_audit_1.xml
(py3venv) [developer@devbox compliance_reporting]$
```

After renaming the file, re-run the script:

```
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