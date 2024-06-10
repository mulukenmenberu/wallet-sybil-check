import requests
from collections import Counter

# Replace with your Etherscan API key
API_KEY = '67ZMHJDQPV3HXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

def get_transactions(wallet_address):
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=99999999&sort=asc&apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('result', [])
    else:
        print(f"Error: {response.status_code}")
        return []

def find_interacting_wallets(transactions):
    interacting_wallets = set()
    for tx in transactions:
        if tx['from'].lower() == wallet_address.lower():
            interacting_wallets.add(tx['to'].lower())
        elif tx['to'].lower() == wallet_address.lower():
            interacting_wallets.add(tx['from'].lower())
    return interacting_wallets

def check_sybil(wallet_address):
    transactions = get_transactions(wallet_address)
    interacting_wallets = find_interacting_wallets(transactions)
    return interacting_wallets

def analyze_interactions(wallet_address, interacting_wallets):
    # Analyze transaction patterns
    num_interactions = len(interacting_wallets)
    print(f"Number of interacting wallets: {num_interactions}")
    
    # Count interactions per wallet
    interaction_counts = Counter(interacting_wallets)
    most_common_interactions = interaction_counts.most_common(5)
    print("Top interacting wallets:")
    for wallet, count in most_common_interactions:
        print(f"Wallet: {wallet}, Count: {count}")

    # Check for circular transactions
    circular_transactions = [tx for tx in transactions if tx['from'].lower() in interacting_wallets and tx['to'].lower() in interacting_wallets]
    num_circular_transactions = len(circular_transactions)
    print(f"Number of circular transactions: {num_circular_transactions}")

    # Check for proxy wallets
    proxy_wallets = set()
    for tx in transactions:
        if tx['from'].lower() == wallet_address.lower() and tx['to'].lower() in interacting_wallets:
            proxy_wallets.add(tx['to'].lower())
        elif tx['to'].lower() == wallet_address.lower() and tx['from'].lower() in interacting_wallets:
            proxy_wallets.add(tx['from'].lower())
    num_proxy_wallets = len(proxy_wallets)
    print(f"Number of potential proxy wallets: {num_proxy_wallets}")

    # Determine if suspicious activity is detected
    suspicious_activity = False
    if num_interactions > 10:
        print("Warning: High number of interactions.")
        suspicious_activity = True
    if num_circular_transactions > 0:
        print("Warning: Circular transactions detected.")
        suspicious_activity = True
    if num_proxy_wallets > 0:
        print("Warning: Proxy wallets detected.")
        suspicious_activity = True
    
    return suspicious_activity

# Example usage
wallet_address = '0x0b2c0240719CAfCXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
interacting_wallets = check_sybil(wallet_address)

if interacting_wallets:
    transactions = get_transactions(wallet_address)
    suspicious_activity = analyze_interactions(wallet_address, interacting_wallets)
    if suspicious_activity:
        print("Potential Sybil behavior detected.")
    else:
        print("No suspicious activity detected.")
else:
    print("No interactions found for the specified wallet address.")
