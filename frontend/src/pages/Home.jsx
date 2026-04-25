import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { analyzeContent } from '../utils/api'

function Home() {
  const [inputType, setInputType] = useState('text')
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleAnalyze = async () => {
    if (!content.trim()) {
      setError('Please enter some content to analyze!')
      return
    }
    setLoading(true)
    setError('')
    try {
      const data = await analyzeContent(inputType, content)
      navigate('/result', { state: { result: data.result } })
    } catch (err) {
      setError('Something went wrong. Make sure the backend is running!')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: '800px', margin: '4rem auto', padding: '0 2rem' }}>
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <h2 style={{ fontSize: '2.5rem', color: '#f1f5f9', marginBottom: '1rem' }}>
          Detect Fake News Instantly
        </h2>
        <p style={{ color: '#94a3b8', fontSize: '1.1rem' }}>
          Paste a news article, URL, or WhatsApp forward to verify it
        </p>
      </div>

      {/* Input Type Selector */}
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1.5rem' }}>
        {['text', 'url'].map(type => (
          <button
            key={type}
            onClick={() => setInputType(type)}
            style={{
              padding: '0.5rem 1.5rem',
              borderRadius: '8px',
              border: 'none',
              cursor: 'pointer',
              background: inputType === type ? '#38bdf8' : '#1e293b',
              color: inputType === type ? '#0f172a' : '#94a3b8',
              fontWeight: 'bold',
              textTransform: 'uppercase'
            }}
          >
            {type}
          </button>
        ))}
      </div>

      {/* Input Box */}
      <textarea
        value={content}
        onChange={e => setContent(e.target.value)}
        placeholder={
          inputType === 'url'
            ? 'Paste a news URL here...'
            : 'Paste news text or WhatsApp forward here...'
        }
        style={{
          width: '100%',
          height: '200px',
          background: '#1e293b',
          border: '1px solid #334155',
          borderRadius: '12px',
          padding: '1rem',
          color: '#f1f5f9',
          fontSize: '1rem',
          resize: 'vertical',
          boxSizing: 'border-box'
        }}
      />

      {error && (
        <p style={{ color: '#f87171', marginTop: '0.5rem' }}>{error}</p>
      )}

      {/* Analyze Button */}
      <button
        onClick={handleAnalyze}
        disabled={loading}
        style={{
          width: '100%',
          padding: '1rem',
          marginTop: '1rem',
          background: loading ? '#334155' : '#38bdf8',
          color: '#0f172a',
          border: 'none',
          borderRadius: '12px',
          fontSize: '1.1rem',
          fontWeight: 'bold',
          cursor: loading ? 'not-allowed' : 'pointer'
        }}
      >
        {loading ? 'Analyzing...' : '🔍 Analyze Now'}
      </button>
    </div>
  )
}

export default Home