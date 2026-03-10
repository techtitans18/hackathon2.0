export default function RecordTable({ records, onDownload, onDownloadSummary }) {
  if (!records || records.length === 0) {
    return <p>No records available</p>;
  }

  return (
    <table className="records-table">
      <thead>
        <tr>
          <th>Type</th>
          <th>Description</th>
          <th>Date</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {records.map((record, idx) => (
          <tr key={idx}>
            <td>{record.record_type}</td>
            <td>{record.description}</td>
            <td>{new Date(record.timestamp).toLocaleDateString()}</td>
            <td>
              {record.download_url && (
                <button
                  className="btn-small"
                  onClick={() => onDownload(record.file_reference)}
                >
                  Download File
                </button>
              )}
              {record.summary_download_url && (
                <button
                  className="btn-small"
                  onClick={() => onDownloadSummary(record.summary_file_reference)}
                  style={{ marginLeft: '0.5rem' }}
                >
                  View Summary
                </button>
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
