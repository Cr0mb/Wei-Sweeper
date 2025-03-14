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

BLOCKCYPHER_API_URL = "https://api.blockcypher.com/v1/eth/main/addrs/{}"
ETHPLORER_API_URL = "https://api.ethplorer.io/getAddressInfo/{}?apiKey=freekey"

def generate_mnemonic(num_words=12):
    if num_words not in [12, 24]:
        raise ValueError(f"{Fore.RED}Error: Choose 12 or 24 words only{Style.RESET_ALL}")
    return Bip39MnemonicGenerator().FromWordsNumber(num_words)

def derive_eth_address(mnemonic):
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    bip44_eth = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
    eth_address = bip44_eth.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress()
    return to_checksum_address(eth_address), mnemonic.ToStr()

def check_eth_balance(address):
    try:
        url = BLOCKCYPHER_API_URL.format(address)
        response = requests.get(url, timeout=10)
        data = response.json()

        if "balance" in data:
            balance_wei = data["balance"]
            balance_eth = balance_wei / 1e18
            if balance_eth == 0:
                return 0, 0
            return balance_eth, balance_wei
    except Exception as e:
        print(f"BlockCypher API failed: {e}")

    try:
        url = ETHPLORER_API_URL.format(address)
        response = requests.get(url, timeout=10)
        data = response.json()

        if "ETH" in data and "balance" in data["ETH"]:
            balance_wei = int(data["ETH"]["balance"])
            balance_eth = balance_wei / 1e18
            return balance_eth, balance_wei
        else:
            print(f"Ethplorer API Error: Balance not found or other error")
            return None, None
    except Exception as e:
        print(f"Ethplorer API failed: {e}")
        return None, None

def save_wallet(mnemonic, address, balance_eth):
    with open("wallets.txt", "a") as f:
        f.write(f"Mnemonic: {mnemonic}\nAddress: {address}\nBalance: {balance_eth:.8f} ETH\n\n")

def generate_wallets(option):
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
