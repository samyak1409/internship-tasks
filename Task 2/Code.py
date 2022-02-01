"""
For the next task can you pull up the transactions data for Cosmos. You can use their API to do so. The information is documented here: https://v1.cosmos.network/rpc/v0.41.4

Looks like the lowest height of the block is  5200791. With proper sleep times you just need a for loop to make calls to this (https://api.cosmos.network/blocks/5200791) where the block number will be increasing by 1 in next API call until 6,303,244. You need to read he json and keep adding to your dataframe and then write in a CSV.
"""
