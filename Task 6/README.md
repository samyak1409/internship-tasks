# Task 6

This directory contains the code which extracts all the blocks' details (~2.5M) & their transaction details (~5M) of 
[Gridcoin](https://en.wikipedia.org/wiki/Gridcoin) from [Ǥridcoin.Network](https://gridcoin.network) 
(an independent Gridcoin block explorer).


## Time required to pull the data

[2.5M (blocks) + 5M (transactions)] * 1 (request/query) * 1s (avg. time/request) = 87 days

*BUT, as we're using [threading](https://docs.python.org/3/library/threading.html) here,*

= 87 days / 100 ([no. of threads](https://github.com/samyak1409/internship-tasks/blob/2d03bb156146826f030d4f819e9f83b8fca04de1/Task%206/Code.py#L30))

= **21 h** (assuming 100 threads successfully execute in a second)
