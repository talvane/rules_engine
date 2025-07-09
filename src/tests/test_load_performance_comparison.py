#!/usr/bin/env python3
"""
Teste de Carga: Comparação de Performance Sync vs Async
Avalia performance sob diferentes cargas de trabalho e cenários
"""

import sys
import os
import time
import asyncio
import random
import statistics
from typing import Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

# Adiciona o path para importar o módulo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.lib.json_logic import jsonLogic, jsonLogicAsync, jsonLogicAuto


class LoadTest:
    """Teste de carga para JSON Logic"""

    def __init__(self):
        self.results = {}

    # ========== FUNÇÕES DE APOIO ==========

    def calc_fibonacci(self, n):
        """Cálculo CPU intensivo - Fibonacci"""
        if n <= 1:
            return n
        return self.calc_fibonacci(n - 1) + self.calc_fibonacci(n - 2)

    async def calc_fibonacci_async(self, n):
        """Versão async do Fibonacci"""
        if n <= 1:
            return n
        # Simula pequena latência entre cálculos
        await asyncio.sleep(0.0001)
        return await self.calc_fibonacci_async(n - 1) + await self.calc_fibonacci_async(n - 2)

    def db_query_simulation(self, query_id, complexity=1):
        """Simula consulta ao banco de dados"""
        # Simula latência de rede/DB
        latency = random.uniform(0.001, 0.01) * complexity
        time.sleep(latency)
        
        # Simula processamento de dados
        result = query_id * random.randint(1, 100)
        for i in range(complexity * 10):
            result = (result * 1.1) % 10000
        
        return int(result)

    async def db_query_simulation_async(self, query_id, complexity=1):
        """Versão async da simulação de DB"""
        # Simula latência async de rede/DB
        latency = random.uniform(0.001, 0.01) * complexity
        await asyncio.sleep(latency)
        
        # Simula processamento de dados
        result = query_id * random.randint(1, 100)
        for i in range(complexity * 10):
            result = (result * 1.1) % 10000
        
        return int(result)

    def process_text(self, text, pattern="test"):
        """Processamento de texto CPU intensivo"""
        result = 0
        words = text.split()
        
        for word in words:
            # Operações custosas com strings
            if pattern.lower() in word.lower():
                result += len(word) * ord(word[0])
            
            # Mais processamento
            for char in word:
                result += ord(char)
        
        return result % 10000

    async def process_text_async(self, text, pattern="test"):
        """Versão async do processamento de texto"""
        result = 0
        words = text.split()
        
        for word in words:
            # Simula latência entre processamentos
            await asyncio.sleep(0.0001)
            
            if pattern.lower() in word.lower():
                result += len(word) * ord(word[0])
            
            for char in word:
                result += ord(char)
        
        return result % 10000

    # ========== CENÁRIOS DE TESTE ==========

    def get_light_load_scenario(self):
        """Cenário de carga leve - operações simples"""
        async def add_async(a, b):
            return a + b
        
        async def multiply_async(a, b):
            return a * b
        
        async def power_async(a, b):
            return a ** b if b <= 10 else a * 10
        
        return {
            "name": "Light Load",
            "description": "Operações matemáticas básicas",
            "iterations": 1000,
            "sync_functions": {
                "add": lambda a, b: a + b,
                "multiply": lambda a, b: a * b,
                "power": lambda a, b: a ** b if b <= 10 else a * 10
            },
            "async_functions": {
                "add": add_async,
                "multiply": multiply_async,
                "power": power_async
            },
            "test_data": [
                {"a": random.randint(1, 100), "b": random.randint(1, 10)}
                for _ in range(100)
            ],
            "rules": [
                {"apply": ["add", {"var": "a"}, {"var": "b"}]},
                {"apply": ["multiply", {"var": "a"}, {"var": "b"}]},
                {"apply": ["power", {"var": "a"}, 2]}
            ]
        }

    def get_medium_load_scenario(self):
        """Cenário de carga média - operações com I/O simulado"""
        async def calc_fib_async(n):
            """Versão async limitada do Fibonacci"""
            limited_n = min(n, 15)  # Limita para evitar explosão
            return self.calc_fibonacci(limited_n)
        
        return {
            "name": "Medium Load", 
            "description": "Simulação de consultas DB + processamento",
            "iterations": 500,
            "sync_functions": {
                "db_query": self.db_query_simulation,
                "calc_fib": lambda n: self.calc_fibonacci(min(n, 15)),  # Limita para evitar explosão
                "process_data": self.process_text
            },
            "async_functions": {
                "db_query": self.db_query_simulation_async,
                "calc_fib": calc_fib_async,
                "process_data": self.process_text_async
            },
            "test_data": [
                {
                    "query_id": random.randint(1, 1000),
                    "fib_n": random.randint(5, 12),
                    "text": f"test data processing {random.randint(1, 100)} complex text analysis",
                    "complexity": random.randint(1, 3)
                }
                for _ in range(100)
            ],
            "rules": [
                {"apply": ["db_query", {"var": "query_id"}, {"var": "complexity"}]},
                {"apply": ["calc_fib", {"var": "fib_n"}]},
                {"apply": ["process_data", {"var": "text"}]}
            ]
        }

    def get_heavy_load_scenario(self):
        """Cenário de carga pesada - operações intensivas"""
        complex_text = " ".join([
            f"complex processing test data item {i} with extensive content"
            for i in range(50)
        ])
        
        async def heavy_calc_async(a, b):
            """Versão async do cálculo pesado"""
            return (a * b) % 10000 + sum(range(min(a, 100)))
        
        return {
            "name": "Heavy Load",
            "description": "Operações CPU/I/O intensivas",
            "iterations": 200,
            "sync_functions": {
                "heavy_db": lambda query_id, comp: self.db_query_simulation(query_id, comp),
                "heavy_text": lambda text: self.process_text(text),
                "heavy_calc": lambda a, b: (a * b) % 10000 + sum(range(min(a, 100)))
            },
            "async_functions": {
                "heavy_db": self.db_query_simulation_async,
                "heavy_text": self.process_text_async,
                "heavy_calc": heavy_calc_async
            },
            "test_data": [
                {
                    "query_id": random.randint(1, 10000),
                    "complexity": random.randint(3, 5),
                    "text": complex_text,
                    "a": random.randint(10, 200),
                    "b": random.randint(10, 200)
                }
                for _ in range(50)
            ],
            "rules": [
                {"apply": ["heavy_db", {"var": "query_id"}, {"var": "complexity"}]},
                {"apply": ["heavy_text", {"var": "text"}]},
                {"apply": ["heavy_calc", {"var": "a"}, {"var": "b"}]}
            ]
        }

    # ========== EXECUÇÃO DE TESTES ==========

    def measure_sync_performance(self, scenario: Dict) -> Dict:
        """Mede performance síncrona"""
        print(f"  📊 Testando SYNC - {scenario['name']}")
        
        times = []
        errors = 0
        
        start_total = time.perf_counter()
        
        for i in range(scenario['iterations']):
            data_idx = i % len(scenario['test_data'])
            rule_idx = i % len(scenario['rules'])
            
            data = scenario['test_data'][data_idx]
            rule = scenario['rules'][rule_idx]
            
            start = time.perf_counter()
            try:
                jsonLogic(rule, data, scenario['sync_functions'])
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
            "std_dev": statistics.stdev(times) if len(times) > 1 else 0,
            "throughput": scenario['iterations'] / total_time,
            "errors": errors,
            "success_rate": (scenario['iterations'] - errors) / scenario['iterations'] * 100
        }

    async def measure_async_performance(self, scenario: Dict) -> Dict:
        """Mede performance assíncrona"""
        print(f"  📊 Testando ASYNC - {scenario['name']}")
        
        times = []
        errors = 0
        
        start_total = time.perf_counter()
        
        for i in range(scenario['iterations']):
            data_idx = i % len(scenario['test_data'])
            rule_idx = i % len(scenario['rules'])
            
            data = scenario['test_data'][data_idx]
            rule = scenario['rules'][rule_idx]
            
            start = time.perf_counter()
            try:
                await jsonLogicAsync(rule, data, scenario['async_functions'])
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
            "std_dev": statistics.stdev(times) if len(times) > 1 else 0,
            "throughput": scenario['iterations'] / total_time,
            "errors": errors,
            "success_rate": (scenario['iterations'] - errors) / scenario['iterations'] * 100
        }

    async def measure_concurrent_async_performance(self, scenario: Dict, concurrency: int = 10) -> Dict:
        """Mede performance assíncrona com concorrência"""
        print(f"  📊 Testando ASYNC CONCURRENT ({concurrency}) - {scenario['name']}")
        
        async def run_batch(batch_size: int):
            tasks = []
            for i in range(batch_size):
                data_idx = i % len(scenario['test_data'])
                rule_idx = i % len(scenario['rules'])
                
                data = scenario['test_data'][data_idx]
                rule = scenario['rules'][rule_idx]
                
                task = jsonLogicAsync(rule, data, scenario['async_functions'])
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
            "median_time": statistics.median(times) if times else 0,
            "min_time": min(times) if times else 0,
            "max_time": max(times) if times else 0,
            "std_dev": statistics.stdev(times) if len(times) > 1 else 0,
            "throughput": scenario['iterations'] / total_time,
            "errors": total_errors,
            "success_rate": total_success / scenario['iterations'] * 100 if scenario['iterations'] > 0 else 0
        }

    def format_performance_results(self, results: Dict) -> str:
        """Formata os resultados de performance"""
        return f"""
    ⏱️  Tempo Total: {results['total_time']:.3f}s
    📈 Throughput: {results['throughput']:.1f} ops/s
    ⌀  Tempo Médio: {results['avg_time']*1000:.2f}ms
    📊 Tempo Mediano: {results['median_time']*1000:.2f}ms
    ⬇️  Tempo Mín: {results['min_time']*1000:.2f}ms
    ⬆️  Tempo Máx: {results['max_time']*1000:.2f}ms
    📏 Desvio Padrão: {results['std_dev']*1000:.2f}ms
    ✅ Taxa Sucesso: {results['success_rate']:.1f}%
    ❌ Erros: {results['errors']}
        """

    def calculate_improvement(self, sync_result: Dict, async_result: Dict) -> Dict:
        """Calcula melhorias de performance"""
        return {
            "total_time_improvement": ((sync_result['total_time'] - async_result['total_time']) / sync_result['total_time']) * 100,
            "throughput_improvement": ((async_result['throughput'] - sync_result['throughput']) / sync_result['throughput']) * 100,
            "avg_time_improvement": ((sync_result['avg_time'] - async_result['avg_time']) / sync_result['avg_time']) * 100
        }

    async def run_load_test(self):
        """Executa o teste de carga completo"""
        print("🚀 Iniciando Teste de Carga: Sync vs Async Performance")
        print("=" * 70)
        
        scenarios = [
            self.get_light_load_scenario(),
            self.get_medium_load_scenario(),
            self.get_heavy_load_scenario()
        ]
        
        all_results = {}
        
        for scenario in scenarios:
            print(f"\n🎯 Cenário: {scenario['name']} - {scenario['description']}")
            print(f"📝 Iterações: {scenario['iterations']}")
            print("-" * 50)
            
            # Teste Síncrono
            sync_results = self.measure_sync_performance(scenario)
            
            # Teste Assíncrono Sequencial
            async_results = await self.measure_async_performance(scenario)
            
            # Teste Assíncrono Concorrente
            concurrent_results = await self.measure_concurrent_async_performance(scenario, concurrency=10)
            
            # Análise dos resultados
            sync_vs_async = self.calculate_improvement(sync_results, async_results)
            sync_vs_concurrent = self.calculate_improvement(sync_results, concurrent_results)
            
            all_results[scenario['name']] = {
                "sync": sync_results,
                "async": async_results,
                "concurrent": concurrent_results,
                "improvements": {
                    "sync_vs_async": sync_vs_async,
                    "sync_vs_concurrent": sync_vs_concurrent
                }
            }
            
            # Exibe resultados
            print(f"\n📊 RESULTADOS - {scenario['name']}:")
            print("\n🔄 SYNC:")
            print(self.format_performance_results(sync_results))
            
            print("\n⚡ ASYNC:")
            print(self.format_performance_results(async_results))
            
            print("\n🚀 ASYNC CONCURRENT:")
            print(self.format_performance_results(concurrent_results))
            
            print("\n📈 MELHORIAS:")
            print(f"  • Async vs Sync:")
            print(f"    - Tempo Total: {sync_vs_async['total_time_improvement']:+.1f}%")
            print(f"    - Throughput: {sync_vs_async['throughput_improvement']:+.1f}%")
            print(f"    - Tempo Médio: {sync_vs_async['avg_time_improvement']:+.1f}%")
            
            print(f"  • Concurrent vs Sync:")
            print(f"    - Tempo Total: {sync_vs_concurrent['total_time_improvement']:+.1f}%")
            print(f"    - Throughput: {sync_vs_concurrent['throughput_improvement']:+.1f}%")
            print(f"    - Tempo Médio: {sync_vs_concurrent['avg_time_improvement']:+.1f}%")
        
        # Resumo geral
        print("\n" + "=" * 70)
        print("📋 RESUMO GERAL")
        print("=" * 70)
        
        for scenario_name, results in all_results.items():
            sync_throughput = results['sync']['throughput']
            async_throughput = results['async']['throughput']
            concurrent_throughput = results['concurrent']['throughput']
            
            print(f"\n🎯 {scenario_name}:")
            print(f"  📊 Throughput (ops/s):")
            print(f"     - Sync: {sync_throughput:.1f}")
            print(f"     - Async: {async_throughput:.1f} ({results['improvements']['sync_vs_async']['throughput_improvement']:+.1f}%)")
            print(f"     - Concurrent: {concurrent_throughput:.1f} ({results['improvements']['sync_vs_concurrent']['throughput_improvement']:+.1f}%)")
        
        print(f"\n✅ Teste de carga concluído!")
        return all_results


def main():
    """Função principal"""
    load_test = LoadTest()
    
    try:
        # Executa o teste de carga
        results = asyncio.run(load_test.run_load_test())
        
        print(f"\n🎉 Todos os testes de carga foram executados com sucesso!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro durante o teste de carga: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
