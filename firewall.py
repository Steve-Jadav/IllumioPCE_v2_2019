import pandas as pd
import math

class Firewall(object):

    """
    Given a set of firewall rules, a network packet will be accepted by the
    firewall if and only if the direction, protocol, port, and IP Address match
    at least one of the input rules.
    """

    def __init__(self, file_path: str):

        """
        Initialize a Firewall object by passing the path to input rules csv file.
        Input will be a csv file containing 4 columns

        Input file structure:

        direction: inbound/outbound, corresponding to whether the traffic is entering or leaving the machine
        protocol: tcp/udp
        port: an integer in the range[1, 65535] or a port range
        IP address: IPv4 address in doted notation, consisting of 4 octets separated by '.' or an IP range

        """

        super(Firewall, self).__init__()
        self.rules = pd.read_csv(file_path)
        self.df_length = len(self.rules.index) - 1
        self.structurize_rules()


    def structurize_rules(self):

        """
        This method adds 2 new columns to the original dataframe. Namely, 'port_start' and 'port_end'.
        port_start contains the starting port number in a range.
        port_end contains the ending port number in a range. NaN if only port_start exists.
        Finally, it sorts the entire dataframe based on the port_start value.
        """

        self.rules['port_start'] = self.rules['port'].apply(lambda x: int(x.split('-')[0]))
        self.rules['port_end'] = self.rules['port'].apply(lambda x: None if len(x.split('-')) == 1 else int(x.split('-')[1]))
        self.rules.drop(['port'], axis=1, inplace=True)
        self.rules.sort_values(by='port_start', axis=0, ascending=True, inplace=True, kind='quicksort')
        self.rules.reset_index()


    def pretty_print_rules(self):
        """Used to print the input rules file."""

        print (self.rules)


    def binary_search(self, rules: pd.DataFrame, start_index: int, end_index: int, packet: tuple):

        """
        Binary search through a DataFrame of rules. This search function is written keeping in mind, 
        the number of rules in the input file. It performs considerably well in case the
        file has thousands of rules.

        :param: rules: pd.DataFrame
        :param: start_index: int
        :param: end_index: int
        :param: packet: tuple
        :return bool:

        """

        if end_index >= start_index:

            mid = int(start_index + (end_index-start_index)/2)
            mid_row = rules.iloc[mid]

            # There can be two possible cases at every recursive call
            # 1 -- The rule specifies a port number
            # 2 -- The rule specifies a port range


            # Case 1: No port range
            if math.isnan(mid_row['port_end']):

                if mid_row['port_start'] == packet[2]:

                    if mid_row['direction'] == packet[0] and mid_row['protocol'] == packet[1]:

                        mask = mid_row['IP address']
                        IP = packet[3]

                        if self.match_ip(mask, IP):
                            return True

                        else: return

                    else:
                        return self.binary_search(rules, start_index, mid-1, packet)

                elif mid_row['port_start'] > packet[2]:
                    return self.binary_search(rules, start_index, mid-1, packet)

                else:
                    return self.binary_search(rules, mid+1, end_index, packet)

            # Case 2: Given a port range
            elif math.isnan(mid_row['port_end']) == False:

                if packet[2] >= mid_row['port_start'] and packet[2] <= mid_row['port_end']:

                    if mid_row['direction'] == packet[0] and mid_row['protocol'] == packet[1]:

                        mask = mid_row['IP address']
                        IP = packet[3]

                        if self.match_ip(mask, IP):
                            return True

                        else: return

                    if packet[2] > mid_row['port_start']:
                         return self.binary_search(rules, mid+1, end_index, packet)

                elif packet[2] > mid_row['port_start']:
                    return self.binary_search(rules, start_index, mid-1, packet)

                elif packet[2] < mid_row['port_start']:
                    return self.binary_search(rules, start_index, mid-1, packet)


        else:
            return False


    def match_ip(mask: str, IP: str) -> bool:

        """
        Checks if a given IP falls under the range of a given IP Address range (i.e. mask)

        :param: mask: str
        :param: IP: str
        :return bool:

        """

        min_ip = mask.split(' - ')[0].split('.')
        max_ip = mask.split(' - ')[1].split('.')
        ip = IP.split('.')

        for i in range(4):
            if int(ip[i]) < int(min_ip[i]) or int(ip[i]) > int(max_ip[i]):
                return False

        return True


    def accept_packet(self, direction: str, protocol: str, port: int, ip_address: str) -> bool:

        """
        Returns True if the packet is allowed by the Firewall. False otherwise.
      
        :param: direction: str
        :param: protocol: str
        :param: port: int
        :param: ip_address: str
        :return bool:

        """

        packet: tuple = (direction, protocol, port, ip_address)
        allow: bool = self.binary_search(self.rules, 0, self.df_length, packet)

        return allow
