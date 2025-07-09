#!/usr/bin/env python3
"""
Teste de Carga Rápido: Comparação de Performance Sync vs Async
Versão mais enxuta para análise rápida de performance
"""

import sys
import os
import time
import asyncio
import statistics
from typing import Dict, List

# Adiciona o path para importar o módulo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.lib.json_logic import jsonLogic, jsonLogicAsync, jsonLogicAuto


class QuickLoadTest:
    """Teste de carga rápido"""

    def __init__(self):
        self.results = {}

    # ========== FUNÇÕES DE TESTE ==========

    def add_sync(self, a, b):
        """Adição simples síncrona"""
        return a + b

    async def add_async(self, a, b):
        """Adição simples assíncrona"""
        await asyncio.sleep(0.001)  # 1ms de latência simulada
        return a + b

    def multiply_sync(self, a, b):
        """Multiplicação síncrona"""
        result = a * b
        # Simula algum processamento
        for _ in range(10):
            result = (result * 1.001) % 10000
        return int(result)

    async def multiply_async(self, a, b):
        """Multiplicação assíncrona"""
        await asyncio.sleep(0.002)  # 2ms de latência simulada
        result = a * b
        for _ in range(10):
            result = (result * 1.001) % 10000
        return int(result)

    def heavy_calc_sync(self, n):
        """Cálculo pesado síncrono"""
        result = 0
        for i in range(min(n, 1000)):
            result += i ** 2
        return result % 10000

    async def heavy_calc_async(self, n):
        """Cálculo pesado assíncrono"""
        await asyncio.sleep(0.005)  # 5ms de latência simulada
        result = 0
        for i in range(min(n, 1000)):
            result += i ** 2
        return result % 10000

    # ========== CENÁRIOS DE TESTE ==========

    def get_quick_scenarios(self):
        """Retorna cenários de teste rápidos"""
        return [
            {
                "name": "Quick Math",
                "description": "Operações matemáticas simples",
                "iterations": 200,
                "sync_functions": {
                    "add": self.add_sync,
                    "multiply": self.multiply_sync
                },
                "async_functions": {
                    "add": self.add_async,
                    "multiply": self.multiply_async
                },
                "test_data": [{"a": i, "b": i+5} for i in range(1, 21)],
                "rules": [
                    {"apply": ["add", {"var": "a"}, {"var": "b"}]},
                    {"apply": ["multiply", {"var": "a"}, {"var": "b"}]}
                ]
            },
            {
                "name": "Heavy Compute",
                "description": "Operações computacionais pesadas",
                "iterations": 100,
                "sync_functions": {
                    "heavy": self.heavy_calc_sync
                },
                "async_functions": {
                    "heavy": self.heavy_calc_async
                },
                "test_data": [{"n": i * 10} for i in range(1, 11)],
                "rules": [
                    {"apply": ["heavy", {"var": "n"}]}
                ]
            }
        ]

    # ========== EXECUÇÃO DE TESTES ==========

    def measure_sync_performance(self, scenario: Dict) -> Dict:
        """Mede performance síncrona"""
        print(f"  📊 Testando SYNC - {scenario['name']}")
        
        times = []
        errors = 0
        functions = scenario['sync_functions']
        
        start_total = time.perf_counter()
        
        for i in range(scenario['iterations']):
            data_idx = i % len(scenario['test_data'])
            rule_idx = i % len(scenario['rules'])
            
            data = scenario['test_data'][data_idx]
            rule = scenario['rules'][rule_idx]
            
            start = time.perf_counter()
            try:
                jsonLogic(rule, data, functions)
                end = time.perf_counter()
                times.append(end - start)
            except Exception as e:
                errors += 1
                end = time.perf_counter()
                times.append(end - start)
        
        end_total = time.perf_counter()
        total_time = end_total - start_total
        
        return {
            "total_time": total_time,
            "avg_time": statistics.mean(times) if times else 0,
            "median_time": statistics.median(times) if times else 0,
            "min_time": min(times) if times else 0,
            "max_time": max(times) if times else 0,
            "throughput": scenario['iterations'] / total_time if total_time > 0 else 0,
            "errors": errors,
            "success_rate": (scenario['iterations'] - errors) / scenario['iterations'] * 100
        }

    async def measure_async_performance(self, scenario: Dict) -> Dict:
        """Mede performance assíncrona"""
        print(f"  📊 Testando ASYNC - {scenario['name']}")
        
        times = []
        errors = 0
        functions = scenario['async_functions']
        
        start_total = time.perf_counter()
        
        for i in range(scenario['iterations']):
            data_idx = i % len(scenario['test_data'])
            rule_idx = i % len(scenario['rules'])
            
            data = scenario['test_data'][data_idx]
            rule = scenario['rules'][rule_idx]
            
            start = time.perf_counter()
            try:
                await jsonLogicAsync(rule, data, functions)
                end = time.perf_counter()
                times.append(end - start)
            except Exception as e:
                errors += 1
                end = time.perf_counter()
                times.append(end - start)
        
        end_total = time.perf_counter()
        total_time = end_total - start_total
        
        return {
            "total_time": total_time,
            "avg_time": statistics.mean(times) if times else 0,
            "median_time": statistics.median(times) if times else 0,
            "min_time": min(times) if times else 0,
            "max_time": max(times) if times else 0,
            "throughput": scenario['iterations'] / total_time if total_time > 0 else 0,
            "errors": errors,
            "success_rate": (scenario['iterations'] - errors) / scenario['iterations'] * 100
        }

    async def measure_concurrent_performance(self, scenario: Dict, concurrency: int = 5) -> Dict:
        """Mede performance assíncrona com concorrência"""
        print(f"  📊 Testando CONCURRENT ({concurrency}) - {scenario['name']}")
        
        functions = scenario['async_functions']
        
        async def run_batch(batch_size: int):
            tasks = []
            for i in range(batch_size):
                data_idx = i % len(scenario['test_data'])
                rule_idx = i % len(scenario['rules'])
                
                data = scenario['test_data'][data_idx]
                rule = scenario['rules'][rule_idx]
                
                task = jsonLogicAsync(rule, data, functions)
                tasks.append(task)
            
            start = time.perf_counter()
            try:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                end = time.perf_counter()
                
                errors = sum(1 for r in results if isinstance(r, Exception))
                return {
                    "time": end - start,
                    "errors": errors,
                    "success": len(results) - errors
                }
            except Exception:
                end = time.perf_counter()
                return {
                    "time": end - start,
                    "errors": batch_size,
                    "success": 0
                }
        
        times = []
        total_errors = 0
        total_success = 0
        
        start_total = time.perf_counter()
        
        # Executa em lotes concorrentes
        remaining = scenario['iterations']
        while remaining > 0:
            batch_size = min(concurrency, remaining)
            result = await run_batch(batch_size)
            
            times.append(result['time'])
            total_errors += result['errors']
            total_success += result['success']
            remaining -= batch_size
        
        end_total = time.perf_counter()
        total_time = end_total - start_total
        
        return {
            "total_time": total_time,
            "avg_time": statistics.mean(times) if times else 0,
            "throughput": scenario['iterations'] / total_time if total_time > 0 else 0,
            "errors": total_errors,
            "success_rate": total_success / scenario['iterations'] * 100 if scenario['iterations'] > 0 else 0
        }

    def format_results(self, results: Dict) -> str:
        """Formata os resultados"""
        return f"""
    ⏱️  Tempo Total: {results['total_time']:.3f}s
    📈 Throughput: {results['throughput']:.1f} ops/s
    ⌀  Tempo Médio: {results['avg_time']*1000:.2f}ms
    ✅ Taxa Sucesso: {results['success_rate']:.1f}%
    ❌ Erros: {results['errors']}"""

    async def run_quick_test(self):
        """Executa o teste rápido"""
        print("🚀 Teste de Carga Rápido: Sync vs Async Performance")
        print("=" * 60)
        
        scenarios = self.get_quick_scenarios()
        
        for scenario in scenarios:
            print(f"\n🎯 Cenário: {scenario['name']} - {scenario['description']}")
            print(f"📝 Iterações: {scenario['iterations']}")
            print("-" * 40)
            
            # Teste Síncrono
            sync_results = self.measure_sync_performance(scenario)
            
            # Teste Assíncrono Sequencial
            async_results = await self.measure_async_performance(scenario)
            
            # Teste Assíncrono Concorrente
            concurrent_results = await self.measure_concurrent_performance(scenario, concurrency=5)
            
            # Exibe resultados
            print(f"\n📊 RESULTADOS - {scenario['name']}:")
            print("\n🔄 SYNC:")
            print(self.format_results(sync_results))
            
            print("\n⚡ ASYNC:")
            print(self.format_results(async_results))
            
            print("\n🚀 CONCURRENT:")
            print(self.format_results(concurrent_results))
            
            # Análise comparativa
            sync_throughput = sync_results['throughput']
            async_throughput = async_results['throughput']
            concurrent_throughput = concurrent_results['throughput']
            
            print(f"\n📈 COMPARAÇÃO:")
            if async_throughput > sync_throughput:
                improvement = ((async_throughput - sync_throughput) / sync_throughput) * 100
                print(f"  ✅ Async é {improvement:.1f}% mais rápido que Sync")
            else:
                degradation = ((sync_throughput - async_throughput) / sync_throughput) * 100
                print(f"  ⚠️  Async é {degradation:.1f}% mais lento que Sync")
            
            if concurrent_throughput > sync_throughput:
                improvement = ((concurrent_throughput - sync_throughput) / sync_throughput) * 100
                print(f"  🚀 Concurrent é {improvement:.1f}% mais rápido que Sync")
            else:
                degradation = ((sync_throughput - concurrent_throughput) / sync_throughput) * 100
                print(f"  🐌 Concurrent é {degradation:.1f}% mais lento que Sync")
        
        print(f"\n✅ Teste rápido concluído!")


def main():
    """Função principal"""
    quick_test = QuickLoadTest()
    
    try:
        # Executa o teste rápido
        asyncio.run(quick_test.run_quick_test())
        
        print(f"\n🎉 Teste executado com sucesso!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
