from firewall import Firewall

class TestFirewall(object):

    def __init__(self):
        pass

    def generate_test_cases(self):
        test_df = pd.read_csv('test_packets.csv')
        return test_df

if __name__=="__main__":

    firewall = Firewall('rules.csv')
    test = TestFirewall()
    packets_df = test.generate_test_cases()

    # Test firewall for all packets in the file
    for index, packet in packets_df.iterrows():
        print (firewall.accept_packet(packet[0], packet[1], packet[2], packet[3]))
