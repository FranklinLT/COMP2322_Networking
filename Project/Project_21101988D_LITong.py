# Implements a simple HTTP Server
import socket
import os
import time
import datetime
import threading


# This function is called when the server encounters a 404 error, indicating that the requested
def not_found():
    fin = open('htdocs/404test.html')
    content = fin.read()
    fin.close()
    return 'HTTP/1.1 404 Not Found\n\n' + content


# This function is called when the server receives a request for a resource that has not been modified
def not_modified():
    fin = open('htdocs/304test.html')
    content = fin.read()
    fin.close()
    return content


# This function is used to find out the last time that a client get the file, if the client have not
# got the file before, the string "last_get_time" will be set to "no"
def cache_check(headers):
    last_get_time = 'no'
    for sen in headers:
        type = sen.split(' ', 1)
        if type[0] == 'if-modified-since:':
            last_get_time = type[1]
        else:
            continue

    return last_get_time


# This function compares the last modified time of a file with the if-modified-since time
# by changing them into timestamp and return a bool value
def time_compare(last_time, file_name):
    f = time.strftime("%a, %d %b %Y %I:%M:%S GMT", time.gmtime(os.path.getmtime('htdocs' + file_name)))
    print(f)
    print(last_time)
    f1 = datetime.datetime.strptime(f, "%a, %d %b %Y %I:%M:%S GMT").timestamp()
    f2 = datetime.datetime.strptime(last_time, "%a, %d %b %Y %I:%M:%S GMT").timestamp()
    return f1 > f2


# This function is used to format the information of output, which including response type, date,
# last-modified time, content length and content type
def output(res_type, file_name, file_type):
    file_len = os.path.getsize('htdocs' + file_name)
    date = time.strftime("%a, %d %b %Y %I:%M:%S GMT", time.localtime())
    date = date + '\n'
    last_m = time.strftime("%a, %d %b %Y %I:%M:%S GMT", time.gmtime(os.path.getmtime('htdocs' + file_name)))
    if file_type == 'html':
        content_type = 'Content_Type: text/html\n\n'
    else:
        content_type = 'Content_Type: application/x-png\n\n'
    return res_type + 'Date: ' + date + 'Last_Modified: ' + last_m + '\n' + 'Content_length: ' \
        + str(file_len) + '\n' + content_type


# this function is the main part of the code, make it as a function because the use of multithreading
# this function describe the basic logic of the code, It will call the functions introduced before
# and use them appropriately to handle a single received request.
def Single_thread(client_connection,client_address):
    IP_address = '-'
    access_time = '-'
    requested_file = '-'
    response_type = '-'

    # Wait for client connections
    access_time = time.strftime("%a, %d %b %Y %I:%M:%S GMT", time.localtime())
    IP_address = client_address[0]

    # Get the client request
    request = client_connection.recv(1024).decode()
    print('request:\n')
    print(request)

    # Split the request
    try:
        headers = request.split("\\n")
        fields = headers[0].split()
        request_type = fields[0]
        filename = fields[1]
    except IndexError:
        response = 'HTTP/1.1 400 Bad Request\n\nRequest Not Supported'.encode()
        response_type = 'HTTP/1.1 400 Bad Request\n'

    # Parse the request type and give the reasonable response
    if request_type == 'GET':
        # Get the content of the file
        if filename == '/':
            filename = '/index.html'
        try:
            file_type = filename.split('.')
            last_time = cache_check(headers)
            if file_type[1] == 'html' and last_time != 'no':
                if time_compare(last_time, filename):
                    fin = open('htdocs' + filename)
                    content = fin.read()
                    fin.close()
                    response = (output('HTTP/1.1 200 OK\n',  filename, file_type[1]) + content).encode()
                    response_type = 'HTTP/1.1 200 OK\n'
                else:
                    response = (output('HTTP/1.1 304 Not Modified\n', filename, file_type[1])
                                + not_modified()).encode()
                    response_type = 'HTTP/1.1 304 Not Modified\n'
            elif file_type[1] == 'html' and last_time == 'no':
                fin = open('htdocs' + filename)
                content = fin.read()
                fin.close()
                response = (output('HTTP/1.1 200 OK\n', filename, file_type[1]) + content).encode()
                response_type = 'HTTP/1.1 200 OK\n'
            elif file_type[1] != 'html' and last_time == 'no':
                fin = open('htdocs' + filename, 'rb')
                content = fin.read()
                fin.close()
                response = output('HTTP/1.1 200 OK\n', filename, file_type[1])
                response_type = 'HTTP/1.1 200 OK\n'
                client_connection.sendall(response.encode())
                response = content
            else:
                if time_compare(last_time, filename):
                    fin = open('htdocs' + filename, 'rb')
                    content = fin.read()
                    fin.close()
                    response = output('HTTP/1.1 200 OK\n', filename, file_type[1])
                    response_type = 'HTTP/1.1 200 OK\n'
                    client_connection.sendall(response.encode())
                    response = content
                else:
                    response = (output('HTTP/1.1 304 Not Modified\n', filename, file_type[1])
                                + not_modified()).encode()
                    response_type = 'HTTP/1.1 304 Not Modified\n'
        except FileNotFoundError:
            response = not_found().encode()
            response_type = 'HTTP/1.1 404 Not Found\n'
    elif request_type == 'HEAD':
        if filename == '/':
            filename = '/index.html'
        try:
            file_type = filename.split('.')
            last_time = cache_check(headers)
            if file_type[1] == 'html' and last_time != 'no':
                if time_compare(last_time, filename):
                    fin = open('htdocs' + filename)
                    fin.close()
                    response = output('HTTP/1.1 200 OK\n', filename, file_type[1]).encode()
                    response_type = 'HTTP/1.1 200 OK\n'
                else:
                    response = (output('HTTP/1.1 304 Not Modified\n', filename, file_type[1])
                                + not_modified()).encode()
                    response_type = 'HTTP/1.1 304 Not Modified\n'
            elif file_type[1] == 'html' and last_time == 'no':
                fin = open('htdocs' + filename)
                fin.close()
                response = output('HTTP/1.1 200 OK\n', filename, file_type[1]).encode()
                response_type = 'HTTP/1.1 200 OK\n'
            elif file_type[1] != 'html' and last_time == 'no':
                fin = open('htdocs' + filename, 'rb')
                fin.close()
                response = output('HTTP/1.1 200 OK\n', filename, file_type[1]).encode()
                response_type = 'HTTP/1.1 200 OK\n'
            else:
                if time_compare(last_time, filename):
                    fin = open('htdocs' + filename, 'rb')
                    fin.close()
                    response = output('HTTP/1.1 200 OK\n', filename, file_type[1]).encode()
                    response_type = 'HTTP/1.1 200 OK\n'
                else:
                    response = (output('HTTP/1.1 304 Not Modified\n', filename, file_type[1])
                                + not_modified()).encode()
                    response_type = 'HTTP/1.1 304 Not Modified\n'
        except FileNotFoundError:
            response = not_found().encode()
            response_type = 'HTTP/1.1 404 Not Found\n'
    else:
        response = 'HTTP/1.1 400 Bad Request\n\nRequest Not Supported'.encode()
        response_type = 'HTTP/1.1 400 Bad Request\n'

    # write information to a log file in a specific format
    client_connection.sendall(response)
    requested_file = filename
    log = open('report/log file.txt', 'a+')
    log.write('{: <25}'.format(IP_address))
    log.write('{: <32}'.format(access_time))
    log.write('{: <26}'.format(requested_file.strip('/')))
    log.write(response_type)
    log.close()

    # Close connection
    client_connection.close()


# Final part of the Project
# server_socket.close()


def main():
    # Define socket host and port
    SERVER_HOST = 'localhost'
    SERVER_PORT = 8000
    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    print('Listening on port %s ...' % SERVER_PORT)

    # open log file and write in the title
    log = open('report/log file.txt', 'w+')
    log.write(
        '--------------------------------------------------log file------------------------------------------------\n')
    log.write('Hostname/IP address      access time                     requested file name       response type\n')
    log.close()
    while True:
        client_connection, client_address = server_socket.accept()

        # Make the program multithread
        thread = threading.Thread(target=Single_thread, args=(client_connection,client_address,))
        thread.start()


# run the whole code
main()
