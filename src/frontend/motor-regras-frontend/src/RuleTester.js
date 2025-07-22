import React, { useState } from 'react';
import './RuleTester.css';

const RuleTester = ({ generatedJson, availableFields }) => {
  const [inputData, setInputData] = useState('{}');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [useBackend, setUseBackend] = useState(false);
  const [backendStatus, setBackendStatus] = useState('unknown'); // 'unknown', 'online', 'offline'

  // Implementação básica do JSON Logic em JavaScript
  const jsonLogic = (rule, data) => {
    if (!rule || typeof rule !== 'object') {
      return rule;
    }

    const operations = {
      '==': (a, b) => a === b,
      '!=': (a, b) => a !== b,
      '>': (a, b) => a > b,
      '>=': (a, b) => a >= b,
      '<': (a, b) => a < b,
      '<=': (a, b) => a <= b,
      '!': (a) => !a,
      'and': (...args) => args.every(Boolean),
      'or': (...args) => args.some(Boolean),
      '+': (...args) => args.reduce((sum, val) => sum + val, 0),
      '-': (a, b) => b !== undefined ? a - b : -a,
      '*': (...args) => args.reduce((product, val) => product * val, 1),
      '/': (a, b) => a / b,
      '%': (a, b) => a % b,
      'var': (path, defaultValue) => {
        if (!path) return data;
        const keys = path.split('.');
        let current = data;
        for (const key of keys) {
          if (current === null || current === undefined) return defaultValue;
          current = current[key];
        }
        return current !== undefined ? current : defaultValue;
      },
      'if': (condition, thenValue, elseValue) => condition ? thenValue : elseValue,
      '?:': (condition, thenValue, elseValue) => condition ? thenValue : elseValue,
      'in': (item, array) => {
        if (Array.isArray(array)) return array.includes(item);
        if (typeof array === 'string') return array.includes(item);
        return false;
      },
      'cat': (...args) => args.join('')
    };

    const operator = Object.keys(rule)[0];
    const values = rule[operator];

    if (!(operator in operations)) {
      throw new Error(`Operação não suportada: ${operator}`);
    }

    let processedValues;
    if (Array.isArray(values)) {
      processedValues = values.map(val => jsonLogic(val, data));
    } else {
      processedValues = [jsonLogic(values, data)];
    }

    return operations[operator](...processedValues);
  };

  // Verifica se o backend está online
  const checkBackendStatus = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/health');
      if (response.ok) {
        setBackendStatus('online');
        return true;
      } else {
        setBackendStatus('offline');
        return false;
      }
    } catch (error) {
      setBackendStatus('offline');
      return false;
    }
  };

  // Processa a regra usando o backend Python
  const processRuleWithBackend = async (rule, data) => {
    try {
      const response = await fetch('http://localhost:5000/api/process-rule', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rule, data })
      });

      if (!response.ok) {
        throw new Error(`Erro do servidor: ${response.status}`);
      }

      const result = await response.json();
      if (result.success) {
        return result.result;
      } else {
        throw new Error(result.error || 'Erro desconhecido do servidor');
      }
    } catch (error) {
      throw new Error(`Erro ao comunicar com o backend: ${error.message}`);
    }
  };

  const handleTestRule = async () => {
    if (!generatedJson) {
      setError('Nenhuma regra foi gerada. Primeiro construa uma regra no FlowBuilder.');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const parsedData = JSON.parse(inputData);
      
      let ruleResult;
      if (useBackend) {
        // Primeiro verifica se o backend está online
        const isBackendOnline = await checkBackendStatus();
        if (!isBackendOnline) {
          throw new Error('Backend não está disponível. Verifique se o servidor Python está rodando em http://localhost:5000');
        }
        
        ruleResult = await processRuleWithBackend(generatedJson, parsedData);
      } else {
        ruleResult = jsonLogic(generatedJson, parsedData);
      }
      
      setResult(ruleResult);
    } catch (err) {
      setError(`Erro ao processar: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  // Verifica o status do backend quando o componente monta
  React.useEffect(() => {
    checkBackendStatus();
  }, []);

  const generateSampleData = () => {
    console.log('=== GENERATE SAMPLE DATA DEBUG ===');
    console.log('availableFields:', availableFields);
    console.log('availableFields type:', typeof availableFields);
    console.log('availableFields isArray:', Array.isArray(availableFields));
    
    // Primeiro, usa os campos padrão do contexto se não há campos customizados
    const defaultFields = [
      { value: 'pontuacao_credito', label: 'Pontuação Crédito' },
      { value: 'renda_mensal', label: 'Renda Mensal' },
      { value: 'possui_divida_ativa', label: 'Possui Dívida Ativa' },
      { value: 'idade', label: 'Idade' },
      { value: 'valor_solicitado', label: 'Valor Solicitado' }
    ];

    const fieldsToUse = (availableFields && availableFields.length > 0) ? availableFields : defaultFields;
    console.log('fieldsToUse:', fieldsToUse);
    
    const sampleData = {};
    fieldsToUse.forEach((field, index) => {
      const fieldName = field.value || field.name || field.label;
      console.log(`Field ${index}: ${fieldName} (from:`, field, ')');
      
      if (!fieldName || fieldName === 'undefined') {
        console.log(`Skipping invalid field: ${fieldName}`);
        return;
      }

      // Infere o tipo baseado no nome do campo
      if (fieldName.includes('pontuacao') || fieldName.includes('renda') || 
          fieldName.includes('valor') || fieldName.includes('idade') || fieldName.includes('Idade') ||
          fieldName.includes('score') || fieldName.includes('Score') || fieldName.includes('numero')) {
        sampleData[fieldName] = Math.floor(Math.random() * 1000) + 100;
      } else if (fieldName.includes('possui') || fieldName.includes('ativo') || 
                 fieldName.includes('divida') || fieldName.includes('aprovado') ||
                 fieldName.includes('boolean')) {
        sampleData[fieldName] = Math.random() > 0.5;
      } else {
        sampleData[fieldName] = `exemplo_${fieldName}`;
      }
    });

    console.log('Final sampleData:', sampleData);
    console.log('=== END DEBUG ===');
    
    setInputData(JSON.stringify(sampleData, null, 2));
  };

  return (
    <div className="rule-tester">
      <h3>Testar Regra</h3>
      
      {/* <div className="processing-options">
        <h4>Opções de Processamento:</h4>
        <div className="radio-group">
          <label className="radio-option">
            <input
              type="radio"
              name="processing"
              checked={!useBackend}
              onChange={() => setUseBackend(false)}
            />
            <span>Frontend (JavaScript)</span>
          </label>
          <label className="radio-option">
            <input
              type="radio"
              name="processing"
              checked={useBackend}
              onChange={() => setUseBackend(true)}
            />
            <span>
              Backend (Python)
              <span className={`status-indicator ${backendStatus}`}>
                {backendStatus === 'online' ? '🟢' : 
                 backendStatus === 'offline' ? '🔴' : '🟡'}
              </span>
            </span>
          </label>
        </div>
        
        {backendStatus === 'offline' && useBackend && (
          <div className="backend-info">
            <p>⚠️ Backend não está disponível. Para usar o processamento Python:</p>
            <ol>
              <li>Instale as dependências: <code>poetry install</code></li>
              <li>Execute o servidor: <code>python src/api_server.py</code></li>
            </ol>
          </div>
        )}
      </div> */}
      
      <div className="input-section">
        <div className="input-header">
          <label htmlFor="input-data">Dados de Entrada (JSON):</label>
          <div className="button-group">
            <button 
              onClick={() => console.log('Debug - Available fields:', availableFields)}
              className="debug-button"
            >
              Debug Campos
            </button>
            <button 
              onClick={generateSampleData}
              className="sample-data-btn"
            >
              Gerar Dados de Exemplo
            </button>
          </div>
        </div>
        
        <textarea
          id="input-data"
          value={inputData}
          onChange={(e) => setInputData(e.target.value)}
          placeholder="Digite os dados em formato JSON..."
          rows={8}
          className="input-textarea"
        />
      </div>

      <button
        onClick={handleTestRule}
        disabled={isLoading || !generatedJson}
        className="test-button"
      >
        {isLoading ? 'Processando...' : 'Testar Regra'}
      </button>

      {error && (
        <div className="error-message">
          <strong>Erro:</strong> {error}
        </div>
      )}

      {result !== null && (
        <div className="result-section">
          <h4>Resultado:</h4>
          <div className="result-value">
            <span className={`result-type ${typeof result}`}>
              {typeof result}
            </span>
            <span className="result-content">
              {JSON.stringify(result, null, 2)}
            </span>
          </div>
        </div>
      )}

      {generatedJson && (
        <div className="current-rule">
          <h4>Regra Atual:</h4>
          <pre className="rule-json">
            {JSON.stringify(generatedJson, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default RuleTester;
