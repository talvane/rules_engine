#!/usr/bin/env python3
"""
Exemplo de uso do JsonLogic com suporte a funções assíncronas.

Este exemplo demonstra como usar jsonLogicAsync para executar regras
que incluem funções assíncronas, como chamadas de API, operações de I/O
ou cálculos que se beneficiam de execução assíncrona.
"""

import asyncio
import sys
import os

# Adiciona o diretório lib ao path para importar json_logic
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

from lib.json_logic import jsonLogic, jsonLogicAsync, jsonLogicAuto


# Funções síncronas
def formatar_nome_completo(primeiro, ultimo):
    """Função síncrona para formatar nome completo."""
    return f"{ultimo.upper()}, {primeiro.capitalize()}"


def calcular_area_sync(largura, altura):
    """Função síncrona para calcular área."""
    return largura * altura


# Funções assíncronas
async def buscar_dados_usuario(user_id):
    """
    Simula uma chamada de API assíncrona para buscar dados do usuário.
    """
    print(f"🔍 Buscando dados do usuário {user_id}...")
    await asyncio.sleep(0.5)  # Simula latência de rede
    
    # Simula dados retornados de uma API
    usuarios_db = {
        123: {"nome": "joão", "sobrenome": "silva", "idade": 30, "ativo": True},
        456: {"nome": "maria", "sobrenome": "santos", "idade": 25, "ativo": True},
        789: {"nome": "pedro", "sobrenome": "oliveira", "idade": 35, "ativo": False},
    }
    
    usuario = usuarios_db.get(user_id)
    if not usuario:
        raise ValueError(f"Usuário {user_id} não encontrado")
    
    print(f"✅ Dados encontrados: {usuario}")
    return usuario


async def calcular_area_async(largura, altura):
    """
    Simula um cálculo de área que requer processamento assíncrono.
    """
    print(f"🧮 Calculando área assincronamente: {largura} x {altura}")
    await asyncio.sleep(0.2)  # Simula processamento complexo
    
    resultado = largura * altura
    print(f"✅ Área calculada: {resultado}")
    return resultado


async def validar_documento_async(documento):
    """
    Simula validação assíncrona de documento em serviço externo.
    """
    print(f"📋 Validando documento: {documento}")
    await asyncio.sleep(0.3)  # Simula chamada para serviço de validação
    
    # Simula validação (documentos válidos têm 11 dígitos)
    valido = len(str(documento)) == 11
    print(f"{'✅' if valido else '❌'} Documento {'válido' if valido else 'inválido'}")
    return valido


# Registro de funções (síncronas e assíncronas)
funcoes_permitidas = {
    "format_name": formatar_nome_completo,
    "calc_area_sync": calcular_area_sync,
    "fetch_user": buscar_dados_usuario,
    "calc_area_async": calcular_area_async,
    "validate_doc": validar_documento_async,
}


async def exemplo_basico():
    """Demonstra uso básico de funções assíncronas."""
    print("\n🚀 === EXEMPLO BÁSICO ===")
    
    dados = {"user_id": 123}
    
    # Regra para buscar dados do usuário
    regra_usuario = {
        "apply": ["fetch_user", {"var": "user_id"}]
    }
    
    print("Executando regra para buscar usuário...")
    usuario = await jsonLogicAsync(regra_usuario, dados, funcoes_permitidas)
    print(f"Resultado: {usuario}")


async def exemplo_combinado():
    """Demonstra combinação de funções síncronas e assíncronas."""
    print("\n🔄 === EXEMPLO COMBINADO ===")
    
    dados = {
        "user_id": 456,
        "retangulo": {"largura": 10, "altura": 5}
    }
    
    # Primeiro busca os dados do usuário
    usuario = await jsonLogicAsync(
        {"apply": ["fetch_user", {"var": "user_id"}]},
        dados,
        funcoes_permitidas
    )
    
    # Adiciona os dados do usuário ao contexto
    dados_completos = {**dados, "usuario": usuario}
    
    # Regra complexa que usa tanto funções síncronas quanto assíncronas
    regra_complexa = {
        "and": [
            # Verifica se o usuário está ativo
            {"var": "usuario.ativo"},
            # Calcula área assincronamente e verifica se é maior que 40
            {
                ">": [
                    {
                        "apply": [
                            "calc_area_async",
                            {"var": "retangulo.largura"},
                            {"var": "retangulo.altura"}
                        ]
                    },
                    40
                ]
            },
            # Formata o nome (função síncrona)
            {
                "!=": [
                    {
                        "apply": [
                            "format_name",
                            {"var": "usuario.nome"},
                            {"var": "usuario.sobrenome"}
                        ]
                    },
                    ""
                ]
            }
        ]
    }
    
    print("Executando regra complexa...")
    resultado = await jsonLogicAsync(regra_complexa, dados_completos, funcoes_permitidas)
    print(f"✅ Resultado da regra complexa: {resultado}")
    
    # Formata e exibe o nome
    nome_formatado = await jsonLogicAsync(
        {
            "apply": [
                "format_name",
                {"var": "usuario.nome"},
                {"var": "usuario.sobrenome"}
            ]
        },
        dados_completos,
        funcoes_permitidas
    )
    print(f"👤 Nome formatado: {nome_formatado}")


async def exemplo_validacao():
    """Demonstra validação assíncrona de documentos."""
    print("\n📋 === EXEMPLO VALIDAÇÃO ===")
    
    casos_teste = [
        {"documento": "12345678901", "esperado": True},   # Válido (11 dígitos)
        {"documento": "123456789", "esperado": False},    # Inválido (9 dígitos)
        {"documento": "98765432100", "esperado": True},   # Válido (11 dígitos)
    ]
    
    for caso in casos_teste:
        dados = {"doc": caso["documento"]}
        
        regra_validacao = {
            "apply": ["validate_doc", {"var": "doc"}]
        }
        
        resultado = await jsonLogicAsync(regra_validacao, dados, funcoes_permitidas)
        status = "✅ PASSOU" if resultado == caso["esperado"] else "❌ FALHOU"
        print(f"{status} - Documento: {caso['documento']} - Resultado: {resultado}")


def exemplo_auto_deteccao():
    """Demonstra a detecção automática de funções assíncronas."""
    print("\n🤖 === EXEMPLO AUTO-DETECÇÃO ===")
    
    # Funções apenas síncronas
    funcoes_sync = {
        "format_name": formatar_nome_completo,
        "calc_area": calcular_area_sync,
    }
    
    # Funções com pelo menos uma assíncrona
    funcoes_mixed = {
        "format_name": formatar_nome_completo,
        "fetch_user": buscar_dados_usuario,
    }
    
    dados = {"nome": "ana", "sobrenome": "costa"}
    regra = {"apply": ["format_name", {"var": "nome"}, {"var": "sobrenome"}]}
    
    # Com funções síncronas - retorna resultado diretamente
    resultado_sync = jsonLogicAuto(regra, dados, funcoes_sync)
    print(f"🔄 Resultado síncrono: {resultado_sync}")
    
    # Com funções mistas - retorna corrotina
    resultado_async = jsonLogicAuto(regra, dados, funcoes_mixed)
    print(f"⚡ Tipo do resultado assíncrono: {type(resultado_async)}")
    
    if asyncio.iscoroutine(resultado_async):
        print("🔍 Detectou função assíncrona - retornou corrotina")
        return resultado_async
    else:
        print("🔍 Detectou apenas funções síncronas - retornou resultado diretamente")


async def main():
    """Função principal que executa todos os exemplos."""
    print("🎯 === DEMONSTRAÇÃO JsonLogic com Suporte Assíncrono ===")
    
    # Exemplos assíncronos
    await exemplo_basico()
    await exemplo_combinado()
    await exemplo_validacao()
    
    # Exemplo de auto-detecção
    resultado_auto = exemplo_auto_deteccao()
    if asyncio.iscoroutine(resultado_auto):
        resultado_final = await resultado_auto
        print(f"✅ Resultado final da auto-detecção: {resultado_final}")
    
    print("\n🎉 === DEMONSTRAÇÃO CONCLUÍDA ===")


if __name__ == "__main__":
    # Executa o exemplo principal
    asyncio.run(main())
