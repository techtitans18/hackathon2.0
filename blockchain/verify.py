"""Blockchain verification utilities."""
from blockchain.blockchain import healthcare_chain


def verify_blockchain_integrity() -> dict[str, bool | list[int]]:
    """
    Verify the integrity of the entire blockchain.
    
    Returns:
        dict with 'valid' (bool) and 'invalid_blocks' (list of indices)
    """
    chain = healthcare_chain.get_chain()
    invalid_blocks = []
    
    for i in range(1, len(chain)):
        current_block = chain[i]
        previous_block = chain[i - 1]
        
        # Verify previous hash link
        if current_block["previous_hash"] != previous_block["hash"]:
            invalid_blocks.append(i)
            continue
        
        # Verify current block hash
        block_copy = {k: v for k, v in current_block.items() if k != "hash"}
        computed_hash = healthcare_chain.generate_hash(block_copy)
        if computed_hash != current_block["hash"]:
            invalid_blocks.append(i)
    
    return {
        "valid": len(invalid_blocks) == 0,
        "invalid_blocks": invalid_blocks,
        "total_blocks": len(chain),
    }
