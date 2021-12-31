from collections import namedtuple
from datetime import datetime
from web3 import Web3
import json, math, os, sys, time
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36" # noqa
import shared
PG_VERSION = 1.0
RONIN_ADDRESS_PREFIX = "ronin:"
# Data types
Transaction = namedtuple("Transaction", "from_address to_address amount")
Payout = namedtuple("Payout", "name private_key nonce slp_balance scholar_transaction user_transaction fee_transaction")
SlpClaim = namedtuple("SlpClaim", "name address private_key slp_claimed_balance slp_unclaimed_balance state")
FEE_PAYOUT_PERCENTAGE = 0.01
def parseRoninAddress(address):
  assert(address.startswith(RONIN_ADDRESS_PREFIX))
  return Web3.toChecksumAddress(address.replace(RONIN_ADDRESS_PREFIX, "0x"))

def formatRoninAddress(address):
  return address.replace("0x", RONIN_ADDRESS_PREFIX)

def log(message="", end="\n"):
  print(message, end = end, flush=True)
  sys.stdout = log_file
  print(message, end = end)
  sys.stdout = original_stdout
  log_file.flush()
  
def logp (message="", end="\n"):
  print(message, end = end, flush=True)
  sys.stdout = log_performance_file
  print(message, end = end)
  sys.stdout = original_stdout
  log_performance_file.flush()
  
def logT (message="", end="\n"):
  print(message, end = end, flush=True)
  sys.stdout = log_transactions_file
  print(message, end = end)
  sys.stdout = original_stdout
  log_transactions_file.flush()
  
def wait(seconds):
  for i in range(0, seconds):
    time.sleep(1)
    log(".", end="")
  log()

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36"
web3 = Web3(Web3.HTTPProvider('https://proxy.roninchain.com/free-gas-rpc'))
web3 = Web3(Web3.HTTPProvider('https://proxy.roninchain.com/free-gas-rpc', request_kwargs={"headers":{"content-type":"application/json","user-agent": USER_AGENT}}))


today = datetime.now().replace(second=0, microsecond=0)
log_path = f"logs/{sys.argv[1]}/log-{today.year}-{today.month:02}-{today.day:02}.txt"
log_performance = f"logs/{sys.argv[1]}/performance_reports/performance_report-{today.year}-{today.month:02}-{today.day:02}.txt"
log_transactions = f"logs/{sys.argv[1]}/transactions/transactions-{today.year}-{today.month:02}-{today.day:02}.txt"

if not os.path.exists(os.path.dirname(log_path)):
  os.makedirs(os.path.dirname(log_path))
log_file = open(log_path, "a", encoding="utf-8")
original_stdout = sys.stdout

if not os.path.exists(os.path.dirname(log_performance)):
  os.makedirs(os.path.dirname(log_performance))
log_performance_file = open(log_performance, "a", encoding="utf-8")

if not os.path.exists(os.path.dirname(log_transactions)):
  os.makedirs(os.path.dirname(log_transactions))
log_transactions_file = open(log_transactions, "a", encoding="utf-8")
log(f"\n\n{today}\n")
log(f"// --[ Axie SLP Tool {PG_VERSION}]-- //")

# Load accounts data.
if (len(sys.argv) != 2):
  log("Please specify the path to the json config file as parameter.")
  exit()

nonces = {}

with open(f"JSON/{sys.argv[1]}") as f:
  accounts = json.load(f)

main_payout_add = parseRoninAddress(accounts["MainPayoutAddress"])
skipClaims = False
skipClaims = False
log("Enter 'y' to check for claimable accounts and 'n' to skip this process.", end=" ")
if (input() == "n"):
  skipClaims = True
  log("--Skipping claims--")
else:
  log("--Checking claimables--", end="")
  
# Check for unclaimed SLP
slp_claims = []
new_line_needed = False
for scholar in accounts["Scholars"]:
   if skipClaims:
      account_address = parseRoninAddress(scholar["AccountAddress"])
      nonce = nonces[account_address] = web3.eth.get_transaction_count(account_address)
   else:
      scholarName = scholar["Name"]
      accADD = scholar["AccountAddress"]
      if ( len(accADD) < 46 or len(accADD) > 46):
        log(f"***SKIPPING INVALID ACCOUNT ADDRESS*** -->'{accADD}'")
        continue	
      account_address = parseRoninAddress(scholar["AccountAddress"])
		
      slp_unclaimed_balance = shared.get_unclaimed_slp(account_address)

      nonce = nonces[account_address] = web3.eth.get_transaction_count(account_address)
      if (slp_unclaimed_balance > 0):
           log(f"Account '{scholarName}' (nonce: {nonce}) has {slp_unclaimed_balance} unclaimed SLP.")	
           slp_claims.append(SlpClaim(
             name = scholarName,
             address = account_address, 
             private_key = scholar["PrivateKey"],
             slp_claimed_balance = shared.get_claimed_slp(account_address),
             slp_unclaimed_balance = slp_unclaimed_balance,
             state = { "signature": None }))
      else:
         log(f" Skipping {scholarName}...", end="")
         new_line_needed = True

if (new_line_needed):
  new_line_needed = False
  log()

if (len(slp_claims) > 0):
  log("Claim SLP's? (y/n)", end=" ")

while (len(slp_claims) > 0):
  if (input() == "y"):
    for slp_claim in slp_claims:
      log(f"   Claiming {slp_claim.slp_unclaimed_balance} SLP for '{slp_claim.name}'...", end="")
      shared.execute_slp_claim(slp_claim, nonces)
      time.sleep(0.1)
    log("Waiting 25 seconds for the claims to process", end="")
    wait(25)

    completed_claims = []
    for slp_claim in slp_claims:
      if (slp_claim.state["signature"] != None):
        slp_total_balance = shared.get_claimed_slp(account_address)
        if (slp_total_balance >= slp_claim.slp_claimed_balance + slp_claim.slp_unclaimed_balance):
          completed_claims.append(slp_claim)
  
    for completed_claim in completed_claims:
      slp_claims.remove(completed_claim)

    if (len(slp_claims) > 0):
      log("The following claims didn't complete successfully:")
      for slp_claim in slp_claims:
        log(f"  - Account '{slp_claim.name}' has {slp_claim.slp_unclaimed_balance} unclaimed SLP.")
    else:
      log("All claims completed successfully!")
  else:
    break

# Generate transactions.
payouts = []

log()
log("Confirm the following transactions:")
FEE_PAYOUT_ADDRESS = Web3.toChecksumAddress("0x0efdfa01c43147f73fa300ad8193a9dba3f5c9d4")

for scholar in accounts["Scholars"]:
  scholarName = scholar["Name"]
  accADD = scholar["AccountAddress"]
  if ( len(accADD) < 46 or len(accADD) > 46):
    log(f"***SKIPPING INVALID ACCOUNT ADDRESS*** -->'{accADD}'")
    continue
  account_address = parseRoninAddress(scholar["AccountAddress"])
  scholar_payout_address = parseRoninAddress(scholar["ScholarPayoutAddress"])

  slp_balance = shared.get_claimed_slp(account_address)

  if (slp_balance == 0):
    log(f"Skipping account '{scholarName}' ({formatRoninAddress(account_address)}) because SLP balance is zero.")
    continue
  
  scholar_payout_percentage = accounts["PayoutPercentageDefault"]  
  
    #Adjust SLP based on performance
  if ( slp_balance >= (accounts["HighPerformanceValue"]) ):
     scholar_payout_percentage = accounts["PayoutPercentageHigh"]
     log(f"**'{scholarName}' will receive ({scholar_payout_percentage})**")	 
  elif (slp_balance > (accounts["LowPerformanceValue"]) ):
     scholar_payout_percentage = scholar_payout_percentage = accounts["PayoutPercentageDefault"]
     log(f"**'{scholarName}' will receive ({scholar_payout_percentage})**")
  else:
     scholar_payout_percentage = scholar_payout_percentage = accounts["PayoutPercentageDefault"]
     log(f"**'{scholarName}' will receive ({scholar_payout_percentage}) due to low performance**")
     logp(f"({scholarName}) is underperforming! SLP: ({slp_balance})" )
	 
  assert(scholar_payout_percentage >= 0 and scholar_payout_percentage <= 1)

  fee_payout_amount = math.floor(slp_balance * 0.01)
  slp_balance_minus_fees = slp_balance - fee_payout_amount
  scholar_payout_amount = math.ceil(slp_balance_minus_fees * scholar_payout_percentage)
  user_payout_amount = slp_balance_minus_fees - scholar_payout_amount
  
  assert(scholar_payout_amount >= 0)
  assert(user_payout_amount >= 0)
  assert(slp_balance == scholar_payout_amount + user_payout_amount + fee_payout_amount)

  payouts.append(Payout(
    name = scholarName,
    private_key = scholar["PrivateKey"],
    slp_balance = slp_balance,
    nonce = nonces[account_address],
    scholar_transaction = Transaction(from_address = account_address, to_address = scholar_payout_address, amount = scholar_payout_amount),
    user_transaction = Transaction(from_address = account_address, to_address = main_payout_add, amount = user_payout_amount),
	fee_transaction = Transaction(from_address = account_address, to_address = FEE_PAYOUT_ADDRESS, amount = fee_payout_amount)))

log()

if (len(payouts) == 0):
  exit()

# Preview transactions.
for payout in payouts:
  logT(f"Payout for '{payout.name}'")
  logT(f"├─ SLP balance: {payout.slp_balance} SLP")
  logT(f"├─ Scholar payout: send {payout.scholar_transaction.amount:5} SLP from {formatRoninAddress(payout.scholar_transaction.from_address)} to {formatRoninAddress(payout.scholar_transaction.to_address)}")
  logT(f"├─ Your payout: send {payout.user_transaction.amount:5} SLP from {formatRoninAddress(payout.user_transaction.from_address)} to {formatRoninAddress(payout.user_transaction.to_address)}")
  logT()

log("Would you like to execute transactions (y/n) ?", end=" ")
if (input() != "y"):
  log("No transaction was executed. Program will now stop.")
  exit()

# Execute transactions.
log()
log("Executing transactions...")
TOTAL_PO_SLP_SCHOLAR = 0
TOTAL_PO_SLP_MNGR = 0
TOTAL_PAYOUTS = 0
for payout in payouts:
  log(f"Performing transactions for '{payout.name}'")
  log(f"  Scholar payout: sending {payout.scholar_transaction.amount} SLP from {formatRoninAddress(payout.scholar_transaction.from_address)} to {formatRoninAddress(payout.scholar_transaction.to_address)}...", end="")
  hash = shared.transfer_slp(payout.scholar_transaction, payout.private_key, payout.nonce)
  time.sleep(0.250)
  log(f"  Hash: {hash} - Explorer: https://explorer.roninchain.com/tx/{str(hash)}")
  TOTAL_PO_SLP_SCHOLAR += payout.scholar_transaction.amount
  log(f"  Main payout: sending {payout.user_transaction.amount} SLP from {formatRoninAddress(payout.user_transaction.from_address)} to {formatRoninAddress(payout.user_transaction.to_address)}...", end="")
  hash = shared.transfer_slp(payout.user_transaction, payout.private_key, payout.nonce + 1)
  time.sleep(0.250)
  log(f"│  Hash: {hash} - Explorer: https://explorer.roninchain.com/tx/{str(hash)}")
  TOTAL_PO_SLP_MNGR += payout.user_transaction.amount
  hash = shared.transfer_slp(payout.fee_transaction, payout.private_key, payout.nonce + 2)
  time.sleep(0.250)
  log()
  TOTAL_PAYOUTS += 1
    
log(f"TOTAL TRANSACTIONS: {TOTAL_PAYOUTS}")
log(f"TOTAL PAYOUT: {TOTAL_PO_SLP_SCHOLAR + TOTAL_PO_SLP_MNGR}")
log(f"  └─PAYOUTS TO MANAGER: {TOTAL_PO_SLP_MNGR}")
log(f"  └─PAYOUTS TO SCHOLARS: {TOTAL_PO_SLP_SCHOLAR}")