#!/usr/bin/env python3
"""
Teste simples para verificar funcionamento das operações JSON Logic
"""

import sys
import os
import asyncio

# Adiciona o path para importar o módulo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.lib.json_logic import jsonLogic, jsonLogicAsync


def test_basic_operations():
    """Testa operações básicas"""
    print("🧪 Testando operações básicas do JSON Logic")
    
    # Função simples
    def add(a, b):
        return a + b
    
    async def add_async(a, b):
        return a + b
    
    # Dados de teste
    data = {"a": 10, "b": 5}
    
    # Regra simples
    rule = {"add": [{"var": "a"}, {"var": "b"}]}
    
    print(f"📝 Dados: {data}")
    print(f"📋 Regra: {rule}")
    
    # Teste síncrono
    try:
        result_sync = jsonLogic(rule, data, {"add": add})
        print(f"✅ Sync resultado: {result_sync}")
    except Exception as e:
        print(f"❌ Sync erro: {e}")
    
    # Teste assíncrono
    async def test_async():
        try:
            result_async = await jsonLogicAsync(rule, data, {"add": add_async})
            print(f"✅ Async resultado: {result_async}")
        except Exception as e:
            print(f"❌ Async erro: {e}")
    
    asyncio.run(test_async())


def test_builtin_operations():
    """Testa operações built-in do JSON Logic"""
    print("\n🧪 Testando operações built-in")
    
    data = {"x": 10, "y": 5}
    
    # Operações que devem funcionar sem funções customizadas
    rules = [
        {">": [{"var": "x"}, {"var": "y"}]},  # 10 > 5
        {"<": [{"var": "y"}, {"var": "x"}]},  # 5 < 10
        {"+": [{"var": "x"}, {"var": "y"}]},  # 10 + 5
        {"-": [{"var": "x"}, {"var": "y"}]},  # 10 - 5
        {"*": [{"var": "x"}, {"var": "y"}]},  # 10 * 5
        {"/": [{"var": "x"}, {"var": "y"}]},  # 10 / 5
    ]
    
    for rule in rules:
        try:
            result_sync = jsonLogic(rule, data)
            print(f"✅ {rule} = {result_sync}")
        except Exception as e:
            print(f"❌ {rule} erro: {e}")
    
    # Teste async das mesmas operações
    async def test_builtin_async():
        for rule in rules:
            try:
                result_async = await jsonLogicAsync(rule, data)
                print(f"✅ Async {rule} = {result_async}")
            except Exception as e:
                print(f"❌ Async {rule} erro: {e}")
    
    asyncio.run(test_builtin_async())


if __name__ == "__main__":
    test_basic_operations()
    test_builtin_operations()
