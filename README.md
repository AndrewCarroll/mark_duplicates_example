# Example of MarkDuplicates Undesired Behavior

This repository provides data and examples required to reproduce what may 
demonstrate undesired behavior of the MarkDuplicates algorithm.

MarkDuplicates is designed to identify multiple read pairs in which the read and mate
or two or more pairs map to the same positions and to mark the lower quality reads as
duplicates. In theory, the better read pair should be the one not marked.

The logic to assess this is the base qualities of the read. Base qualities are phred-encoded,
meaning small changes at the low range correspond to large differences in error probability.

MarkDuplicates behavior does not guarantee that the read pair with the lower number of errors
is the read that is retained. Instead, the sum of linear qualities is use, which can often
result in the worse quality read paire being maintained.

This example is for reads which have the same length, which is likely the most common case. 
In reads where one pair is longer, this will tend to favor the longer reads even if they have more errors,
which might be desirable

Presented is an example with the data and commands to replicate.

## Demonstration of effect

Two read pairs with identical forward and reverse sequence are presented in *mark_duplicate_test.1.fastq*
and *mark_duplicate_test.2.fastq*. The first of these read pairs has all quality values 37 (F), but 5 bases
in each read of 2 (#). The second pair has all quality values 32 (A).

The expected number of errors in the first pair is: **6.3678**


The expected number of errors in the second pair is **0.1905**

The error calculation is performed in the script get_errors.py (e.g. ```python get_errors.py FF#AA```)

After the following operations, the second read pair is marked as a duplicate and the first of higher quality:

```
bwa mem references/GRCh38/GRCh38.no_alt_analysis_set.fa mark_duplicate_test.1.fastq mark_duplicate_test.2.fastq -R '@RG\tID:test_duplicates\tLB:1\tPL:ILLUMINA\tPU:NONE\tSM:TEST'| samtools sort -O SAM -o test_duplicates.sam
java -jar gatk/gatk-package-4.0.10.0-local.jar MarkDuplicates -I test_duplicates.sam -O test_duplicates.mark.sam -M metrics
```

The resulting SAM files from BWA and from MarkDuplicates are provided in this repo
