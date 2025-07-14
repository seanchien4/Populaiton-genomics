#!/bin/bash
# cleaning seq names
# if thre are more than two lanes for an sample, merge them
# result names should be name.R1.fastq.gz


# Make an output directory to store renamed/combined files
mkdir -p renamed_fastqs

# Loop through all fastq.gz files
for file in *.fastq.gz; do
    # Get sample name by removing everything after first underscore
    sample=$(echo "$file" | cut -d'_' -f1)
    
    # Group by sample and read direction (R1 or R2)
    if [[ "$file" == *_R1* ]]; then
        echo "$file" >> "${sample}_R1_list.txt"
    elif [[ "$file" == *_R2* ]]; then
        echo "$file" >> "${sample}_R2_list.txt"
    fi
done

# Process each sample
for r1list in *_R1_list.txt; do
    sample=${r1list%_R1_list.txt}
    r2list="${sample}_R2_list.txt"
    
    # Combine R1 reads
    cat $(cat "$r1list") > "renamed_fastqs/${sample}.R1.fastq.gz"
    
    # Combine R2 reads (if exist)
    if [[ -f "$r2list" ]]; then
        cat $(cat "$r2list") > "renamed_fastqs/${sample}.R2.fastq.gz"
    else
        echo "Warning: R2 missing for $sample"
    fi
    
    # Cleanup temp list files
    rm "$r1list" "$r2list" 2>/dev/null
done
