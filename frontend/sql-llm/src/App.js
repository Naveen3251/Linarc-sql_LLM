import React, { useState } from 'react';
import axios from 'axios';

import './App.css'; // Import your CSS file

function App() {
    const [question, setQuestion] = useState('');
    const [sqlQuery, setSqlQuery] = useState('');
    const [results, setResults] = useState([]);
    const [columns, setColumns] = useState([]);

    const handleQuestionSubmit = async () => {
        try {
            const response = await axios.post('http://localhost:5000/generate-query', {
                question: question
            });
            
            console.log("API Response:", response.data);
            
            setSqlQuery(response.data.sql_query);
            
            
            if (response.data.results.error) {
                setResults([response.data.results.error]);
                setColumns([]);
            } else {
                setResults(response.data.results.rows);
                setColumns(response.data.results.columns);
                //console.log("Results:", response.data.results.rows);  // Log the results
            }
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };
    

    return (
        <div className="app-container">
            <h1 className="app-title">SQL Query Generator for E-commerce Dataset</h1>
            <div className="input-group">
                <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask your question"
                    className="question-input"
                />
                <button onClick={handleQuestionSubmit} className="submit-button">Run Query</button>
            </div>
            
            <h2 className="sql-title">Generated SQL Query:</h2>
            <div className='code-container'>
                <pre className="sql-query">
                    <code>
                        {sqlQuery}
                    </code>
                </pre>
            </div>
            <h2 className="results-title">Results:</h2>
            {columns.length > 0 && (
                <div className='table-container'>
                <table>
                    <thead>
                        <tr>
                            {columns.map((col, index) => <th key={index}>{col}</th>)}
                        </tr>
                    </thead>
                    <tbody>
                        {results.map((row, index) => (
                            <tr key={index}>
                                {row.map((cell, idx) => <td key={idx}>{cell}</td>)}
                            </tr>
                        ))}
                    </tbody>
                </table>
                </div>
            )}
            {results.length === 0 && <p className="no-results">No results found.</p>}
        </div>
    );
}

export default App;
