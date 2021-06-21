import socket
import sys
import string
import re

# Author: Frank Tate
# Description:
# This is a VERY simple EIF (Event Integration Facility) listener written in Python.


# Here's what an Event looks like:
# two_unprintable_chars<START>>EVENT_TYPE;name1=value1;name2=value2;END<newline>
# So when the event is received, we just need to strip out the unprintable characters and it's ready for parsing.

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
printable = set(string.printable)
while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address
        data = connection.recv(4096)
        data1=filter(lambda x: x in printable, data)  # strip out unprintable chars
        data1=re.sub("<START.*?>>","",data1)
        data1=data1.replace(";END\n","")
        nvpairs=data1.split(";")
        for nvpair in nvpairs:
            nvp=nvpair.split("=")
            
            print >>sys.stderr, 'name %s' % nvp[0]
            if len(nvp) == 2:
                print >>sys.stderr, 'value %s' % nvp[1]
        
        
            
    finally:
        # Clean up the connection
        connection.close()
