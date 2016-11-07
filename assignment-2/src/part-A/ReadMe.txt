Part-A

-----------------------------------------------------------------------------------------------------------------------------------------------------

Question 1:
Configuration parameters: Driver memory = 5G
                          Executor memory = 15G
                          4 Executor cores

lines : RDD created by reading input file, 100 partitions
<lines : (from-URL, to-URLs)>

ranks : RDD created by applying a map transformation on links (does not preserve parent RDD partitioning)
<ranks : (from-URL, 1.0)>

for each iteration :
    contributions : RDD created by applying join and flatMap transformations on links and ranks
    <contributions : from-URL -> (to_URL, contribution)>

    ranks : new RDD containing updated ranks => sum of contributions from other URLs
    <ranks : (to-URL, updated-rank)>

output : apply collect() action on ranks

-----------------------------------------------------------------------------------------------------------------------------------------------------

Question 2:
Configuration parameters: Driver memory = 5G
                          Executor memory = 15G
                          4 Executor cores

lines : RDD created by reading input file, 100 partitions, custom hash partitioning
<lines : (from-URL, to-URLs)>

ranks : RDD created by applying a mapValues transformation on links (preserves parent RDD partitioning)
<ranks : (from-URL, 1.0)>

for each iteration :
    contributions : RDD created by applying join and flatMap transformations on links and ranks
    <contributions : from-URL -> (to_URL, contribution)>

    ranks : new RDD containing updated ranks => sum of contributions from other URLs
    <ranks : (to-URL, updated-rank)>

output : apply collect() action on ranks

-----------------------------------------------------------------------------------------------------------------------------------------------------

Question 3:
Configuration parameters: Driver memory = 5G
                          Executor memory = 15G
                          4 Executor cores

lines : RDD created by reading input file, 100 partitions, custom hash partitioning, cache in memory as RDD is not updated
<lines : (from-URL, to-URLs)>

ranks : RDD created by applying a mapValues transformation on links (preserves parent RDD partitioning)
<ranks : (from-URL, 1.0)>

for each iteration :
    contributions : RDD created by applying join and flatMap transformations on links and ranks
    <contributions : from-URL -> (to_URL, contribution)>

    ranks : new RDD containing updated ranks => sum of contributions from other URLs
    <ranks : (to-URL, updated-rank)>

output : apply collect() action on ranks

-----------------------------------------------------------------------------------------------------------------------------------------------------
