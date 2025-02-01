# optionsData

This code helps you analyze and compare options data for multiple stocks to make informed decisions about selling puts or calls. It first prompts you to input the stock tickers you're interested in and select an expiration date. Then, it fetches the current stock price and filters for out-of-the-money (OTM) call and put options. 

To help you assess the potential risks and rewards, the code calculates key metrics for each option:

* **Return %:**  How much money you could make relative to the strike price.
* **Move Needed %:** How much the stock price needs to change for the underlying to be at the strike price.
* **Move Needed/Return:** A ratio showing the risk-to-reward profile of the option.
* **Change R%:**  How the potential return changes between different strike prices.
* **Change P:** How the option price changes between different strike prices.

Finally, the code generates visualizations comparing these metrics across different stocks and option types, allowing you to identify potentially favorable opportunities for selling puts or calls based on your risk tolerance and market outlook.
