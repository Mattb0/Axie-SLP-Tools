# Axie-SLP-Tool
This tool is aimed at Axie Infinity Scholar Managers looking to streamline their workflow and optimize SLP management
The purpose of this tool is to speed up the process of SLP claims, transactions, and performance tracking of scholars within the NFT-Based online video game Axie Infinity.

1. [Features](#section-a)
2. [Configuration](#section-b)
3. [API Documentation for Developers](#section-c)
4. [Dependencies](#section-d)

## Features <a name="section-a"></a>
1. **Automated SLP Claiming:** Automatically claim all SLP. The program will cycle through every account and attempt to claim SLP if available.

2. **Automated Payouts:** Execute SLP transactions which split the SLP between the manager's and scholar's Ronin addresses. Payout percentage can be easily changed and set to reward scholars who are overperforming. The software will also verify each transaction; if a transaction takes too long to verify, it will be marked as failed and skipped.

3. **Comprehensive Logging System:** Includes a date-stamped logging system organized into appropriate folders within `/logs/`.

4. **Performance Logger:** Automatically logs scholars considered to be underperforming based on the value defined in 'LowPerformanceValue'. This feature can be used to easily identify scholars who may require additional training.

## Configuration<a name="section-b"></a>
In order to run this program, the `.JSON` file located in `root/JSON` folder must be properly set up and populated with the appropriate accounts.

- **MainPayoutAddress:** Your/manager's Ronin address where a portion of the SLP will be sent.
  
- **PayoutPercentageHigh:** Allows setting a custom percentage for scholars who are performing well. If not needed, change this value to be the same as PayoutPercentageDefault.

- **LowPerformanceValue:** Used to log accounts considered to be underperforming. Does not affect payout value.

- **HighPerformanceValue:** Used to determine the payout percentages.

Example:

```json
{
  "HighPerformanceValue": 2000,
  "PayoutPercentageDefault": 0.5,
  "PayoutPercentageHigh": 0.6
}
```

## API Documentation for Developers<a name="section-c"></a>

### Functions

#### get_claimed_slp(address)

- **Description**: Retrieves the claimed SLP (Smooth Love Potion) balance for a given Ethereum address.
- **Parameters**:
  - `address` (str): The Ethereum address for which to retrieve the claimed SLP balance.
- **Returns**:
  - `claimed_slp` (int): The amount of claimed SLP for the specified address.
  
#### get_unclaimed_slp(address)

- **Description**: Retrieves the unclaimed SLP (Smooth Love Potion) balance for a given Ethereum address.
- **Parameters**:
  - `address` (str): The Ethereum address for which to retrieve the unclaimed SLP balance.
- **Returns**:
  - `unclaimed_slp` (int): The amount of unclaimed SLP for the specified address.

#### execute_slp_claim(claim, nonces)

- **Description**: Executes the claiming of SLP (Smooth Love Potion) tokens for a specified address.
- **Parameters**:
  - `claim` (object): An object containing address, private key, and claim state information.
  - `nonces` (dict): A dictionary containing nonces for each address.
- **Returns**:
  - `txn_hash` (str): The transaction hash of the executed SLP claim transaction.

#### transfer_slp(transaction, private_key, nonce)

- **Description**: Transfers SLP (Smooth Love Potion) tokens to a specified address.
- **Parameters**:
  - `transaction` (object): An object containing transaction details such as recipient address and amount.
  - `private_key` (str): The private key of the sender's Ethereum address.
  - `nonce` (int): The nonce value for the transaction.
- **Returns**:
  - `txn_hash` (str): The transaction hash of the executed SLP transfer transaction.

#### sign_message(message, private_key)

- **Description**: Signs a message using the provided private key.
- **Parameters**:
  - `message` (str): The message to be signed.
  - `private_key` (str): The private key used for signing the message.
- **Returns**:
  - `signature` (str): The signature of the message signed with the private key.

#### get_jwt_access_token(address, private_key)

- **Description**: Retrieves a JWT access token using the provided Ethereum address and private key for authentication.
- **Parameters**:
  - `address` (str): The Ethereum address used for authentication.
  - `private_key` (str): The private key corresponding to the Ethereum address.
- **Returns**:
  - `access_token` (str): The JWT access token generated for authentication.

## Dependencies<a name="section-d"></a>

This software requires several dependencies before it can be installed. This installation guide is for *Windows operating systems only*.

**Install the following dependencies in the following order:**

1. [Python 3.8 or later version](https://www.python.org/downloads/release/python-380/)
2. [pip/package-management system](https://pypi.org/project/pip/)
3. [Visual Studio 2019 Community Edition](https://visualstudio.microsoft.com)
4. Poetry
