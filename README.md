# Axie-SLP-Tool
This tool is aimed at Axie Infinity Scholar Managers looking to streamline their workflow and optimize SLP management

The purpose of this tool is to speed up the process of SLP claims, transactions, and performance tracking of scholars within the NFT-Based online video game Axie Infinity.

## Features
1. **Automated SLP Claiming:** Automatically claim all SLP. The program will cycle through every account and attempt to claim SLP if available.

2. **Automated Payouts:** Execute SLP transactions which split the SLP between the manager's and scholar's Ronin addresses. Payout percentage can be easily changed and set to reward scholars who are overperforming. The software will also verify each transaction; if a transaction takes too long to verify, it will be marked as failed and skipped.

3. **Comprehensive Logging System:** Includes a date-stamped logging system organized into appropriate folders within `/logs/`.

4. **Performance Logger:** Automatically logs scholars considered to be underperforming based on the value defined in 'LowPerformanceValue'. This feature can be used to easily identify scholars who may require additional training.

## Setting up the Necessary Configuration
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

## Dependencies ##
This software requires several dependencies before it can be installed. This installation guide is for *Windows operating systems only*.

*This installation guide is for Windows operating systems only*

**Install the following dependencies in the following order**

## Dependencies

This software requires several dependencies before it can be installed. This installation guide is for *Windows operating systems only*.

**Install the following dependencies in the following order:**

1. [Python 3.8 or later version](https://www.python.org/downloads/release/python-380/)
2. pip (package-management system)
3. [Visual Studio 2019 Community Edition](https://visualstudio.microsoft.com)
4. Poetry

After installing the dependencies, clone the repository and follow the setup instructions provided in the repository to configure and run the software.
