import socket, sys, binascii
from struct import *

# Create a raw socket. Replace FAMILY and TYPE with the correct socket object
try:
    s = socket.socket(socket.FAMILY, socket.TYPE, socket.IPPROTO_RAW)
except socket.error as msg:
    print('Socket creation failed! \nError Code - ' + str(msg))
    sys.exit()

# Construct the packet. We are going to add the IP header, then just stick some data in it since a raw socket can handle this.
packet = ''

source_ip = '10.1.0.2'	# This is your net1 client...but you can spoof this address if you want!
dest_ip = '10.3.0.2' 	# This is your DMZ client, but it can be wherever you want to send the packets.

# IP header info in decimal. You need to consider the full field size and the decimal therein. The ip_ihl_ver field for example is actually read as 2 nibbles, however for ease of coding, we're going to just use the decimal value of the entire byte, assuming that the packet is not using IP options.
ip_ver_ihl = ?	 # Decimal representing '0x45', as this is the first byte of a normal IPv4 packet.
ip_tos = ?	    # Type of service/QoS
ip_len = 0      # kernel will fill this in
ip_id = ?      # IP ID of this packet, this value can just be made-up
ip_frag = ?	    # This is not a fragmented packet...but you could make it one if you wanted!
ip_ttl = ?	    # Use the TTL of Linux
ip_proto = ?	# This should be the value for TCP
ip_check = 0    # kernel will fill the correct checksum
ip_saddr = socket.inet_aton(source_ip)
ip_daddr = socket.inet_aton(dest_ip)

# This portion creates the header by packing the above variables into a structure. The ! in the string means network order, while the code following specifies how to store the info. These "?"'s should indicate the size of the field that the information contained in the corresponding variables should be stored in. The "?"'s should be replaced with B, H or 4s. B=Byte, H=Half-word, 4s=four byte string
ip_header = pack('!????????????' , ip_ver_ihl, ip_tos, ip_len, ip_id, ip_frag, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)

# TCP header fields in decimal. Create your fields in a similar manner as in the IP header. Replace the TCP_VARs with a variable and replace the "?" values for each. 
# The variables tcp_window and tcp_check have been provided for you. 
# Be sure to either combine the data offset and reserve fields into 1 byte, or combine them afterwards.
TCP_VAR1 = ?
TCP_VAR2 = ?
TCP_VAR3 = ?
TCP_VAR4 = ?
TCP_VAR5 = ?       # The value of this field is decimal for '0x50' which is the offset of 5 * 4 words = 20 and 0 for the reserve bit
TCP_VAR6 = ?
tcp_window = socket.htons(5620)  # maximum allowed window size
tcp_check = 0  # We will define the calculation for this further down
TCP_VAR9 = ?

# Pack the tcp header like you did with the IP header. Replace capitalized VAR names with what you used in the TCP header feilds, tcp_check and tcp_window has been provided. The "?"'s should be replaced with B, H or L. (B = Byte, H = Half-word, L = Word) 
tcp_header = pack('!?????????', VAR1, VAR2, VAR3, VAR4, VAR5, VAR6, tcp_window, tcp_check, VAR9)

# Create the message to be sent using the format b'message'
user_data = 

# After you create the tcp header, create pseudo header fields for the tcp checksum
source_address = socket.inet_aton( source_ip )
dest_address = socket.inet_aton(dest_ip)
reserved = 0
protocol = socket.IPPROTO_TCP
tcp_length = len(tcp_header) + len(user_data)

# Pack the pseudoheader. The "?"'s should be replaced with B, H or 4s. B=Byte, H=Half-word, 4s=four byte string
pseudo_header = pack('!???????' , source_address , dest_address , reserved , protocol , tcp_length)

# Combine the entire message with the pseudo header by adding the variables for the pseudo header, tcp header, and your user data
pseudo_header = ??? + ??? + ???

# checksum functions needed for calculation of tcp checksum (This has been done for you)
def checksum(data):

        s = 0
        n = len(data) % 2
        for i in range (0, len(data)-n, 2):
                s+= data[i] + (data[i+1] << 8)
        if n:
                s+= data[i+1]
        while (s >> 16):
                s = (s & 0xffff) + (s >> 16)
        s = ~s & 0xffff
        return s

# Recombine the tcp_check variable with the checksum definition calling the compiled pseudoheader
tcp_check = checksum(pseudo_header)

# Re-pack the tcp header to fill in the correct checksum - remember checksum is NOT in network byte order
tcp_header = pack('!???????' , VAR1, VAR2, VAR3, VAR4, VAR5, VAR6, tcp_window) + pack('H' , tcp_check) + pack('!?' , VAR9)

# final packet creation (combine the ip and tcp header with your user data)
packet = ??? + ??? + ???

# Sendto the target with the packet fully assembled (change OBJECT to the correct socket object)
s.OBJECT(packet, (dest_ip, 0))
