import brownie
from brownie import Contract
from brownie import config
    
# TODO: Add tests that show proper migration of the strategy to a newer one
#       Use another copy of the strategy to simulate the migration
#       Show that nothing is lost!


def test_migration(token, vault, strategy, strategist, gov, whale, StrategyCurveIBVoterProxy):
    # Put some funds into current strategy
    amount = token.balanceOf(whale)
    token.approve(vault.address, amount, {"from": whale})
    vault.deposit(amount, {"from": whale})
    strategy.setOptimal(0)
    strategy.harvest({"from": strategist})
    assert strategy.estimatedTotalAssets() == amount

    # migrate to a new strategy, but can effectively re-deploy existing strategy to serve as second strategy
    new_strategy = strategist.deploy(StrategyCurveIBVoterProxy, vault)
    strategy.migrate(new_strategy.address, {"from": gov})
    assert new_strategy.estimatedTotalAssets() == amount
    assert strategy.estimatedTotalAssets() == 0
    
    
