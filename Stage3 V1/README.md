# Stage 3: Entity Matching with Magellan
We performed entity match on Songs and Tracks.

## Tables
### Source Data
We used the Songs and Tracks datasets provided, but downsampled them into sampleA (17731 tuples) and sampleB (10,0000 tuples) respectively. The attributes were left unchanged.

The overlap blocker was removing the '+' character in artists attribute of sampleB without replacing it with a whitespace, which meant 1-word overlap blocking removed good candidate tuples. We modified sampleB so that '+' would be replaced by a single whitespace and this table is saved as sampleB1.

### Candidate Tuple Pairs
C5 contains the final candidate tuple pairs (2742). C, C1a, and C2 had too many candidates and the files were too large to share on GitHub.

### Golden Data
400 tuples were sampled from C5 and the final golden dataset, G, has 390 labelled tuple pairs (184 positive, 206 negative). The 10 tuples that were discarded due to ambiguity are stored in 'Removed from G.csv'.



