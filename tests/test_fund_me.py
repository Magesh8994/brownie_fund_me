from brownie.network import account
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENT
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_fund_me_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    enterance_fee = fund_me.getEntranceFee()
    tx = fund_me.fund({"form": account, "value": enterance_fee}) + 100
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == enterance_fee
    txt2 = fund_me.withdraw({"from": account})
    txt2.wait(1)


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        pytest.skip("only for local testing")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})


def main():
    test_fund_me_and_withdraw()
    test_only_owner_can_withdraw()
