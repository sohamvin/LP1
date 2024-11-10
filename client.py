import xmlrpc.client

# Connect to the server
proxy = xmlrpc.client.ServerProxy('http://localhost:7500/')

# Call factorial function
print("Factorial of 3 is:", proxy.factorial_rpc(3))

# Call square function
print("Square of 5 is:", proxy.square_rpc(5))

# Call addition function
print("Addition of 10 and 20 is:", proxy.addition_rpc(10, 20))
