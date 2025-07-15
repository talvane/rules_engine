from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Adiciona o diretório src ao path para importar as bibliotecas
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from lib.json_logic import jsonLogic

app = Flask(__name__)
CORS(app)  # Permite requisições do frontend React


@app.route("/api/process-rule", methods=["POST"])
def process_rule():
    """
    Endpoint para processar uma regra JSON Logic com dados de entrada.

    Esperado no body da requisição:
    {
        "rule": { ... },  // Regra em formato JSON Logic
        "data": { ... }   // Dados de entrada para processar
    }
    """
    try:
        # Obtém os dados da requisição
        request_data = request.get_json()

        if not request_data:
            return jsonify({"error": "Nenhum dado fornecido na requisição"}), 400

        rule = request_data.get("rule")
        data = request_data.get("data", {})

        if not rule:
            return jsonify({"error": "Regra não fornecida"}), 400

        # Processa a regra usando o JSON Logic
        result = jsonLogic(rule, data)

        return jsonify({"success": True, "result": result, "rule": rule, "data": data})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health_check():
    """Endpoint para verificar se o servidor está funcionando."""
    return jsonify(
        {"status": "healthy", "message": "Servidor JSON Logic está funcionando"}
    )


@app.route("/api/validate-rule", methods=["POST"])
def validate_rule():
    """
    Endpoint para validar uma regra JSON Logic sem processar dados.

    Esperado no body da requisição:
    {
        "rule": { ... }  // Regra em formato JSON Logic
    }
    """
    try:
        request_data = request.get_json()

        if not request_data:
            return jsonify({"error": "Nenhum dado fornecido na requisição"}), 400

        rule = request_data.get("rule")

        if not rule:
            return jsonify({"error": "Regra não fornecida"}), 400

        # Tenta processar a regra com dados vazios para validar
        try:
            jsonLogic(rule, {})
            return jsonify({"valid": True, "message": "Regra válida"})
        except Exception as validation_error:
            return jsonify({"valid": False, "error": str(validation_error)})

    except Exception as e:
        return jsonify({"valid": False, "error": str(e)}), 500


if __name__ == "__main__":
    print("Iniciando servidor JSON Logic...")
    print("Endpoints disponíveis:")
    print("  POST /api/process-rule - Processar regra com dados")
    print("  POST /api/validate-rule - Validar regra")
    print("  GET  /api/health - Verificar saúde do servidor")
    print("\nServidor rodando em http://localhost:5000")

    app.run(debug=True, host="0.0.0.0", port=5000)
