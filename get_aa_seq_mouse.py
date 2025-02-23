from multiprocessing import Pool
import pandas as pd
import gget
from tqdm import tqdm


import re

def parse_seq_header(header):
    # Extract key information using regex
    ensemble_pattern = r'ensembl_id:\s*(ENSMUS[T|G]\d+)'
    gene_pattern = r'gene_name:\s*([^\s]+)'  # Changed: capture everything until a space
    length_pattern = r'sequence_length:\s*(\d+)'
    
    ensemble_id = re.search(ensemble_pattern, header).group(1)
    gene_name = re.search(gene_pattern, header).group(1)
    sequence_length = int(re.search(length_pattern, header).group(1))
    
    return {
        'ensemble_id': ensemble_id,
        'gene_name': gene_name,
        'sequence_length': sequence_length
    }


def process_single_gene(gene_id):
    try:
        out = gget.seq(gene_id, translate=True, isoforms=False, verbose=False)
        if len(out) == 2:
            df_single = pd.DataFrame([parse_seq_header(out[0])])
            df_single["aa_seq"] = out[1]
            return df_single
    except Exception as e:
        print(f"Error processing gene {gene_id}: {str(e)}")
        return None

def get_aa_seq(lookup_ids):
    # Number of processes - adjust based on your system
    n_processes = 16
    
    # Create a process pool and map the function over all gene IDs
    with Pool(n_processes) as pool:
        results = list(tqdm(
            pool.imap(process_single_gene, lookup_ids),
            total=len(lookup_ids)
        ))

    # Combine all successful results

    # if all results are None, return None
    if all(r is None for r in results):
        # all results are None
        df_prot = pd.DataFrame(columns=["ensemble_id", "gene_name", "sequence_length", "aa_seq"])
    else:
        df_prot = pd.concat([r for r in results if r is not None], ignore_index=True)
    return df_prot


if __name__ == "__main__":
    import time
    df = pd.read_csv("./data/nuc_seqs_mouse.csv")
    all_lookup_ids = df["ens_gene_id"].unique()
    
    batch_size = 1000

    for i in range(23000, len(all_lookup_ids), batch_size):
        batch_ids = all_lookup_ids[i:i+batch_size]
        start_idx = i
        end_idx = min(i + batch_size, len(all_lookup_ids))
        
        print(f"Processing batch {start_idx:05d}-{end_idx:05d}")
        
        start_time = time.time()
        df_prot = get_aa_seq(batch_ids)
        end_time = time.time()
        
        output_file = f"./data/aa_seqs_mouse_{start_idx:05d}-{end_idx:05d}.csv"
        df_prot.to_csv(output_file, index=False)
        print(f"Batch completed in {end_time - start_time:.2f} seconds")
        print(f"Saved to {output_file}")