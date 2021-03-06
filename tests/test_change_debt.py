import brownie
from brownie import Contract

def test_change_debt(gov, token, vault, strategy, strategist, amount, whale):
    # Deposit to the vault and harvest
    token.approve(vault.address, amount, {"from": whale})
    vault.deposit(amount, {"from": whale})
    half = amount / 2
    vault.updateStrategyDebtRatio(strategy.address, half, {"from": gov})
    strategy.setOptimal(0)
    strategy.harvest({"from": strategist})

    assert curve_proxy.balanceOf(gauge) == amount / 2

    vault.updateStrategyDebtRatio(strategy.address, amount, {"from": gov})
    strategy.harvest({"from": strategist})
    assert curve_proxy.balanceOf(gauge) == amount

    # In order to pass this tests, you will need to implement prepareReturn.
    # TODO: uncomment the following lines.
    # vault.updateStrategyDebtRatio(strategy.address, 5_000, {"from": gov})
    # assert token.balanceOf(strategy.address) == amount / 2


