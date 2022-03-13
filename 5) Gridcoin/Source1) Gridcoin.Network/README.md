# Task 6

This directory contains the code which extracts the details of all the blocks (~2.5M) & their transactions (~5M) from 
[Gridcoin.Network](https://gridcoin.network)(an independent Gridcoin block explorer) 
[API](https://gridcoin.network/api.html).


## Time required to pull the data

[2.5M (Blocks) + 5M (Transactions)] * 1 (Request/Block_or_Transaction) * 1s (Avg. Time/Request) = ~3 months

*BUT, as we're using [`threading`](https://docs.python.org/3/library/threading.html) here,*

= 3 months / 100 ([no. of threads](Code.py#L30))

= **~21 hours** (assuming 100 threads successfully execute in a second)
