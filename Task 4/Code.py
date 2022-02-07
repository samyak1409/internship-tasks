coins = {'Namecoin': 'nmc', 'Emercoin': 'emc', 'Siacoin': 'sc', 'Gamecredits': 'game',
         'Peercoin': 'ppc', 'Feathercoin': 'ftc', 'Stratis': 'strat', 'Cosmos': 'atom'}

types = {'Tweets Cnt': 'daily_tweets_cnt', 'Active Address': 'daily_active_address',
         'New Address': 'daily_new_address', 'Block Cnt': 'daily_block_cnt',
         'Avg Difficulty': 'daily_avg_difficulty', 'Avg Hashrate': 'daily_avg_hashrate',
         'Fee': 'daily_fee', 'Fee Usd': 'daily_fee_usd',
         'Avg Block Fee': 'daily_avg_block_fee', 'Median Block Fee': 'daily_median_block_fee',
         'Avg Tx Fee': 'daily_avg_tx_fee', 'Avg Tx Fee Usd': 'daily_avg_tx_fee_usd',
         'Sent Value': 'daily_sent_value', 'Sent Value Usd': 'daily_sent_value_usd',
         'Median Block Sent Value': 'daily_median_block_sent_value', 'Avg Tx Value': 'daily_avg_tx_value',
         'Tx Cnt': 'daily_tx_cnt', 'Reward': 'daily_reward',
         'Reward Usd': 'daily_reward_usd', 'Mining Profitability': 'daily_mining_profitability',
         'Total Mined Coin': 'daily_total_mined_coin', 'Price': 'daily_price',
         'Marketcap': 'daily_marketcap', 'Gas Used': 'daily_gas_used',
         'Avg Gas Price': 'daily_avg_gas_price', 'Avg Gas Limit': 'daily_avg_gas_limit',
         'Avg Tx Gas Used': 'daily_avg_tx_gas_used', 'Sent Value Gas': 'daily_sent_value_gas',
         'Uncle Block Cnt': 'daily_uncle_block_cnt', 'Uncle Reward': 'daily_uncle_reward',
         'Uncle Reward Usd': 'daily_uncle_reward_usd', 'Uncle Total Mined Coin': 'daily_uncle_total_mined_coin'}


for coin_name, coin_sym in coins.items():

    print()
    print(coin_name)

    for type_key, type_val in types.items():

        link = f'https://{coin_sym}.tokenview.com/v2api/chart/?coin={coin_sym}&type={type_val}&splice=5000'
        print(f'{type_key}: {link}')
