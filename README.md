![image](https://github.com/user-attachments/assets/0cab39e1-8f7b-4152-986e-ace7337632f3)
# Wei-Sweeper
Wei Sweeper is a Python script that generates Ethereum wallets, derives their addresses from BIP39 mnemonics, and checks their balances using the BlockCypher API. If a generated wallet has a non-zero balance, it is saved to a file.


## Features

- Generates Ethereum wallets with either 12 or 24-word BIP39 mnemonics
- Derives Ethereum addresses from the generated mnemonics
- Checks wallet balances using the BlockCypher API
- Saves wallets with non-zero balances to a file
- User-friendly CLI with colorized output


## Requirements
- Python 3
```
pip install requests colorama bip_utils eth_utils web3
```



## Disclaimer
> This script is for educational and research purposes only. The author is not responsible for any misuse or unethical activities performed using this tool.
