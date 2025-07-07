import React from 'react';

const JsonOutput = ({ generatedJson }) => {
  // Simplificado para mostrar apenas a regra de processamento principal
  return (
    <div className="json-output-card">
      <h3>JSON Final Gerado</h3>
      <pre><code>{JSON.stringify(generatedJson, null, 2)}</code></pre>
    </div>
  );
};

export default JsonOutput;