import pcap
import dpkt
from datetime import datetime
import os
import pandas as pd
import numpy as np
import sys

def sniffing(nicname):
    print('Start Snifing... @', nicname, 'UDP, Port 5500')
    sniffer = pcap.pcap(name=nicname, promisc=True, immediate=True, timeout_ms=50)
    sniffer.setfilter('udp and port 5500')

    csv_name = 'csidata_{}.csv'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))

    print('Save CSI Data to {}...'.format(csv_name))

    for ts, pkt in sniffer:
        eth = dpkt.ethernet.Ethernet(pkt)
        ip = eth.data
        udp = ip.data 
        csi = udp.data[18:]

        bandwidth = ip.__hdr__[2][2]
        nsub = int(bandwidth * 3.2)

        # Convert CSI bytes to numpy array
        csi_np = np.frombuffer(
            csi,
            dtype = np.int16,
            count = nsub * 2
        )

        # Cast numpy 1-d array to matrix
        csi_np = csi_np.reshape((1, nsub * 2))

        # Convert csi into complex numbers
        csi_cmplx = np.fft.fftshift(
            csi_np[:1, ::2] + 1.j * csi_np[:1, 1::2], axes=(1,)
        )

        csi_df = pd.DataFrame(np.abs(csi_cmplx))
        csi_df.insert(0, 'time', ts)

        if not os.path.exists(csv_name):
            print('new csv')
            csi_df.to_csv(csv_name, index=False, mode='w')
        else:
            print('append csv')
            csi_df.to_csv(csv_name, index=False, mode='a', header=False)

if __name__ == '__main__':
    sniffingInterface = sys.argv[1]
    sniffing(sniffingInterface)
