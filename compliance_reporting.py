from jinja2 import Environment
from jinja2 import FileSystemLoader
import os

def j2_template_wrapper(template_service_name, **kwargs):
    """
    adapted from Santiago's code:
    https://github.com/NSO-developer/service-launcher/blob/d0dc2a41315d5ac6dd8aca0d78a10b14610ff63d/web_ui/api_controller.py
    :param template_service_name: jinja template to be used
    :param kwargs: arguments to be replaced in the jinja template
    :return:
    """
    DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    env = Environment(loader=FileSystemLoader(DIR_PATH + '/templates'))
    template = env.get_template(template_service_name + '.j2')
    rendered = template.render(**kwargs)
    return rendered



if __name__ == "__main__":
  delete_loopback(dry_run=False)
  template_output = j2_template_wrapper(template_service_name="wan",intf="Ethernet1/0",intdscr="WAN_byJinja",ip="10.1.1.1",
                  mask="255.255.255.252", qospol="200MB_SHAPE",bgpasn="65456",
                  bgpnip="10.1.1.2",remasn="65499")