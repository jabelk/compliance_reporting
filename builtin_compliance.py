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
