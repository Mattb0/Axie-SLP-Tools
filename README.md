# Axie-SLP-Tool
This software has been created to optimize solutions and to improve efficiency of Axie Infinity Scholar Managers by automating critical tasks.

The purpose of this tool is to speed up the process of SLP claims, transactions, and performance tracking of scholars within the NFT-Based online video game Axie Infinity.

## Features
1. Automatically claim all SLP. The program will cycle through every account and attempt to claim SLP, if available.

2. Automated payouts for scholars. Execute SLP transactions which splits the SLP between the manager's and scholar's ronin addresses. Payout percentage can be easily changed and can be set to reward scholars who are overperforming. Software will also verify each transaction, if a transaction takes too long to verify, it will be marked as failed and skipped.

3. Comprehensive logging system, which are date-stamped and organized into the appropriate folders found within /logs/

4. Performance logger capable of automatically logging scholars who considered to be under-performing based on the value defined in 'LowPerformanceValue'. This feature can be used to easily identify scholars who may require additional training.


## Setting up the neccesary configuration:
In order to run this program, the .JSON file located in root/JSON folder must be properly setup, and populated with the appropriate accounts.


 **MainPayoutAddress** 
 >Your/manager's ronin address where portion of the SLP will be sent to


**PayoutPercentageHigh**
>High percantage value allows you to set a custom percentage scholars who are performing well. If you do not need separate percentages for high performers, change this value to be the same as PayoutPercentageDefault and all of your scholars will receive the same SLP.
  
  
**LowPerformanceValue**
>Low performance value does not directly affect the payout value, however it is used to log accounts who are considered to be underperforming by your standards. 1200 indicates to the program that any scholar who has made less than or equal to 1200 SLP will be logged within logs/account.json/performance_reports. This does not change the payout value.

**HighPerformanceValue**
>High performance value is used determine the payout percentages. 

Example:

	HighPerformanceValue = 2000
	PayoutPercentageDefault 0.5 
	PayoutPercentageHigh = 0.6
	
	result:
	Any scholar below 2000 SLP will receive 0.5 (50%)
	Any scholar with 2000 SLP or above will receive 0.6 (60%)


## Dependencies ##
This software requires several dependencies before it can be installed.
*This installation guide is for Windows operating systems only*

**Install the following dependencies in the following order**

1. [python 3.8 or later version](https://www.python.org/downloads/release/python-380/)
2. pip (package-management system)
3. [Visual Studio 2019 Community Edition](https://visualstudio.microsoft.com)
4. poetry

