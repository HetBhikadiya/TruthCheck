import { useLocation, useNavigate } from 'react-router-dom'
import VerdictCard from '../components/VerdictCard'

function Result() {
  const location = useLocation()
  const navigate = useNavigate()
  const result = location.state?.result

  if (!result) {
    navigate('/')
    return null
  }

  return (
    <div style={{ maxWidth: '800px', margin: '3rem auto', padding: '0 2rem' }}>
      <button
        onClick={() => navigate('/')}
        style={{
          background: '#1e293b',
          color: '#94a3b8',
          border: 'none',
          padding: '0.5rem 1rem',
          borderRadius: '8px',
          cursor: 'pointer',
          marginBottom: '2rem'
        }}
      >
        ← Analyze Another
      </button>

      <h2 style={{ color: '#f1f5f9', marginBottom: '1.5rem' }}>
        Analysis Result
      </h2>

      <VerdictCard result={result} />

      <div style={{
        background: '#1e293b',
        borderRadius: '12px',
        padding: '1rem',
        marginTop: '1rem'
      }}>
        <h4 style={{ color: '#38bdf8', margin: '0 0 0.5rem' }}>📝 Analyzed Content</h4>
        <p style={{ color: '#94a3b8', margin: 0, wordBreak: 'break-all' }}>
          {result.content}
        </p>
      </div>
    </div>
  )
}

export default Result