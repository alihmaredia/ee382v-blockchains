# README for Final Assignment

I've made a simple Python CLI tool that provides two useful features:   

(1) You can query basic data on for a Bitcoin address and collect a history of transactions in a tabular format.    
(2) Each Bitcoin address queried gets checked to see if it is on OFAC’s Specially Designated Nationals list.

To setup, there's two simple steps!     

(1) Make sure you have the dependencies installed in your Python 3 environment (you can leverage the requirements.txt file in the repo for this with pip install).    
(2) Run main.py (ie, python3 main.py using any command line tool).    

To use the tool or test it out, make sure to have a Bitcoin address handy. It doesn't have to be one on the OFAC sanctioned list, but once you run main.py, you'll see a prompt where you can select option 1 to input that Bitcoin address to see the basic information, and then from there you'll have another prompt where you can opt to look into transaction history (select option 1 again if you'd like to do that!).

Resources:    
https://github.com/INTERPOL-Innovation-Centre/GraphSense-Maltego-transform    
https://github.com/0xB10C/ofac-sanctioned-digital-currency-addresses    
https://github.com/coleplante16/Bitcoin-Analyzer    
