export default function EHealthCard({ card }) {
  if (!card) {
    return <div>No e-health card data available</div>;
  }

  return (
    <div className="e-health-card">
      <div className="card-front">
        <div className="card-header">
          <h3>E-Health Card</h3>
        </div>

        <div className="card-body">
          {card.photo_url && (
            <div className="card-photo">
              <img src={card.photo_url} alt="Profile" />
            </div>
          )}

          <div className="card-info">
            <div className="info-item">
              <label>Health ID</label>
              <p>{card.health_id}</p>
            </div>

            <div className="info-item">
              <label>Name</label>
              <p>{card.name}</p>
            </div>

            <div className="info-item">
              <label>Blood Group</label>
              <p>{card.blood_group}</p>
            </div>

            <div className="info-item">
              <label>Phone</label>
              <p>{card.phone}</p>
            </div>
          </div>
        </div>

        <div className="card-footer">
          <p>Emergency Contact: Call Your Hospital</p>
        </div>
      </div>
    </div>
  );
}
