function TrendingNews({ items }) {
  return (
    <div style={{
      background: '#1e293b',
      borderRadius: '16px',
      padding: '1.5rem',
      marginBottom: '1.5rem'
    }}>
      <h3 style={{ color: '#38bdf8', marginTop: 0 }}>🔥 Trending Fake News Topics</h3>
      {items.map((item, index) => (
        <div key={index} style={{
          background: '#0f172a',
          borderRadius: '8px',
          padding: '0.75rem 1rem',
          marginBottom: '0.75rem',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <span style={{ color: '#f1f5f9' }}>{item.topic}</span>
          <span style={{
            background: '#ef4444',
            color: 'white',
            padding: '0.2rem 0.6rem',
            borderRadius: '999px',
            fontSize: '0.8rem'
          }}>
            {item.count} reports
          </span>
        </div>
      ))}
    </div>
  )
}

export default TrendingNews