import React, { useState } from 'react';
import './App.css';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [result, setResult] = useState(null);

  // Function to handle API calls
  const handleSearch = async (type) => {
    const endpoint =
      type === 'crawler'
        ? `http://127.0.0.1:5001/business/crawl?business-name=${encodeURIComponent(searchQuery)}`
        : `http://127.0.0.1:5001/business/db-lookup?business-name=${encodeURIComponent(searchQuery)}`;

    try {
      const response = await fetch(endpoint);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Error response:', response.status, response.statusText, errorText);
        setResult({ error: `Error: ${response.status} ${response.statusText}`, details: errorText });
        return;
      }

      const data = await response.json();
      console.log("RESPONSE",data)
      setResult(data); // Await ensures we don't proceed until the response resolves
    } catch (error) {
      console.error('Fetch error:', error);
      setResult({ error: 'An error occurred while fetching data.', details: error.message });
    }
  };

  // Function to render a table for the result data
  const renderTable = () => {
    if (!result) return null;

    return (
      <div style={{ marginTop: '20px', textAlign: 'left' }}>
        <h3>Corporation Details:</h3>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th style={styles.th}>Field</th>
              <th style={styles.th}>Value</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style={styles.td}>Corporation Type</td>
              <td style={styles.td}>{result.corporation_type || ''}</td>
            </tr>
            <tr>
              <td style={styles.td}>Entity Name</td>
              <td style={styles.td}>{result.entity_name || ''}</td>
            </tr>
            <tr>
              <td style={styles.td}>Mailing Address</td>
              <td style={styles.td}>{result.mailing_address || ''}</td>
            </tr>
            <tr>
              <td style={styles.td}>Principal Address</td>
              <td style={styles.td}>{result.principal_address || ''}</td>
            </tr>
            <tr>
              <td style={styles.td}>Registered Agent</td>
              <td style={styles.td}>
                {(result.registered_agent && result.registered_agent.name) || ''}
                <br />
                {(result.registered_agent && result.registered_agent.address) || ''}
              </td>
            </tr>
          </tbody>
        </table>

        <h3>Filing Information:</h3>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th style={styles.th}>Field</th>
              <th style={styles.th}>Value</th>
            </tr>
          </thead>
          <tbody>
            {result.filing_information
              ? Object.entries(result.filing_information).map(([key, value]) => (
                  <tr key={key}>
                    <td style={styles.td}>{key || ''}</td>
                    <td style={styles.td}>{value || ''}</td>
                  </tr>
                ))
              : null}
          </tbody>
        </table>

        <h3>Officers and Directors:</h3>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th style={styles.th}>Title</th>
              <th style={styles.th}>Name</th>
              <th style={styles.th}>Address</th>
            </tr>
          </thead>
          <tbody>
            {result.officers_directors
              ? result.officers_directors.map((officer, index) => (
                  <tr key={index}>
                    <td style={styles.td}>{officer.title || ''}</td>
                    <td style={styles.td}>{officer.name || ''}</td>
                    <td style={styles.td}>{officer.address || ''}</td>
                  </tr>
                ))
              : null}
          </tbody>
        </table>
      </div>
    );
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Florida Business Lookup Crawler</h1>
        <div style={{ margin: '20px' }}>
          <input
            type="text"
            placeholder="Enter business name"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{
              padding: '10px',
              width: '300px',
              marginRight: '10px',
              borderRadius: '5px',
              border: '1px solid #ccc',
            }}
          />
          <div>
            <button
              onClick={() => handleSearch('crawler')}
              style={{
                padding: '10px 20px',
                margin: '10px',
                backgroundColor: '#007BFF',
                color: '#fff',
                border: 'none',
                borderRadius: '5px',
                cursor: 'pointer',
              }}
            >
              Crawler Search
            </button>
            <button
              onClick={() => handleSearch('db')}
              style={{
                padding: '10px 20px',
                margin: '10px',
                backgroundColor: '#28a745',
                color: '#fff',
                border: 'none',
                borderRadius: '5px',
                cursor: 'pointer',
              }}
            >
              DB Search
            </button>
          </div>
        </div>
        {result ? renderTable() : <p>No results yet. Perform a search to see results here.</p>}
      </header>
    </div>
  );
}

const styles = {
  th: {
    border: '1px solid #ddd',
    padding: '8px',
    textAlign: 'left',
    backgroundColor: '#f2f2f2',
  },
  td: {
    border: '1px solid #ddd',
    padding: '8px',
    textAlign: 'left',
  },
};

export default App;
