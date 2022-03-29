# Task 6.1

This directory contains the code which extracts some data of all the blocks (~8M) from 
[Filfox](https://filfox.info) (a Filecoin blockchain explorer and data service platform) 
[API](https://filfox.info/api/v1).


## Time required to pull the data

8M (Blocks) * 1 (Request/Block) * 1s (Avg. Time/Request) = ~3 months

But as we are using Threading here,

3 Months / 100 (Threads Executing/Second) = **~1 day**
