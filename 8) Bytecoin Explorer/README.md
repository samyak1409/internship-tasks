# Task 8

This directory contains the code which extracts some data 
of all the blocks (~3M) from [Bytecoin Explorer](https://explorer.bytecoin.org) 
(Official BCN explorer to track transactions and other Bytecoin network data).


## Time required to pull the data

3M (Blocks) * 1 (Request/Block) * 2s (Avg. Time/Request) = ~2 months

But as we are using Threading here,

2 Months / 100 (Threads Executing/Second) = **~16 hours**
