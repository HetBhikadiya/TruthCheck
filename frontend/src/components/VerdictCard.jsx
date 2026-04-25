function VerdictCard({ result }) {
  const verdictColors = {
    '✅ LIKELY REAL': '#22c55e',
    '❌ LIKELY FAKE': '#ef4444',
    '⚠️ UNVERIFIED': '#f59e0b',
  }

  const color = verdictColors[result.final_verdict] || '#94a3b8'

  return (
    <div style={{
      background: '#1e293b',
      borderRadius: '16px',
      padding: '2rem',
      border: `2px solid ${color}`,
      marginBottom: '1.5rem'
    }}>
      {/* Main Verdict */}
      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '2.5rem', color, margin: 0 }}>
          {result.final_verdict}
        </h2>
        <p style={{ color: '#94a3b8', marginTop: '0.5rem' }}>
          Confidence: {result.final_score}%
        </p>

        {/* Confidence Bar */}
        <div style={{
          background: '#0f172a',
          borderRadius: '999px',
          height: '12px',
          marginTop: '1rem',
          overflow: 'hidden'
        }}>
          <div style={{
            width: `${result.final_score}%`,
            height: '100%',
            background: color,
            borderRadius: '999px',
            transition: 'width 1s ease'
          }} />
        </div>
      </div>

      {/* ML Result */}
      {result.ml_result && (
        <div style={{
          background: '#0f172a',
          borderRadius: '12px',
          padding: '1rem',
          marginBottom: '1rem'
        }}>
          <h4 style={{ color: '#38bdf8', margin: '0 0 0.5rem' }}>🤖 ML Analysis</h4>
          <p style={{ color: '#94a3b8', margin: '0.2rem 0' }}>
            Verdict: <span style={{ color: '#f1f5f9' }}>{result.ml_result.verdict}</span>
          </p>
          <p style={{ color: '#94a3b8', margin: '0.2rem 0' }}>
            Fake Probability: <span style={{ color: '#ef4444' }}>{result.ml_result.fake_probability}%</span>
          </p>
          <p style={{ color: '#94a3b8', margin: '0.2rem 0' }}>
            Real Probability: <span style={{ color: '#22c55e' }}>{result.ml_result.real_probability}%</span>
          </p>
        </div>
      )}

      {/* URL Result */}
      {result.url_result && (
        <div style={{
          background: '#0f172a',
          borderRadius: '12px',
          padding: '1rem',
          marginBottom: '1rem'
        }}>
          <h4 style={{ color: '#38bdf8', margin: '0 0 0.5rem' }}>🔗 URL Analysis</h4>
          <p style={{ color: '#94a3b8', margin: '0.2rem 0' }}>
            Domain: <span style={{ color: '#f1f5f9' }}>{result.url_result.domain}</span>
          </p>
          <p style={{ color: '#94a3b8', margin: '0.2rem 0' }}>
            SSL: <span style={{ color: result.url_result.ssl ? '#22c55e' : '#ef4444' }}>
              {result.url_result.ssl ? '✅ Secure' : '❌ Not Secure'}
            </span>
          </p>
          <p style={{ color: '#94a3b8', margin: '0.2rem 0' }}>
            Trust Status: <span style={{ color: '#f1f5f9' }}>{result.url_result.trust_status}</span>
          </p>
          <p style={{ color: '#94a3b8', margin: '0.2rem 0' }}>
            Trust Score: <span style={{ color }}>{result.url_result.trust_score}/100</span>
          </p>
        </div>
      )}
    </div>
  )
}

export default VerdictCard