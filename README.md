# COL764-Vector-Space-Reterival-
An efficient and effective end-to-end Vector-space retrieval model and retrieval system for English
# How to Run?
# Build Dictionary:
$ python3 invidx cons.py assignment1 data/TaggedTrainingAP/ index-file

# Print Dictionary :
$ python3 printdict.py indexfile.dict n
last parameter (n) is optional

# Process Queries:
$ python3 vecsearch.py assignment1 data/topics.51-100 10 output2 in-dexfile.dict indexfile.idx

# Caclulate nDCG score:
$ ./trec eval-9.0.7/trec eval -mndcg cut.10 -M100 qrels.51-100 output

# Calculate F1 score:
$ ./trec eval-9.0.7/trec eval -m set F -M100 qrels.51-100 output
