# Task 4.1

This directory contains the code which extracts the transactions' data of all the blocks (~125M) of 
[Solana](https://en.wikipedia.org/wiki/Solana_(blockchain_platform)) from 
[Solscan](https://solscan.io) (the user-friendly and real-time update Scanning Tool for the Solana Ecosystem) 
[API](https://api.solscan.io/docs).


## Time required to pull the data

125M (Blocks) * 1 (Request/Block) * 1s (Avg. Time/Request) = **~4 years 💀**

BUT, as we're using threading here, time will depend on the internet speed.

Assuming it's enough to successfully execute 100 Threads/second 
i.e. speed = 1MB/s (for smallest blocks) to 100 MB/s (for largest blocks)
[possible with [5G](https://en.wikipedia.org/wiki/5G#Speed)!]:

125M (Blocks) * 1 (Request/Block) / 100 (Threads) * 1s (Avg. Time/100 Threads) = **~14 days**
