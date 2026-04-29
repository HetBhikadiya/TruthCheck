import FakeRealChart from '../components/FakeRealChart'
import TrendingNews from '../components/TrendingNews'

const fakeRealData = [
  { name: 'Fake', value: 42 },
  { name: 'Real', value: 35 },
  { name: 'Unverified', value: 23 },
]

const trendingTopics = [
  { topic: '🏥 Fake Medical Cures', count: 145 },
  { topic: '🏛️ Political Misinformation', count: 132 },
  { topic: '🌪️ Disaster Hoaxes', count: 89 },
  { topic: '💰 Financial Scams', count: 67 },
  { topic: '🦠 Health Myths', count: 54 },
]

function Analytics() {
  return (
    <div style={{ maxWidth: '900px', margin: '3rem auto', padding: '0 2rem' }}>
      <h2 style={{ color: '#f1f5f9', marginBottom: '2rem' }}>
        📊 Analytics Dashboard
      </h2>

      {/* Stats Row */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: '1rem',
        marginBottom: '2rem'
      }}>
        {[
          { label: 'Total Analyzed', value: '1,247', color: '#38bdf8' },
          { label: 'Fake Detected', value: '523', color: '#ef4444' },
          { label: 'Real Verified', value: '436', color: '#22c55e' },
        ].map((stat, i) => (
          <div key={i} style={{
            background: '#1e293b',
            borderRadius: '12px',
            padding: '1.5rem',
            textAlign: 'center'
          }}>
            <h3 style={{ color: stat.color, fontSize: '2rem', margin: 0 }}>
              {stat.value}
            </h3>
            <p style={{ color: '#94a3b8', margin: '0.5rem 0 0' }}>
              {stat.label}
            </p>
          </div>
        ))}
      </div>

      <FakeRealChart data={fakeRealData} />
      <TrendingNews items={trendingTopics} />
    </div>
  )
}

export default Analytics