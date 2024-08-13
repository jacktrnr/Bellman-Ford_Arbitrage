import math
import requests
import networkx as nx
import matplotlib.pyplot as plt

# --- Editable Section ---
# Define the currencies to analyze
currencies = ['USD', 'EUR', 'GBP', 'INR', 'BRL', 'KRW', 'JPY', 'CNY']

# Define the threshold for detecting profitable arbitrage opportunities
threshold = 0.1  # 0.1% profit

# --- End of Editable Section ---

def get_real_time_rates(currencies):
    rates = []
    base_url = "https://api.exchangerate-api.com/v4/latest/"

    # Fetch exchange rates and build the rate matrix
    for i in range(len(currencies)):
        row = []
        for j in range(len(currencies)):
            if i == j:
                row.append(1)  # Exchange rate of a currency to itself is 1
            elif len(rates) > j and len(rates[j]) > i:  # Ensure reciprocal condition
                row.append(1 / rates[j][i])
            else:
                response = requests.get(base_url + currencies[i])
                data = response.json()
                rate = data['rates'][currencies[j]]
                row.append(rate)
        rates.append(row)
    
    return rates

def bellman_ford_arbitrage(currencies, rates, start_currency, threshold=0.1):
    V = len(currencies)
    start_index = currencies.index(start_currency)
    
    dist = [float('inf')] * V
    dist[start_index] = 0  # Start from the specified node
    predecessor = [-1] * V  # To store the path
    
    # Relax edges |V-1| times
    for _ in range(V-1):
        for u in range(V):
            for v in range(V):
                if dist[u] != float('inf') and dist[u] + rates[u][v] < dist[v]:
                    dist[v] = dist[u] + rates[u][v]
                    predecessor[v] = u
    
    # Check for negative-weight cycles
    for u in range(V):
        for v in range(V):
            if dist[u] != float('inf') and dist[u] + rates[u][v] < dist[v]:
                # If a negative cycle is detected, retrieve the path
                path = []
                start = v
                while start != -1 and start not in path:
                    path.append(start)
                    start = predecessor[start]
                path.append(start)
                path.reverse()

                # Ensure the path forms a loop
                if path[0] == path[-1] and path[0] == start_index:
                    # Calculate profit percentage
                    profit = 1.0
                    for i in range(len(path) - 1):
                        profit *= math.exp(-rates[path[i]][path[i+1]])
                    
                    profit_percentage = (profit - 1) * 100
                    
                    # Check if the profit exceeds the threshold
                    if profit_percentage > threshold:
                        return True, path, profit_percentage
    
    return False, [], 0.0

def visualize_network(currencies, rates, paths):
    G = nx.DiGraph()
    
    # Build the graph from the rate matrix
    for i in range(len(currencies)):
        for j in range(len(currencies)):
            if i != j:
                # Add edge without the weight and direction label
                G.add_edge(currencies[i], currencies[j], 
                           weight=round(rates[i][j], 4))

    # Use shell layout for better symmetry
    pos = nx.shell_layout(G)
    
    # Draw the nodes and edges (without edge labels)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=4000, font_size=12, font_weight='bold')
    
    # Highlight all paths
    colors = ['green', 'blue', 'red', 'orange', 'purple', 'brown', 'pink', 'cyan']
    for idx, path in enumerate(paths):
        path_edges = [(currencies[path[i]], currencies[path[i+1]]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color=colors[idx % len(colors)], width=4)
    
    plt.show()

# Get real-time exchange rates
exchange_rates = get_real_time_rates(currencies)

# Convert exchange rates to -log form for arbitrage detection
log_rates = [[-math.log(rate) for rate in row] for row in exchange_rates]

# Find and store the best loop for each starting currency
all_paths = []
for start_currency in currencies:
    arbitrage, path, profit_percentage = bellman_ford_arbitrage(currencies, log_rates, start_currency, threshold)
    if arbitrage:
        print(f"Arbitrage opportunity detected for {start_currency}!")
        print(f"Arbitrage path: {[currencies[node] for node in path]}")
        print(f"Expected profit: {profit_percentage:.2f}%\n")
        all_paths.append(path)
    else:
        print(f"No arbitrage opportunity detected for {start_currency}.\n")

# Visualize the network with all detected paths
visualize_network(currencies, exchange_rates, all_paths)
