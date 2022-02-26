# Task 6

This directory contains the code which extracts all the blocks' details (~2.5M) & their transaction details (~5M) of 
[Gridcoin](https://en.wikipedia.org/wiki/Gridcoin) from [Gridcoin.Network](https://gridcoin.network) 
(an independent Gridcoin block explorer) [API](https://gridcoin.network/api.html).


## Time required to pull the data

[2.5M (blocks) + 5M (transactions)] * 1 (request/query) * 1s (avg. time/request) = 87 days

*BUT, as we're using [threading](https://docs.python.org/3/library/threading.html) here,*

= 87 days / 100 ([no. of threads](https://github.com/samyak1409/internship-tasks/blob/main/Task%206/Code.py#L30))

= **21 h** (assuming 100 threads successfully execute in a second)
