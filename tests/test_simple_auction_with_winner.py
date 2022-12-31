from brownie import SimpleAuction
from scripts.helpful_scripts import get_account
from web3 import Web3
import time

# Testing in case there is a winner.
def test_simple_auction_with_winner():
    address_0 = "0x0000000000000000000000000000000000000000"
    beneficiary = get_account()
    account_1 = get_account(1)
    account_2 = get_account(2)
    account_3 = get_account(3)
    account_4 = get_account(4)
    auction = SimpleAuction.deploy(10, beneficiary, {"from": beneficiary})
    assert auction.beneficiary() == beneficiary
    assert auction.owner() == beneficiary
    tx_bid_1st = auction.bid({"from": account_1, "value": Web3.toWei(2, "ether")})
    tx_bid_1st.wait(1)
    assert auction.highestBid() == 2000000000000000000
    assert auction.highestBidder() == account_1
    assert auction.pendingReturns(account_1) == 2000000000000000000
    tx_withdraw_1st = auction.withdraw({"from": account_1})
    tx_withdraw_1st.wait(1)
    assert auction.highestBid() == 0
    assert auction.highestBidder() == address_0
    assert auction.pendingReturns(account_1) == 0
    tx_bid_2nd = auction.bid({"from": account_2, "value": Web3.toWei(1, "ether")})
    tx_bid_2nd.wait(1)
    assert auction.highestBid() == 1000000000000000000
    assert auction.highestBidder() == account_2
    assert auction.pendingReturns(account_2) == 1000000000000000000
    tx_bid_3rd = auction.bid({"from": account_1, "value": Web3.toWei(1.5, "ether")})
    tx_bid_3rd.wait(1)
    assert auction.highestBid() == 1500000000000000000
    assert auction.highestBidder() == account_1
    assert auction.pendingReturns(account_1) == 1500000000000000000
    assert auction.pendingReturns(account_2) == 1000000000000000000
    tx_bid_4th = auction.bid({"from": account_3, "value": Web3.toWei(3, "ether")})
    tx_bid_4th.wait(1)
    assert auction.highestBid() == 3000000000000000000
    assert auction.highestBidder() == account_3
    assert auction.pendingReturns(account_3) == 3000000000000000000
    assert auction.pendingReturns(account_1) == 1500000000000000000
    assert auction.pendingReturns(account_2) == 1000000000000000000
    assert auction.ended() == False
    tx_withdraw_2nd = auction.withdraw({"from": account_1})
    tx_withdraw_2nd.wait(1)
    assert auction.highestBid() == 3000000000000000000
    assert auction.highestBidder() == account_3
    assert auction.pendingReturns(account_3) == 3000000000000000000
    assert auction.pendingReturns(account_1) == 0
    assert auction.pendingReturns(account_2) == 1000000000000000000
    assert account_1.balance() == 100000000000000000000
    assert auction.ended() == False
    time.sleep(9)
    tx_end = auction.auctionEnd({"from": beneficiary})
    tx_end.wait(1)
    assert auction.highestBid() == 0
    assert auction.highestBidder() == address_0
    assert auction.pendingReturns(account_3) == 0
    assert auction.pendingReturns(account_1) == 0
    assert auction.pendingReturns(account_2) == 0
    assert beneficiary.balance() == 103000000000000000000
    assert account_1.balance() == 100000000000000000000
    assert account_2.balance() == 100000000000000000000
    assert account_3.balance() == 97000000000000000000
    assert auction.ended() == True
