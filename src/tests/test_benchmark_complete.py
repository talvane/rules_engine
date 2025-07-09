#!/usr/bin/env python3
"""
Benchmark Completo: JSON Logic Sync vs Async
Análise detalhada de performance em diferentes cenários
"""

import sys
import os
import time
import asyncio
import random
from typing import Dict, List

# Adiciona o path para importar o módulo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.lib.json_logic import jsonLogic, jsonLogicAsync, jsonLogicAuto


class PerformanceBenchmark:
    """Benchmark completo de performance"""

    def __init__(self):
        self.results = {}

    # ========== CENÁRIOS DE TESTE ==========

    def get_scenario_fast_cpu(self):
        """Cenário: Operações rápidas de CPU"""
        def calc_simples(a, b, c):
            return (a * b) + (c / 2)

        async def calc_simples_async(a, b, c):
            # Sem await - apenas overhead async
            return (a * b) + (c / 2)

        return {
            "name": "Fast CPU",
            "description": "Operações matemáticas simples",
            "sync_functions": {"calc": calc_simples},
            "async_functions": {"calc": calc_simples_async},
            "data": {"a": 10, "b": 5, "c": 20},
            "rule": {"apply": ["calc", {"var": "a"}, {"var": "b"}, {"var": "c"}]}
        }

    def get_scenario_io_simulation(self):
        """Cenário: Simulação de operações I/O"""
        def fetch_data_sync(user_id):
            # Simula I/O bloqueante
            time.sleep(0.001)  # 1ms
            return f"user_{user_id}_data"

        async def fetch_data_async(user_id):
            # Simula I/O não-bloqueante
            await asyncio.sleep(0.001)  # 1ms
            return f"user_{user_id}_data"

        return {
            "name": "I/O Simulation",
            "description": "Simulação de operações I/O (1ms latência)",
            "sync_functions": {"fetch": fetch_data_sync},
            "async_functions": {"fetch": fetch_data_async},
            "data": {"user_id": 123},
            "rule": {"apply": ["fetch", {"var": "user_id"}]}
        }

    def get_scenario_complex_logic(self):
        """Cenário: Lógica complexa com múltiplas operações"""
        def process_complex_sync(data_list, threshold):
            filtered = [x for x in data_list if x > threshold]
            squared = [x**2 for x in filtered]
            return sum(squared) / len(squared) if squared else 0

        async def process_complex_async(data_list, threshold):
            await asyncio.sleep(0.002)  # 2ms I/O
            filtered = [x for x in data_list if x > threshold]
            squared = [x**2 for x in filtered]
            return sum(squared) / len(squared) if squared else 0

        return {
            "name": "Complex Logic",
            "description": "Processamento de lista com I/O",
            "sync_functions": {"process": process_complex_sync},
            "async_functions": {"process": process_complex_async},
            "data": {"numbers": [1, 5, 10, 15, 20, 25], "threshold": 10},
            "rule": {"apply": ["process", {"var": "numbers"}, {"var": "threshold"}]}
        }

    def get_scenario_nested_calls(self):
        """Cenário: Chamadas aninhadas"""
        def step1_sync(x):
            return x * 2

        def step2_sync(x):
            return x + 10

        async def step1_async(x):
            await asyncio.sleep(0.0005)  # 0.5ms
            return x * 2

        async def step2_async(x):
            await asyncio.sleep(0.0005)  # 0.5ms
            return x + 10

        return {
            "name": "Nested Calls",
            "description": "Operações aninhadas com I/O",
            "sync_functions": {"step1": step1_sync, "step2": step2_sync},
            "async_functions": {"step1": step1_async, "step2": step2_async},
            "data": {"value": 5},
            "rule": {
                "apply": [
                    "step2",
                    {"apply": ["step1", {"var": "value"}]}
                ]
            }
        }

    async def run_scenario_benchmark(self, scenario: Dict, iterations: int = 100):
        """Executa benchmark para um cenário específico"""
        print(f"\n🎯 CENÁRIO: {scenario['name']}")
        print(f"📝 {scenario['description']}")
        print("-" * 50)

        results = {}

        # Teste SYNC
        print("🔄 Testando SYNC...")
        start_time = time.time()
        sync_times = []
        
        for _ in range(iterations):
            iter_start = time.time()
            result = jsonLogic(scenario['rule'], scenario['data'], scenario['sync_functions'])
            iter_end = time.time()
            sync_times.append(iter_end - iter_start)
        
        sync_total_time = time.time() - start_time
        
        results['sync'] = {
            'total_time': sync_total_time,
            'avg_time': sum(sync_times) / len(sync_times),
            'min_time': min(sync_times),
            'max_time': max(sync_times),
            'throughput': iterations / sync_total_time
        }

        # Teste ASYNC (sequencial)
        print("🔄 Testando ASYNC Sequencial...")
        start_time = time.time()
        async_times = []
        
        for _ in range(iterations):
            iter_start = time.time()
            result = await jsonLogicAsync(scenario['rule'], scenario['data'], scenario['async_functions'])
            iter_end = time.time()
            async_times.append(iter_end - iter_start)
        
        async_total_time = time.time() - start_time
        
        results['async_sequential'] = {
            'total_time': async_total_time,
            'avg_time': sum(async_times) / len(async_times),
            'min_time': min(async_times),
            'max_time': max(async_times),
            'throughput': iterations / async_total_time
        }

        # Teste ASYNC (concorrente)
        print("🚀 Testando ASYNC Concorrente...")
        batch_size = 10
        batches = iterations // batch_size
        
        async def run_batch():
            tasks = []
            for _ in range(batch_size):
                task = jsonLogicAsync(scenario['rule'], scenario['data'], scenario['async_functions'])
                tasks.append(task)
            return await asyncio.gather(*tasks)
        
        start_time = time.time()
        for _ in range(batches):
            await run_batch()
        concurrent_total_time = time.time() - start_time
        
        results['async_concurrent'] = {
            'total_time': concurrent_total_time,
            'avg_time': concurrent_total_time / iterations,
            'throughput': iterations / concurrent_total_time
        }

        # Teste jsonLogicAuto
        print("🎯 Testando jsonLogicAuto...")
        start_time = time.time()
        auto_times = []
        
        for _ in range(iterations):
            iter_start = time.time()
            result = jsonLogicAuto(scenario['rule'], scenario['data'], scenario['async_functions'])
            if asyncio.iscoroutine(result):
                result = await result
            iter_end = time.time()
            auto_times.append(iter_end - iter_start)
        
        auto_total_time = time.time() - start_time
        
        results['auto'] = {
            'total_time': auto_total_time,
            'avg_time': sum(auto_times) / len(auto_times),
            'throughput': iterations / auto_total_time
        }

        # Imprime resultados
        self.print_scenario_results(scenario['name'], results, iterations)
        return results

    def print_scenario_results(self, scenario_name: str, results: Dict, iterations: int):
        """Imprime resultados de um cenário"""
        print(f"\n📊 Resultados - {scenario_name} ({iterations} iterações):")
        print(f"{'Método':<20} {'Tempo Total':<12} {'Tempo Médio':<12} {'Throughput':<12} {'Speedup':<10}")
        print("-" * 75)
        
        sync_throughput = results['sync']['throughput']
        
        for method, data in results.items():
            method_name = {
                'sync': 'SYNC',
                'async_sequential': 'ASYNC Seq',
                'async_concurrent': 'ASYNC Conc',
                'auto': 'Auto'
            }[method]
            
            speedup = data['throughput'] / sync_throughput
            
            print(f"{method_name:<20} {data['total_time']:<12.3f} {data['avg_time']*1000:<12.3f} {data['throughput']:<12.0f} {speedup:<10.2f}x")

        # Identifica o melhor método
        best_method = max(results.keys(), key=lambda k: results[k]['throughput'])
        best_name = {
            'sync': 'SYNC',
            'async_sequential': 'ASYNC Sequencial',
            'async_concurrent': 'ASYNC Concorrente',
            'auto': 'jsonLogicAuto'
        }[best_method]
        
        print(f"\n🏆 Melhor performance: {best_name} ({results[best_method]['throughput']:.0f} ops/s)")

    async def run_full_benchmark(self):
        """Executa benchmark completo"""
        print("🚀 BENCHMARK COMPLETO: JSON Logic Sync vs Async")
        print("=" * 70)
        print("Análise detalhada de performance em diferentes cenários")
        print("=" * 70)

        scenarios = [
            self.get_scenario_fast_cpu(),
            self.get_scenario_io_simulation(),
            self.get_scenario_complex_logic(),
            self.get_scenario_nested_calls()
        ]

        all_results = {}
        iterations = 50  # Menor para ser mais rápido

        for scenario in scenarios:
            results = await self.run_scenario_benchmark(scenario, iterations)
            all_results[scenario['name']] = results

        # Resumo final
        self.print_final_summary(all_results)

    def print_final_summary(self, all_results: Dict):
        """Imprime resumo final com recomendações"""
        print("\n" + "=" * 70)
        print("📋 RESUMO FINAL E RECOMENDAÇÕES")
        print("=" * 70)

        print("\n🏆 MELHOR PERFORMANCE POR CENÁRIO:")
        for scenario_name, results in all_results.items():
            best_method = max(results.keys(), key=lambda k: results[k]['throughput'])
            best_throughput = results[best_method]['throughput']
            
            method_names = {
                'sync': 'SYNC',
                'async_sequential': 'ASYNC Sequencial',
                'async_concurrent': 'ASYNC Concorrente',
                'auto': 'jsonLogicAuto'
            }
            
            print(f"   {scenario_name:<20}: {method_names[best_method]:<15} ({best_throughput:.0f} ops/s)")

        print("\n🎯 RECOMENDAÇÕES DE USO:")
        print("✅ SYNC:")
        print("   • Operações CPU-intensivas rápidas")
        print("   • Cálculos matemáticos simples")
        print("   • Quando não há I/O ou latência")
        print("   • Melhor para throughput puro")

        print("\n✅ ASYNC Sequencial:")
        print("   • Operações com I/O moderado")
        print("   • Quando há latência de rede/disco")
        print("   • APIs externas síncronas")

        print("\n✅ ASYNC Concorrente:")
        print("   • Múltiplas operações I/O paralelas")
        print("   • Melhor quando pode paralelizar")
        print("   • APIs externas com batching")
        print("   • Excelente para escalabilidade")

        print("\n✅ jsonLogicAuto:")
        print("   • Detecção automática inteligente")
        print("   • Mistura de funções sync/async")
        print("   • Facilita migração gradual")
        print("   • Boa escolha para casos gerais")

        print("\n💡 REGRAS GERAIS:")
        print("• Se não há I/O → use SYNC")
        print("• Se há I/O + pode paralelizar → use ASYNC Concorrente")
        print("• Se não tem certeza → use jsonLogicAuto")
        print("• Meça sempre no seu contexto específico!")


async def main():
    """Executa o benchmark completo"""
    benchmark = PerformanceBenchmark()
    await benchmark.run_full_benchmark()
    
    print("\n🎉 Benchmark concluído!")
    print("📈 Use estes resultados para otimizar sua aplicação")


if __name__ == "__main__":
    asyncio.run(main())
