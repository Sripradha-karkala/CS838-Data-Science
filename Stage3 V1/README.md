# Stage 3: Entity Matching with Magellan
We performed entity match on Songs and Tracks.

## Code: Jupyter Notebook
Our process is documented in CS838+Stage+3+V1.ipynb.

## DATA: Tables
### Source Data
We used the Songs and Tracks datasets provided, but downsampled them into sampleA (17731 tuples) and sampleB (10,0000 tuples) respectively. The attributes were left unchanged.

The overlap blocker was removing the '+' character in artists attribute of sampleB without replacing it with a whitespace, which meant 1-word overlap blocking removed good candidate tuples. We modified sampleB so that '+' would be replaced by a single whitespace and this table is saved as sampleB1.

### Candidate Tuple Pairs
C5 contains the final candidate tuple pairs (2742). Our previous blocking attempts (C, C1a, and C2) had too many candidates and the files were too large to share on GitHub.

### Golden Data
400 tuples were sampled from C5 and the final golden dataset, G, has 390 labelled tuple pairs (184 positive, 206 negative). The 10 tuples that were discarded due to ambiguity are stored in 'Removed from G.csv'.

### Train and Test Data
I has 273 labelled tuple pairs for training and J has 117 for testing.

### Other Tables
C4, D, E, and E1 represent other blocking attempts and S, S1, S2, and S3 are samples from some of these earlier blocking attempts. dbg to dbg5 also document our blocking process. dbg6 are sample tuples from our final blocker (C5).

