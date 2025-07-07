import React from 'react';
import { generateExplanationSteps } from './utils';

const Explanation = ({ generatedJson }) => {
  // Não renderiza nada se o JSON estiver vazio, for nulo, ou contiver um erro
  if (!generatedJson || generatedJson.error || Object.keys(generatedJson).length === 0) {
    return null; 
  }
  
  const steps = generateExplanationSteps(generatedJson);

  if (steps.length === 0) {
      return null;
  }

  return (
    <div className="explanation-card">
      <h3>Sequência Lógica da Regra</h3>
      <ol>
        {steps.map((step, index) => (
          // Usamos um truque para renderizar o negrito (<strong>) do nosso texto
          <li key={index} style={{ paddingLeft: `${step.level * 20}px` }}>
            <span dangerouslySetInnerHTML={{ __html: step.text }} />
          </li>
        ))}
      </ol>
    </div>
  );
};

export default Explanation;