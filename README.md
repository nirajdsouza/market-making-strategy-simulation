# Market Maker Simulation

This repository contains Python scripts that simulate a market maker's behavior, focusing on buying and selling assets at prices around a "fair value," with inventory and risk management.

## Code Overview

### MarketMaker Class
- **Cash & Inventory Management**: Tracks available funds and manages asset holdings.
- **Fair Value & Spread Calculation**: Computes asset's fair value and adjusts bid/ask prices based on market volatility.
- **Order Placement & Risk Management**: Places buy/sell orders and handles inventory risk.

### Versions
- **Code 1**: Dynamic spreads based on market volatility.
- **Code 2**: Fixed spreads with basic risk management.

## Requirements
Install the required libraries:
```bash
pip install matplotlib numpy
```
## How to Run
1.  Run the desired script:
    
	```bash
    python market_maker_code1.py  # For dynamic spreads
    python market_maker_code2.py  # For fixed spreads
    ```
    
3.  The simulation prints trade details and shows a plot of cash balance over time.

## Customization

Adjust parameters like initial cash, max inventory, spread, and simulation steps.

## License

[MIT](LICENSE) License.