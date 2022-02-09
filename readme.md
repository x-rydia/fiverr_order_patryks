This strategy will use the bollinger bands in the manner that I
have found most intuitive and sucessful in a highly volatile environment. Simplicity here is the key design philosophy, working
under the assumption that the pairs traded will be incredibly volatile, this strategy can have very high success.

- If the price crosses the lower bollinger band, execute a 
  market buy order (Buy Low)

- If the price crosses the upper bollinger band, execute a 
  market sell order (Sell High)

If we shorten the period of the bolllinger bands, it will allow our trading 
logic to feed off of the higher volatility. Thus we make our profit not a 
function of price movenments but rather proportional to the volatility of the
asset. For stocks, this is not so advisable because of the stability the 
institutional investors give them. But for cryptocurrencies this is incredibly 
advantageous. 

This is not dissimilar from the logic used in grid trading strategies.
You may find--if you enjoy using this script--that you may want a grid
strategy made in the future to compement this strategy. I will intentionally 
strucutre the code so that a grid trading element could easily be incorportated by 
either myself or another developer.

This strategy relies on a few libraries in python, which need to be installed using 'pip.' Below is a tutorial on using pip:
-  Ensure that you are running python 3.XX

-  On Mac, go to your command line and type in "pip3 -V" [Note: the V must be 
capitalized] If no error pops up, then you are good. If not, re install python from
python.org 

- On windows, use the same command except "pip -V" [Note: no '3']
 
- After confirming that pip is installed, run all of the following commands:

- ON WINDOWS: "pip install pandas" "pip install ta" "pip install python-binance"

- ON MAC: "pip3 install pandas" "pip3 install ta" "pip3 install python-binance"

- If after running any command, an error pops up, check both your installation of pip and your spelling of the comand.

SETUP INSTRUCTIONS

- Follow the pip instructions.

- Set up all of the variables in the config.py file. Make sure that they are all valid api keys

- Ensure that the quantity unit is set to a reasonable unit to measure quantity. This
is the amount that will be exchanged on each signal. 

- Ensure that the tickers set in the config file are valid tickers.

IF YOU HAVE ANY QUESTIONS PLEASE CONTACT ME AND I WILL SORT THEM OUT FOR YOU.
