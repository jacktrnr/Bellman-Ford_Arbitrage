# Bellman-Ford_Arbitrage
Application of the Bellman-Ford algorithm to find shortest loops in a ForEx arbitrage cycle.


# Forex Arbitrage Detection Script

This Python script, `forex.py`, is designed to detect arbitrage opportunities between different fiat currencies using the Bellman-Ford algorithm. The script calculates the possible profit from arbitrage loops and visualizes these opportunities using network graphs.

## How to Use

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/Bellman-Ford_Arbitrage.git
    cd forex-arbitrage
    ```

2. **Install Required Libraries**:
    Ensure you have the necessary Python libraries installed:
    ```bash
    pip install requests networkx matplotlib
    ```

3. **Run the Script**:
    Run the script with:
    ```bash
    python forex.py
    ```

## Editable Sections

The script includes clearly marked sections where you can customize its behavior:

- **Currencies**: Modify the `currencies` list to specify the fiat currencies you wish to analyze.
  ```python
  # Example currencies
  currencies = ['USD', 'EUR', 'GBP', 'INR', 'BRL', 'KRW', 'JPY', 'CNY']
  ```

- **Threshold**: Adjust the `threshold` variable to define the minimum profit percentage required to consider an arbitrage opportunity:
  ```python
  threshold = 0.1  # 0.1% profit
  ```

## Mathematical Background

The core of this script is based on the Bellman-Ford algorithm, which is used to find negative-weight cycles in a graph. In the context of forex trading, these cycles represent arbitrage opportunities. Here's a brief overview of the mathematical principles involved:

### Bellman-Ford Algorithm

Given a set of currencies and their exchange rates, the goal is to identify if there exists a sequence of trades that results in a net profit. The exchange rates are first transformed using the logarithm function:

`log_rates[i][j] = -log(rate[i][j])`

The negative logarithm of the exchange rate converts the problem into one of finding negative cycles in the graph.

#### Algorithm Steps

1. **Initialization**: 
    - Start with a source currency and set its distance to 0.
    - Set the distance to all other currencies as infinity.
  
    ```
    dist[i] = 0       if i = source
    dist[i] = infinity otherwise
    ```

2. **Relaxation**: 
    - For each currency pair `(u, v)`, update the distance if a shorter path is found:
    
    ```
    dist[v] = min(dist[v], dist[u] + log_rates[u][v])
    ```
  
3. **Cycle Detection**:
    - After `|V| - 1` relaxations (where `V` is the number of currencies), check for any negative cycles. A negative cycle indicates an arbitrage opportunity.
    
    ```
    if dist[v] > dist[u] + log_rates[u][v], then a negative cycle exists
    ```

4. **Profit Calculation**:
    - If a negative cycle is found, calculate the profit:
    
    ```
    profit = (exp(-sum(log_rates[i][j])) - 1) * 100%
    ```

### Visualization

The script visualizes the detected arbitrage opportunities using a directed graph where nodes represent currencies and edges represent exchange rates. The arbitrage paths are highlighted to show potential profit loops.

## License

This project is licensed under the MIT License.
