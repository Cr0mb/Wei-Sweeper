These projects are intended solely for educational purposes to help individuals understand the principles of cryptography and blockchain technology. It is important to recognize that attempting to generate Bitcoin wallets in the hope of randomly finding one with a balance is not a feasible strategy. This same logic applies to any tool that tries to work in any way the same as this.

The number of possible Bitcoin wallet combinations exceeds 76 trillion, making the odds of discovering an active wallet astronomically low. To put it into perspective, you are statistically far more likely to win the lottery every day for the rest of your life than to recover even a single wallet with funds—even over the course of a decade.



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
