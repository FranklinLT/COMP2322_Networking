----------README----------


This project is written in python language, please use a compiler that supports python language to 
compile.

For browser side:
This server supports browser-side and code client-side requests. When using the browser for testing, 
you should run the client (Project_21101988D_LITong.py) first. This file can be run directly without
any external package. After successfully running, open the browser and enter the corresponding URL 
to access files or pictures. (It is recommended to use the URL in test_text.txt for access, such as 
"http://localhost:8000/", which is more convenient)
------------------------------------------------------------------------------------------------------


For code client side:
Since it is difficult for browsers to implement HEAD type requests and display the server's response,
if you want to view the server's response, you should use the code client for testing (client.py).

When testing with the code client, the server should be run first, and then the code client (the 
test_text.txt file also contains input samples for the code client and indicates expected results).
When testing multiple requests, you only need to run the code client multiple times without re-running
the server.
------------------------------------------------------------------------------------------------------


Notice:
1.The log file will be updated every time the server is run, if you open the log file directly before 
  running the server, you will see the last record

2.When done testing, manually kill the server and roll it out.

3.If you want to view the log file, you can find it in the "report" folder, the report is also in it!!

4.The folder ".idea" is generated by the compiler Pycharm

5.All the file that the server have is store in the folder "htdocs"