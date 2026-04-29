import { PieChart, Pie, Cell, Legend, Tooltip } from 'recharts'

function FakeRealChart({ data }) {
  const COLORS = ['#ef4444', '#22c55e', '#f59e0b']

  return (
    <div style={{
      background: '#1e293b',
      borderRadius: '16px',
      padding: '1.5rem',
      marginBottom: '1.5rem'
    }}>
      <h3 style={{ color: '#38bdf8', marginTop: 0 }}>📊 Fake vs Real Ratio</h3>
      <PieChart width={400} height={300}>
        <Pie
          data={data}
          cx={200}
          cy={150}
          outerRadius={100}
          dataKey="value"
          label={({ name, value }) => `${name}: ${value}`}
        >
          {data.map((entry, index) => (
            <Cell key={index} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </div>
  )
}

export default FakeRealChart