export default function BlockchainViewer({ blockchain }) {
  if (!blockchain || !blockchain.chain) {
    return <div>No blockchain data available</div>;
  }

  const integrity = blockchain.integrity || {};

  return (
    <div className="blockchain-viewer">
      <h3>Blockchain Ledger</h3>
      <div className="blockchain-info">
        <p><strong>Total Blocks:</strong> {blockchain.length || blockchain.chain?.length}</p>
        {integrity.valid !== undefined && (
          <p>
            <strong>Integrity Status:</strong>{' '}
            <span className={integrity.valid ? 'status-valid' : 'status-invalid'}>
              {integrity.valid ? '✓ Valid' : '✗ Tampered'}
            </span>
          </p>
        )}
      </div>

      <div className="blockchain-chain">
        {blockchain.chain?.map((block, idx) => (
          <div key={idx} className="blockchain-block">
            <div className="block-header">
              <span className="block-index">Block #{block.index}</span>
              <span className="block-type">{block.RecordType}</span>
            </div>

            <div className="block-content">
              <p><strong>Health ID:</strong> {block.HealthID}</p>
              <p><strong>Hospital ID:</strong> {block.HospitalID}</p>
              <p><strong>Record Hash:</strong> <code>{block.RecordHash?.substring(0, 16)}...</code></p>
              <p><strong>Timestamp:</strong> {new Date(block.timestamp).toLocaleString()}</p>
              <p><strong>Block Hash:</strong> <code>{block.hash?.substring(0, 16)}...</code></p>
              <p><strong>Previous Hash:</strong> <code>{block.previous_hash?.substring(0, 16)}...</code></p>
            </div>

            {idx < blockchain.chain?.length - 1 && <div className="block-connector">↓</div>}
          </div>
        ))}
      </div>
    </div>
  );
}
