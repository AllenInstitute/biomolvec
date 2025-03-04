
### Genome-wide nucleotide and amino acid sequences.

#### 1. Download fasta files for cdna sequences:

 - `Mus_musculus.GRCm39.cdna.all.fa.gz` was downloaded from [Ensemble](https://useast.ensembl.org/Mus_musculus/Info/Index)
 - `Homo_sapiens.GRCh38.cdna.all.fa.gz` was downloaded from [Ensemble](https://useast.ensembl.org/Homo_sapiens/Info/Index)

#### 2. Extract nucleitide sequences from `.fa` files into dataframes (and saved as `.csv` files)

 - `00_get_seqs_mouse.ipynb`
 - `00_get_seqs_human.ipynb`

####  3. Use lookups with `gget` to get amino acid sequences using ensembl_ids

 - `get_aa_seq_mouse.py`
 - `get_aa_seq_human.py`

#### 4. Merge and clean up the dataframes

 - `03_inspect_aa_seq_human.ipynb`
 - `04_inspect_aa_seq.ipynb`

#### The final dataframes are saved as 

 - `prot_nuc_seqs_mouse.csv` 
 - `prot_nuc_seqs_human.csv`

#### Example row: 

|gene_symbol|ensg_id|enst_id|nuc_seq_length|aa_seq_length|nuc_aa_seq_ratio|chromosome|start|end|strand|nuc_seq|aa_seq|
|---|---|---|---|---|---|---|---|---|---|---|---|
|Gm20730|ENSMUSG00.. |ENSMUST00 |359|119.0|3.01|GRCm39:6|430 |4305 |-1.0|ATGAGGTGC |MRCLAEFLR.

### Embedding nucleotide sequences with Nucleotide Transformer

We used [Nucleotide Transformer](https://github.com/instadeepai/nucleotide-transformer) models to embed sequences with a maximum length of 5952 nucleotides. Sequences longer than 5952 nucleotides were truncated. Specifically, we used the `500M_human_ref` and `500M_multi_species_v2` models for human and mouse respectively.

 - `04_nuc_nt_emb_mouse.ipynb`
 - `05_nuc_nt_emb_human.ipynb`

### Embedding amino-acid sequences with ESM3 and MMIDAS joint clustering

 - See the [nautilex-esm repository](https://github.com/alleninstitute/nautilex-esm/)

### Combining results for analysis and visualization

We performed Leiden clustering for `nt-emb` and `esm3-emb`, along with 2d umap projections. Results are merged with those from MMIDAS joint clustering for further visualization. 

 - `06_make_df.ipynb`
 - `07_static_plots.ipynb`
 - `08_dynamic_plots.ipynb`
 - `09_enrichr_vignettes.ipynb`

### Contact:

 - Rohan Gala
 - Yeganeh Marghi