#  imports SimpleXMLRPCServer class from the xmlrpc.server module -  to create an XML-RPC server easily.
from xmlrpc.server import SimpleXMLRPCServer
# Define the functions
# Factorial of a number 
def factorial(n):
    fact = 1
    for i in range(1, n+1):
        fact = fact * i
    return fact

# Addition of two numbers
def addition(n1, n2):
    return n1 + n2

# Square of a number
def square(n):
    sq = n*n
    return sq

# Set port number for server to 7500 
port = 7500

# creates an instance of SimpleXMLRPCServer that listens on localhost at the specified port. 
# The logRequests = False argument prevents the server from logging incoming requests.
server = SimpleXMLRPCServer(("localhost", port), logRequests=False)

# registers the factorial function with the server under the name 'factorial_rpc'. 
# This allows clients to call it remotely.
server.register_function(factorial, 'factorial_rpc')

# registers the square function with the server under the name 'square_rpc'.
server.register_function(square, 'square_rpc')

# registers the addition function with the server under the name 'addition_rpc'.
server.register_function(addition, 'addition_rpc')

# try block starts the server and puts it into an infinite loop to listen for incoming requests.
try:
    print("Starting and listening on the port", port)   #prints a message indicating that the server is running on the specified port.
    server.serve_forever()   #infinite loop

# except block catches any exceptions that occur during the server's operation, printing "Exit" if an error occurs.
except:
    print("Exit")