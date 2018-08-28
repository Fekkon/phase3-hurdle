# this module will be imported in the into your flowgraph

def make_usrp_ip_list(increment_address, ip_prefix, ip_base, num_nodes):
    '''
    Try to make it sane to allow people to use either fixed or incrementing IPs.
    Note: using 127.0.0.1 for both socket_meta_pdu servers and clients will
    result in conflicts. Consider using eth0 IP instead for the servers.

    IP prefix must be of the form "192.168.40."

    IP base is an int.

    Resulting list will be ip_prefix + "{}".format(ip_base +i)
    '''
    if increment_address:
        return [ip_prefix + "{}".format(ip_base +i) for i in range(num_nodes)]
    else:
        return [ip_prefix + "{}".format(ip_base) for i in range(num_nodes)]


import netifaces as ni

def get_debug_ip():
    '''
    This is used to allow people to autogenerate python from GNURadio Companion
    for the debug flowgraph in the case that their host system does not have an "eth0" interface.
    '''

    if u"eth0" in ni.interfaces():
        debug_ip = str(ni.ifaddresses("eth0")[ni.AF_INET][0]['addr'].decode('utf-8'))
    else:
        debug_ip = "10.0.0.0"

    return debug_ip
