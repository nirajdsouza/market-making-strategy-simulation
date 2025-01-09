import random
import time
import matplotlib.pyplot as plt

# Market Maker Class
class MarketMaker:
    def __init__(self, initial_cash, symbol, max_inventory=10, bid_spread=0.05, ask_spread=0.05):
        self.cash = initial_cash
        self.symbol = symbol
        self.inventory = 0
        self.max_inventory = max_inventory  # Maximum allowed inventory to manage risk
        self.bid_spread = bid_spread  # Spread between buy and market price
        self.ask_spread = ask_spread  # Spread between sell and market price
        self.trading_history = []  # Track trades for analysis

    def get_mid_price(self, market_price):
        """
        Calculate the mid price (average of current market price).
        """
        return market_price

    def place_order(self, market_price):
        """
        Place buy and sell orders around the mid-price.
        """
        mid_price = self.get_mid_price(market_price)
        bid_price = mid_price - self.bid_spread  # Buy price
        ask_price = mid_price + self.ask_spread  # Sell price

        # Simulate the order execution
        if random.random() < 0.5:
            # Buying logic
            if self.cash >= bid_price:  # Ensure sufficient cash for buying
                self.inventory += 1
                self.cash -= bid_price
                self.trading_history.append(('BUY', bid_price))
                print(f"Placed buy order at {bid_price:.2f} for {self.symbol}")
            else:
                print("Not enough cash to place a buy order.")
        else:
            # Selling logic
            if self.inventory > 0:  # Ensure there's inventory to sell
                self.inventory -= 1
                self.cash += ask_price
                self.trading_history.append(('SELL', ask_price))
                print(f"Placed sell order at {ask_price:.2f} for {self.symbol}")
            else:
                print("No inventory to place a sell order.")

    def manage_risk(self, market_price):
        """
        Risk management: Liquidate inventory if it exceeds certain limits.
        """
        if abs(self.inventory) > self.max_inventory:
            print("Liquidating inventory to manage risk.")
            liquidation_price = market_price  # Use the current market price for liquidation
            if self.inventory > 0:
                self.cash += self.inventory * liquidation_price
            else:
                self.cash -= abs(self.inventory) * liquidation_price
            self.trading_history.append(('LIQUIDATE', liquidation_price))
            self.inventory = 0

    def track_performance(self):
        """
        Track the performance of the trading strategy.
        """
        return self.cash, self.inventory, len(self.trading_history)


# Simulate Market Making Strategy
def simulate_market_making(
    initial_cash=10000, symbol='BTC/USD', max_steps=10, delay=1, bid_spread=0.05, ask_spread=0.05, max_inventory=10
):
    market_maker = MarketMaker(
        initial_cash=initial_cash,
        symbol=symbol,
        max_inventory=max_inventory,
        bid_spread=bid_spread,
        ask_spread=ask_spread,
    )

    # Track cash history for plotting
    cash_history = [market_maker.cash]

    # Simulate for a number of time steps (or trades)
    for step in range(max_steps):
        # Simulate market price fluctuations
        market_price = random.uniform(1000, 1100)  # Random market price between $1000-$1100
        print(f"\nStep {step + 1}: Market Price = {market_price:.2f}")

        # Execute market-making strategy
        market_maker.place_order(market_price)
        market_maker.manage_risk(market_price)  # Risk management: check for inventory levels

        # Append current cash to cash history
        cash_history.append(market_maker.cash)

        # Delay to simulate real-time trading
        time.sleep(delay)

    # Track final performance
    final_cash, final_inventory, total_trades = market_maker.track_performance()
    print(f"\nFinal Cash: ${final_cash:.2f}")
    print(f"Final Inventory: {final_inventory}")
    print(f"Total Trades Executed: {total_trades}")

    # Plot results: cash over time
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(cash_history)), cash_history, label="Cash Over Time")
    plt.xlabel("Time Step")
    plt.ylabel("Cash ($)")
    plt.title(f"Market Making Strategy: {symbol} Cash Over Time")
    plt.legend()
    plt.show()


# Main Execution
if __name__ == "__main__":
    simulate_market_making(
        initial_cash=10000,
        symbol='BTC/USD',
        max_steps=10,
        delay=1,
        bid_spread=0.05,
        ask_spread=0.05,
        max_inventory=10,
    )
