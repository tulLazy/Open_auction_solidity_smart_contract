from brownie import SimpleAuction
from scripts.helpful_scripts import get_account
from web3 import Web3
import time

# Testing in case there is not a  winner.
def testing_the_no_winner():
    address_0 = "0x0000000000000000000000000000000000000000"
    beneficiary = get_account()
    account_1 = get_account(1)
    account_2 = get_account(2)
    account_3 = get_account(3)
    account_4 = get_account(4)
    auction = SimpleAuction.deploy(10, beneficiary, {"from": beneficiary})
    assert auction.beneficiary() == beneficiary
    assert auction.owner() == beneficiary
    tx_bid_1st = auction.bid({"from": account_1, "value": Web3.toWei(0.1, "ether")})
    tx_bid_1st.wait(1)
    assert auction.pendingReturns(account_1) == 100000000000000000
    assert auction.highestBid() == 100000000000000000
    assert auction.highestBidder() == account_1
    tx_bid_2nd = auction.bid({"from": account_3, "value": Web3.toWei(0.2, "ether")})
    tx_bid_2nd.wait(1)
    assert auction.pendingReturns(account_1) == 100000000000000000
    assert auction.pendingReturns(account_3) == 200000000000000000
    assert auction.highestBid() == 200000000000000000
    assert auction.highestBidder() == account_3
    tx_withdraw_lowest = auction.withdraw({"from": account_1})
    tx_withdraw_lowest.wait(1)
    assert auction.pendingReturns(account_1) == 0
    assert auction.pendingReturns(account_3) == 200000000000000000
    assert auction.highestBid() == 200000000000000000
    assert auction.highestBidder() == account_3
    assert account_1.balance() == 100000000000000000000
    assert account_3.balance() == 99800000000000000000
    assert auction.ended() == False
    time.sleep(9)
    tx_withdraw_highest = auction.withdraw({"from": account_3})
    tx_withdraw_highest.wait(1)
    assert auction.pendingReturns(account_3) == 0
    assert auction.highestBid() == 0
    assert auction.highestBidder() == address_0
    tx_end = auction.auctionEnd({"from": beneficiary})
    tx_end.wait(1)
    assert beneficiary.balance() == 100000000000000000000
    assert auction.highestBid() == 0
    assert auction.highestBidder() == address_0
    assert auction.ended() == True
    assert account_1.balance() == 100000000000000000000
    assert account_3.balance() == 100000000000000000000
