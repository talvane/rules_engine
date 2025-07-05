import React from 'react';

const JsonOutput = ({ validationRules, processingRule }) => {
  return (
    <div className="output-card">
      <h2>JSON Gerado</h2>
      <p>Copie e cole este código no seu arquivo <strong>regras.py</strong>.</p>
      
      <div className="json-section">
        <h3>REGRAS_VALIDACAO</h3>
        <pre><code>
          {JSON.stringify(validationRules, null, 2)}
        </code></pre>
      </div>

      <div className="json-section">
        <h3>REGRA_PROCESSAMENTO</h3>
        <pre><code>
          {JSON.stringify(processingRule, null, 2)}
        </code></pre>
      </div>
    </div>
  );
};

export default JsonOutput;