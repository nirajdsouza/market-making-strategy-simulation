import random
import time
import matplotlib.pyplot as plt
import numpy as np

# Market Maker Class
class MarketMaker:
    def __init__(self, initial_cash, symbol, max_inventory=10, base_spread=0.05):
        self.cash = initial_cash
        self.symbol = symbol
        self.inventory = 0
        self.max_inventory = max_inventory  # Maximum allowed inventory to manage risk
        self.base_spread = base_spread  # Base spread used for quoting prices
        self.trading_history = []  # Track trades for analysis
        self.fair_value = 1050  # Initial fair value (can be updated dynamically)

    def calculate_fair_value(self, historical_prices):
        """
        Calculate the fair value based on historical prices (e.g., moving average).
        """
        self.fair_value = np.mean(historical_prices[-10:])  # 10-period moving average

    def calculate_spread(self, market_volatility):
        """
        Adjust spreads dynamically based on market volatility.
        """
        dynamic_spread = self.base_spread * (1 + market_volatility / 0.02)  # Adjust spread with volatility
        return dynamic_spread

    def place_order(self, market_price, market_volatility):
        """
        Place buy and sell orders around the fair value with dynamic spreads.
        """
        dynamic_spread = self.calculate_spread(market_volatility)
        bid_price = self.fair_value - dynamic_spread  # Buy price
        ask_price = self.fair_value + dynamic_spread  # Sell price

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

    def hedge_inventory_risk(self, correlated_asset_price):
        """
        Hedge inventory risk by trading a correlated asset.
        """
        if self.inventory > self.max_inventory:
            print("Hedging inventory risk using correlated asset.")
            hedge_price = correlated_asset_price
            hedge_amount = self.inventory - self.max_inventory
            self.cash += hedge_amount * hedge_price  # Assume a perfect hedge for simplicity
            self.inventory -= hedge_amount

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
    initial_cash=10000,
    symbol='BTC/USD',
    max_steps=50,
    delay=0.1,
    base_spread=0.05,
    max_inventory=10
):
    market_maker = MarketMaker(
        initial_cash=initial_cash,
        symbol=symbol,
        max_inventory=max_inventory,
        base_spread=base_spread,
    )

    # Track cash history for plotting
    cash_history = [market_maker.cash]

    # Simulated historical prices for fair value calculation
    historical_prices = [random.uniform(1000, 1100) for _ in range(10)]

    # Simulate for a number of time steps (or trades)
    for step in range(max_steps):
        # Simulate market price fluctuations
        market_price = random.uniform(1000, 1100)  # Random market price between $1000-$1100
        market_volatility = random.uniform(0.01, 0.03)  # Simulated volatility
        correlated_asset_price = random.uniform(500, 550)  # Simulated correlated asset price

        # Update historical prices and fair value
        historical_prices.append(market_price)
        market_maker.calculate_fair_value(historical_prices)

        print(f"\nStep {step + 1}: Market Price = {market_price:.2f}, Fair Value = {market_maker.fair_value:.2f}")

        # Execute market-making strategy
        market_maker.place_order(market_price, market_volatility)
        market_maker.hedge_inventory_risk(correlated_asset_price)  # Hedge risk using correlated asset
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
        max_steps=50,
        delay=0.1,
        base_spread=0.05,
        max_inventory=10,
    )
