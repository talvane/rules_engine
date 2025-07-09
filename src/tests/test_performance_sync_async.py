#!/usr/bin/env python3
"""
Teste de Performance: JSON Logic Sync vs Async
Compara a performance do processamento síncrono vs assíncrono
"""

import sys
import os
import time
import asyncio
import random
from typing import List, Dict, Callable
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Adiciona o path para importar o módulo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.lib.json_logic import jsonLogic, jsonLogicAsync, jsonLogicAuto


class PerformanceTest:
    """Classe para testes de performance sync vs async"""

    def __init__(self):
        self.results = {}

    # ========== FUNÇÕES DE TESTE ==========

    def operacao_simples(self, x, y):
        """Operação matemática simples"""
        return x * y + (x - y)

    def operacao_media(self, lista_numeros):
        """Operação de complexidade média - cálculos com lista"""
        if not lista_numeros:
            return 0
        soma = sum(lista_numeros)
        media = soma / len(lista_numeros)
        variancia = sum((x - media) ** 2 for x in lista_numeros) / len(lista_numeros)
        return round(media + variancia, 2)

    def operacao_complexa(self, texto, pattern, multiplicador):
        """Operação mais complexa - processamento de string"""
        # Simula processamento de string mais pesado
        result = 0
        for i, char in enumerate(texto.lower()):
            if pattern.lower() in char:
                result += ord(char) * multiplicador * (i + 1)
        
        # Adiciona algum processamento adicional
        palavras = texto.split()
        for palavra in palavras:
            result += len(palavra) * multiplicador
        
        return result % 10000

    async def operacao_simples_async(self, x, y):
        """Versão assíncrona da operação simples"""
        # Simula uma pequena latência I/O
        await asyncio.sleep(0.001)  # 1ms
        return x * y + (x - y)

    async def operacao_media_async(self, lista_numeros):
        """Versão assíncrona da operação média"""
        # Simula latência I/O média
        await asyncio.sleep(0.005)  # 5ms
        if not lista_numeros:
            return 0
        soma = sum(lista_numeros)
        media = soma / len(lista_numeros)
        variancia = sum((x - media) ** 2 for x in lista_numeros) / len(lista_numeros)
        return round(media + variancia, 2)

    async def operacao_complexa_async(self, texto, pattern, multiplicador):
        """Versão assíncrona da operação complexa"""
        # Simula latência I/O alta
        await asyncio.sleep(0.010)  # 10ms
        result = 0
        for i, char in enumerate(texto.lower()):
            if pattern.lower() in char:
                result += ord(char) * multiplicador * (i + 1)
        
        palavras = texto.split()
        for palavra in palavras:
            result += len(palavra) * multiplicador
        
        return result % 10000

    def get_sync_functions(self):
        """Retorna funções síncronas"""
        return {
            "op_simples": self.operacao_simples,
            "op_media": self.operacao_media,
            "op_complexa": self.operacao_complexa,
        }

    def get_async_functions(self):
        """Retorna funções assíncronas"""
        return {
            "op_simples": self.operacao_simples_async,
            "op_media": self.operacao_media_async,
            "op_complexa": self.operacao_complexa_async,
        }

    def get_mixed_functions(self):
        """Retorna mix de funções síncronas e assíncronas"""
        return {
            "op_simples": self.operacao_simples,  # Sync
            "op_media": self.operacao_media_async,  # Async
            "op_complexa": self.operacao_complexa,  # Sync
        }

    def gerar_dados_teste(self):
        """Gera dados de teste variados"""
        return [
            {
                "x": random.randint(1, 100),
                "y": random.randint(1, 100),
                "lista": [random.randint(1, 50) for _ in range(10)],
                "texto": f"Texto de teste {random.randint(1, 1000)} com padrão abc",
                "pattern": random.choice(["a", "e", "t", "x"]),
                "mult": random.randint(1, 10)
            }
            for _ in range(100)
        ]

    def gerar_regras_teste(self):
        """Gera regras JSON Logic para teste"""
        return [
            # Regra simples
            {
                "apply": [
                    "op_simples",
                    {"var": "x"},
                    {"var": "y"}
                ]
            },
            # Regra média
            {
                "apply": [
                    "op_media",
                    {"var": "lista"}
                ]
            },
            # Regra complexa
            {
                "apply": [
                    "op_complexa",
                    {"var": "texto"},
                    {"var": "pattern"},
                    {"var": "mult"}
                ]
            },
            # Regra combinada
            {
                "+": [
                    {
                        "apply": [
                            "op_simples",
                            {"var": "x"},
                            {"var": "y"}
                        ]
                    },
                    {
                        "apply": [
                            "op_media",
                            {"var": "lista"}
                        ]
                    }
                ]
            },
            # Regra condicional
            {
                "if": [
                    {">": [{"var": "x"}, 50]},
                    {
                        "apply": [
                            "op_complexa",
                            {"var": "texto"},
                            {"var": "pattern"},
                            {"var": "mult"}
                        ]
                    },
                    {
                        "apply": [
                            "op_simples",
                            {"var": "x"},
                            {"var": "y"}
                        ]
                    }
                ]
            }
        ]

    def executar_teste_sync(self, num_execucoes=1000):
        """Executa teste síncrono"""
        print(f"🔄 Executando teste SÍNCRONO ({num_execucoes} execuções)")
        print("-" * 50)

        functions = self.get_sync_functions()
        dados_teste = self.gerar_dados_teste()
        regras_teste = self.gerar_regras_teste()

        sucessos = 0
        erros = 0
        tempos = []

        inicio_total = time.time()

        for i in range(num_execucoes):
            regra = random.choice(regras_teste)
            dados = random.choice(dados_teste)

            try:
                inicio = time.time()
                resultado = jsonLogic(regra, dados, functions)
                fim = time.time()

                tempo_execucao = fim - inicio
                tempos.append(tempo_execucao)
                sucessos += 1

            except Exception as e:
                erros += 1
                if erros <= 3:
                    print(f"   ❌ Erro sync {i+1}: {e}")

        fim_total = time.time()
        tempo_total = fim_total - inicio_total

        # Calcula estatísticas
        tempo_medio = sum(tempos) / len(tempos) if tempos else 0
        tempo_min = min(tempos) if tempos else 0
        tempo_max = max(tempos) if tempos else 0

        resultado = {
            "tipo": "sync",
            "execucoes": num_execucoes,
            "sucessos": sucessos,
            "erros": erros,
            "tempo_total": tempo_total,
            "tempo_medio": tempo_medio,
            "tempo_min": tempo_min,
            "tempo_max": tempo_max,
            "throughput": sucessos / tempo_total if tempo_total > 0 else 0
        }

        self.results["sync"] = resultado
        self.imprimir_resultado_sync(resultado)
        return resultado

    async def executar_teste_async(self, num_execucoes=1000):
        """Executa teste assíncrono"""
        print(f"\n🔄 Executando teste ASSÍNCRONO ({num_execucoes} execuções)")
        print("-" * 50)

        functions = self.get_async_functions()
        dados_teste = self.gerar_dados_teste()
        regras_teste = self.gerar_regras_teste()

        sucessos = 0
        erros = 0
        tempos = []

        inicio_total = time.time()

        for i in range(num_execucoes):
            regra = random.choice(regras_teste)
            dados = random.choice(dados_teste)

            try:
                inicio = time.time()
                resultado = await jsonLogicAsync(regra, dados, functions)
                fim = time.time()

                tempo_execucao = fim - inicio
                tempos.append(tempo_execucao)
                sucessos += 1

            except Exception as e:
                erros += 1
                if erros <= 3:
                    print(f"   ❌ Erro async {i+1}: {e}")

        fim_total = time.time()
        tempo_total = fim_total - inicio_total

        # Calcula estatísticas
        tempo_medio = sum(tempos) / len(tempos) if tempos else 0
        tempo_min = min(tempos) if tempos else 0
        tempo_max = max(tempos) if tempos else 0

        resultado = {
            "tipo": "async",
            "execucoes": num_execucoes,
            "sucessos": sucessos,
            "erros": erros,
            "tempo_total": tempo_total,
            "tempo_medio": tempo_medio,
            "tempo_min": tempo_min,
            "tempo_max": tempo_max,
            "throughput": sucessos / tempo_total if tempo_total > 0 else 0
        }

        self.results["async"] = resultado
        self.imprimir_resultado_async(resultado)
        return resultado

    async def executar_teste_async_concorrente(self, num_execucoes=1000, concorrencia=10):
        """Executa teste assíncrono com concorrência"""
        print(f"\n🚀 Executando teste ASSÍNCRONO CONCORRENTE ({num_execucoes} execuções, {concorrencia} concorrentes)")
        print("-" * 60)

        functions = self.get_async_functions()
        dados_teste = self.gerar_dados_teste()
        regras_teste = self.gerar_regras_teste()

        sucessos = 0
        erros = 0
        tempos = []

        async def executar_lote(lote_size):
            nonlocal sucessos, erros, tempos
            tasks = []
            
            for _ in range(lote_size):
                regra = random.choice(regras_teste)
                dados = random.choice(dados_teste)
                
                async def executar_regra():
                    try:
                        inicio = time.time()
                        resultado = await jsonLogicAsync(regra, dados, functions)
                        fim = time.time()
                        return fim - inicio, True, None
                    except Exception as e:
                        return 0, False, str(e)
                
                tasks.append(executar_regra())
            
            results = await asyncio.gather(*tasks)
            
            for tempo, sucesso, erro in results:
                if sucesso:
                    sucessos += 1
                    tempos.append(tempo)
                else:
                    erros += 1

        inicio_total = time.time()

        # Executa em lotes concorrentes
        lotes = [concorrencia] * (num_execucoes // concorrencia)
        if num_execucoes % concorrencia:
            lotes.append(num_execucoes % concorrencia)

        for lote_size in lotes:
            await executar_lote(lote_size)

        fim_total = time.time()
        tempo_total = fim_total - inicio_total

        # Calcula estatísticas
        tempo_medio = sum(tempos) / len(tempos) if tempos else 0
        tempo_min = min(tempos) if tempos else 0
        tempo_max = max(tempos) if tempos else 0

        resultado = {
            "tipo": "async_concurrent",
            "execucoes": num_execucoes,
            "concorrencia": concorrencia,
            "sucessos": sucessos,
            "erros": erros,
            "tempo_total": tempo_total,
            "tempo_medio": tempo_medio,
            "tempo_min": tempo_min,
            "tempo_max": tempo_max,
            "throughput": sucessos / tempo_total if tempo_total > 0 else 0
        }

        self.results["async_concurrent"] = resultado
        self.imprimir_resultado_async_concurrent(resultado)
        return resultado

    async def executar_teste_mixed(self, num_execucoes=1000):
        """Executa teste com funções mistas usando jsonLogicAuto"""
        print(f"\n🎯 Executando teste MISTO (jsonLogicAuto) ({num_execucoes} execuções)")
        print("-" * 60)

        functions = self.get_mixed_functions()
        dados_teste = self.gerar_dados_teste()
        regras_teste = self.gerar_regras_teste()

        sucessos = 0
        erros = 0
        tempos = []

        inicio_total = time.time()

        for i in range(num_execucoes):
            regra = random.choice(regras_teste)
            dados = random.choice(dados_teste)

            try:
                inicio = time.time()
                resultado = jsonLogicAuto(regra, dados, functions)
                
                # Se retornou uma corrotina, aguarda
                if asyncio.iscoroutine(resultado):
                    resultado = await resultado
                
                fim = time.time()

                tempo_execucao = fim - inicio
                tempos.append(tempo_execucao)
                sucessos += 1

            except Exception as e:
                erros += 1
                if erros <= 3:
                    print(f"   ❌ Erro mixed {i+1}: {e}")

        fim_total = time.time()
        tempo_total = fim_total - inicio_total

        # Calcula estatísticas
        tempo_medio = sum(tempos) / len(tempos) if tempos else 0
        tempo_min = min(tempos) if tempos else 0
        tempo_max = max(tempos) if tempos else 0

        resultado = {
            "tipo": "mixed",
            "execucoes": num_execucoes,
            "sucessos": sucessos,
            "erros": erros,
            "tempo_total": tempo_total,
            "tempo_medio": tempo_medio,
            "tempo_min": tempo_min,
            "tempo_max": tempo_max,
            "throughput": sucessos / tempo_total if tempo_total > 0 else 0
        }

        self.results["mixed"] = resultado
        self.imprimir_resultado_mixed(resultado)
        return resultado

    def imprimir_resultado_sync(self, resultado):
        """Imprime resultado do teste síncrono"""
        print("📊 Resultados SYNC:")
        print(f"   ✅ Sucessos: {resultado['sucessos']}")
        print(f"   ❌ Erros: {resultado['erros']}")
        print(f"   ⏱️  Tempo total: {resultado['tempo_total']:.3f}s")
        print(f"   📈 Tempo médio: {resultado['tempo_medio']*1000:.3f}ms")
        print(f"   🚀 Throughput: {resultado['throughput']:.0f} ops/s")

    def imprimir_resultado_async(self, resultado):
        """Imprime resultado do teste assíncrono"""
        print("📊 Resultados ASYNC:")
        print(f"   ✅ Sucessos: {resultado['sucessos']}")
        print(f"   ❌ Erros: {resultado['erros']}")
        print(f"   ⏱️  Tempo total: {resultado['tempo_total']:.3f}s")
        print(f"   📈 Tempo médio: {resultado['tempo_medio']*1000:.3f}ms")
        print(f"   🚀 Throughput: {resultado['throughput']:.0f} ops/s")

    def imprimir_resultado_async_concurrent(self, resultado):
        """Imprime resultado do teste assíncrono concorrente"""
        print("📊 Resultados ASYNC CONCURRENT:")
        print(f"   ✅ Sucessos: {resultado['sucessos']}")
        print(f"   ❌ Erros: {resultado['erros']}")
        print(f"   🔗 Concorrência: {resultado['concorrencia']}")
        print(f"   ⏱️  Tempo total: {resultado['tempo_total']:.3f}s")
        print(f"   📈 Tempo médio: {resultado['tempo_medio']*1000:.3f}ms")
        print(f"   🚀 Throughput: {resultado['throughput']:.0f} ops/s")

    def imprimir_resultado_mixed(self, resultado):
        """Imprime resultado do teste misto"""
        print("📊 Resultados MIXED (jsonLogicAuto):")
        print(f"   ✅ Sucessos: {resultado['sucessos']}")
        print(f"   ❌ Erros: {resultado['erros']}")
        print(f"   ⏱️  Tempo total: {resultado['tempo_total']:.3f}s")
        print(f"   📈 Tempo médio: {resultado['tempo_medio']*1000:.3f}ms")
        print(f"   🚀 Throughput: {resultado['throughput']:.0f} ops/s")

    def comparar_resultados(self):
        """Compara os resultados dos testes"""
        print("\n" + "=" * 80)
        print("📊 COMPARAÇÃO DE PERFORMANCE: SYNC vs ASYNC")
        print("=" * 80)

        if "sync" not in self.results or "async" not in self.results:
            print("❌ Nem todos os testes foram executados")
            return

        sync = self.results["sync"]
        async_result = self.results["async"]

        print(f"{'Métrica':<25} {'SYNC':<15} {'ASYNC':<15} {'Diferença':<15}")
        print("-" * 70)

        # Throughput
        sync_throughput = sync['throughput']
        async_throughput = async_result['throughput']
        diff_throughput = ((async_throughput - sync_throughput) / sync_throughput * 100) if sync_throughput > 0 else 0
        print(f"{'Throughput (ops/s)':<25} {sync_throughput:<15.0f} {async_throughput:<15.0f} {diff_throughput:+.1f}%")

        # Tempo médio
        sync_time = sync['tempo_medio'] * 1000
        async_time = async_result['tempo_medio'] * 1000
        diff_time = ((async_time - sync_time) / sync_time * 100) if sync_time > 0 else 0
        print(f"{'Tempo médio (ms)':<25} {sync_time:<15.3f} {async_time:<15.3f} {diff_time:+.1f}%")

        # Tempo total
        sync_total = sync['tempo_total']
        async_total = async_result['tempo_total']
        diff_total = ((async_total - sync_total) / sync_total * 100) if sync_total > 0 else 0
        print(f"{'Tempo total (s)':<25} {sync_total:<15.3f} {async_total:<15.3f} {diff_total:+.1f}%")

        # Taxa de sucesso
        sync_success = (sync['sucessos'] / sync['execucoes'] * 100)
        async_success = (async_result['sucessos'] / async_result['execucoes'] * 100)
        print(f"{'Taxa de sucesso (%)':<25} {sync_success:<15.1f} {async_success:<15.1f}")

        # Conclusões
        print("\n📋 CONCLUSÕES:")
        if async_throughput > sync_throughput:
            print(f"✅ ASYNC é {(async_throughput/sync_throughput):.1f}x mais rápido em throughput")
        else:
            print(f"⚠️  SYNC é {(sync_throughput/async_throughput):.1f}x mais rápido em throughput")

        if "async_concurrent" in self.results:
            concurrent = self.results["async_concurrent"]
            concurrent_throughput = concurrent['throughput']
            print(f"🚀 ASYNC CONCURRENT: {concurrent_throughput:.0f} ops/s ({(concurrent_throughput/sync_throughput):.1f}x sync)")

        # Recomendações
        print("\n🎯 RECOMENDAÇÕES:")
        print("✅ Use SYNC para: operações rápidas, CPU-intensivas, sem I/O")
        print("✅ Use ASYNC para: operações com I/O, latência de rede, APIs externas")
        print("✅ Use ASYNC CONCURRENT para: múltiplas operações I/O paralelas")
        print("✅ Use jsonLogicAuto para: detectar automaticamente o melhor modo")


async def main():
    """Executa todos os testes de performance"""
    print("🚀 TESTE DE PERFORMANCE: JSON LOGIC SYNC vs ASYNC")
    print("=" * 80)
    print("Comparando performance entre processamento síncrono e assíncrono")
    print("=" * 80)

    teste = PerformanceTest()
    
    # Configuração de testes
    num_execucoes = 1000
    concorrencia = 20

    # Executa testes
    teste.executar_teste_sync(num_execucoes)
    await teste.executar_teste_async(num_execucoes)
    await teste.executar_teste_async_concorrente(num_execucoes, concorrencia)
    await teste.executar_teste_mixed(num_execucoes)
    
    # Compara resultados
    teste.comparar_resultados()

    print("\n🎉 Testes de performance concluídos!")
    print("💡 Os resultados mostram as características de cada abordagem")
    print("📈 Use essas métricas para escolher a melhor estratégia para seu caso")


if __name__ == "__main__":
    asyncio.run(main())
