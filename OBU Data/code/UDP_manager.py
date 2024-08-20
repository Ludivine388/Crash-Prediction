# -----------------------------------------------------------
# Code to send specific message corresponding as a service in
# UDP
# !! UDP_IP has to be changed with your IP !!
# -----------------------------------------------------------

import socket
import xml.etree.ElementTree as ElementTree
service_data='''<ucuSetForwarding dt="2024-03-15T08:10:33" start="1" duration="0" fwdType="direct" fwdVersion="2" fwdId="34089"> <v2x> <forwarding ip="192.168.20.11" portIncoming="1444" portOutgoing="1444"/> </v2x> </ucuSetForwarding>'''
tree = ElementTree.ElementTree(ElementTree.fromstring(service_data))
root = tree.getroot()
data_xml = ElementTree.tostring(root, encoding='unicode', method='xml', xml_declaration=True)

#dt="[DT]2024-03-14T17:23:52.259Z"

UDP_IP = "192.168.30.220"
UDP_DES_PORT = 6543

#MESSAGE = "0000000000"
#m2 = bytes([000000, 200, 0, 0])
# MESSAGE = bytes([000000, 00, 0, 0,])

m2 = bytes([000000, 200, 0, 0])

service = (200).to_bytes(2, byteorder='big')
counter = (0).to_bytes(1, byteorder='big')
control = (0).to_bytes(1, byteorder='big')
book_now = (0).to_bytes(6, byteorder='big')
header = service + counter + control + book_now

m = header + bytes(service_data, 'utf-8')#service_data.encode("utf-8")
print(header)
print(service_data.encode("utf-8"))
print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_DES_PORT)
print("message:", m)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind(('192.168.20.11', 1444))
sock.sendto(m, (UDP_IP, UDP_DES_PORT))
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("received message: %s" % data)
