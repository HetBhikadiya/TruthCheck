import { Link } from 'react-router-dom'

function Navbar() {
  return (
    <nav style={{
      background: '#1e293b',
      padding: '1rem 2rem',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      borderBottom: '1px solid #334155'
    }}>
      <Link to="/" style={{ textDecoration: 'none' }}>
        <h1 style={{ color: '#38bdf8', margin: 0, fontSize: '1.5rem' }}>
          🔍 TruthCheck
        </h1>
      </Link>
      <div style={{ display: 'flex', gap: '2rem' }}>
        <Link to="/" style={{ color: '#94a3b8', textDecoration: 'none' }}>Home</Link>
              <Link to="/dashboard" style={{ color: '#94a3b8', textDecoration: 'none' }}>Dashboard</Link>
              <Link to="/analytics" style={{ color: '#94a3b8', textDecoration: 'none' }}>Analytics</Link>
      </div>
    </nav>
  )
}

export default Navbar