import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    // Atualiza o estado para que a próxima renderização mostre a UI de fallback.
    return { hasError: true, error: error };
  }

  componentDidCatch(error, errorInfo) {
    // Você também pode logar o erro para um serviço de monitoramento
    console.error("Erro capturado pelo Error Boundary:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      // Renderiza a UI de fallback customizada
      return (
        <div className="error-boundary">
          <h2>Algo deu errado.</h2>
          <p>Por favor, atualize a página. Se o erro persistir, verifique o console.</p>
          <details style={{ whiteSpace: 'pre-wrap' }}>
            {this.state.error && this.state.error.toString()}
          </details>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;