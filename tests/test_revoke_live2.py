import brownie
from brownie import Contract
from brownie import config

def test_revoke_live2(token, vault, strategyProxy, strategy, dudesahn, gaugeIB, voter, strategist_ms, whale, gov, chain, rando):
    # Simulate ydaddy approving my strategy on the StrategyProxy
    tx = strategyProxy.approveStrategy(strategy.gauge(), strategy, {"from": gov})
    tx.call_trace(True)

    # Deposit to the vault and harvest
    startingVault = token.balanceOf(vault)
    amount = 100 * (10 ** 18)
    token.transfer(rando, amount, {"from": whale})
    startingRando = token.balanceOf(rando)
    token.approve(vault.address, amount, {"from": rando})
    vault.deposit(amount, {"from": rando})
    strategy.harvest({"from": dudesahn})
    holdings = amount + startingVault
    
    print("\nStarting Vault Balance", startingVault) 
    # Check for any assets only in the vault, not in the strategy
    print("\nHoldings: ", holdings)
    old_assets_dai = vault.totalAssets()
    old_proxy_balanceOf_gauge = strategyProxy.balanceOf(gaugeIB)
    old_gauge_balanceOf_voter = gaugeIB.balanceOf(voter)
    old_strategy_balance = token.balanceOf(strategy)
    old_estimated_total_assets = strategy.estimatedTotalAssets()
    old_vault_balance = token.balanceOf(vault)
    # Check for any assets only in the vault, not in the strategy
    print("\nOld Vault Holdings: ", old_vault_balance)

    # Check total assets in the strategy
    print("\nOld Strategy totalAssets: ", old_estimated_total_assets)

    # Check total assets in the vault + strategy
    print("\nOld Vault totalAssets: ", old_assets_dai)

    # Want token should never be in the strategy
    print("\nOld Strategy balanceOf: ", old_strategy_balance)

    # These two calls should return the same value, and should update after every harvest call
    print("\nOld Proxy balanceOf gauge: ", old_proxy_balanceOf_gauge)
    print("\nOld gauge balanceOf voter: ", old_gauge_balanceOf_voter)
    
    assert strategy.estimatedTotalAssets() == holdings
    
    strategy.setEmergencyExit({"from": strategist_ms})
    strategy.harvest({"from": dudesahn})
    assert token.balanceOf(vault) == holdings

    # wait to allow share price to reach full value (takes 6 hours as of 0.3.2)
    chain.sleep(2592000)
    chain.mine(1)
    
    # give rando his money back, then he sends back to whale
    vault.withdraw({"from": rando})    
    assert token.balanceOf(rando) >= startingRando
    endingRando = token.balanceOf(rando)
    token.transfer(whale, endingRando, {"from": rando})
