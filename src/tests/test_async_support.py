import pytest
import asyncio

from src.lib.json_logic import jsonLogic, jsonLogicAsync, jsonLogicAuto, has_async_functions


class TestAsyncSupport:
    """Testes para o suporte a funções assíncronas no JsonLogic."""

    def test_has_async_functions_detection(self):
        """Testa a detecção de funções assíncronas."""
        # Apenas funções síncronas
        sync_functions = {
            "add": lambda a, b: a + b,
            "multiply": lambda a, b: a * b,
        }
        assert not has_async_functions(sync_functions)

        # Com pelo menos uma função assíncrona
        async def async_func():
            return "async result"

        mixed_functions = {
            "add": lambda a, b: a + b,
            "async_func": async_func,
        }
        assert has_async_functions(mixed_functions)

        # Apenas funções assíncronas
        async_functions = {
            "async1": async_func,
            "async2": async_func,
        }
        assert has_async_functions(async_functions)

    @pytest.mark.asyncio
    async def test_basic_async_function_call(self):
        """Testa chamada básica de função assíncrona."""
        async def multiply_async(a, b):
            await asyncio.sleep(0.01)  # Simula operação assíncrona
            return a * b

        functions = {"multiply_async": multiply_async}
        data = {"x": 5, "y": 3}

        rule = {
            "apply": ["multiply_async", {"var": "x"}, {"var": "y"}]
        }

        result = await jsonLogicAsync(rule, data, functions)
        assert result == 15

    @pytest.mark.asyncio
    async def test_mixed_sync_async_functions(self):
        """Testa combinação de funções síncronas e assíncronas."""
        def add_sync(a, b):
            return a + b

        async def multiply_async(a, b):
            await asyncio.sleep(0.01)
            return a * b

        functions = {
            "add": add_sync,
            "multiply_async": multiply_async
        }

        data = {"x": 5, "y": 3, "z": 2}

        # Regra que usa ambas as funções
        rule = {
            "apply": [
                "add",
                {"apply": ["multiply_async", {"var": "x"}, {"var": "y"}]},
                {"var": "z"}
            ]
        }

        result = await jsonLogicAsync(rule, data, functions)
        assert result == 17  # (5 * 3) + 2 = 17

    @pytest.mark.asyncio
    async def test_complex_async_logic(self):
        """Testa lógica complexa com múltiplas funções assíncronas."""
        async def fetch_user(user_id):
            await asyncio.sleep(0.01)
            users = {
                1: {"name": "João", "age": 30, "active": True},
                2: {"name": "Maria", "age": 25, "active": False},
            }
            return users.get(user_id, {"name": "Unknown", "age": 0, "active": False})

        async def calculate_discount(age):
            await asyncio.sleep(0.01)
            if age >= 60:
                return 0.3  # 30% desconto para idosos
            elif age >= 18:
                return 0.1  # 10% desconto para adultos
            else:
                return 0.0  # Sem desconto para menores

        functions = {
            "fetch_user": fetch_user,
            "calculate_discount": calculate_discount
        }

        data = {"user_id": 1}

        # Busca usuário e calcula desconto baseado na idade
        user_rule = {"apply": ["fetch_user", {"var": "user_id"}]}
        user = await jsonLogicAsync(user_rule, data, functions)

        discount_rule = {"apply": ["calculate_discount", user["age"]]}
        discount = await jsonLogicAsync(discount_rule, {}, functions)

        # Verifica se usuário está ativo e tem desconto
        complex_rule = {
            "and": [
                user["active"],
                {">": [discount, 0]}
            ]
        }

        result = await jsonLogicAsync(complex_rule, {}, functions)
        assert result is True  # João está ativo e tem desconto

    def test_json_logic_auto_sync_only(self):
        """Testa jsonLogicAuto com apenas funções síncronas."""
        functions = {
            "add": lambda a, b: a + b,
            "multiply": lambda a, b: a * b,
        }

        data = {"x": 5, "y": 3}
        rule = {"apply": ["add", {"var": "x"}, {"var": "y"}]}

        result = jsonLogicAuto(rule, data, functions)
        
        # Deve retornar resultado diretamente (não uma corrotina)
        assert not asyncio.iscoroutine(result)
        assert result == 8

    def test_json_logic_auto_with_async(self):
        """Testa jsonLogicAuto com funções assíncronas."""
        async def multiply_async(a, b):
            await asyncio.sleep(0.01)
            return a * b

        functions = {
            "add": lambda a, b: a + b,
            "multiply_async": multiply_async,
        }

        data = {"x": 5, "y": 3}
        rule = {"apply": ["add", {"var": "x"}, {"var": "y"}]}

        result = jsonLogicAuto(rule, data, functions)
        
        # Deve retornar uma corrotina porque há funções assíncronas registradas
        assert asyncio.iscoroutine(result)
        
        # Descarta a corrotina para evitar warning do pytest
        result.close()

    @pytest.mark.asyncio
    async def test_nested_async_operations(self):
        """Testa operações assíncronas aninhadas."""
        async def double_async(x):
            await asyncio.sleep(0.01)
            return x * 2

        async def add_async(a, b):
            await asyncio.sleep(0.01)
            return a + b

        functions = {
            "double": double_async,
            "add": add_async
        }

        data = {"x": 5, "y": 3}

        # Regra aninhada: add(double(x), double(y))
        rule = {
            "apply": [
                "add",
                {"apply": ["double", {"var": "x"}]},
                {"apply": ["double", {"var": "y"}]}
            ]
        }

        result = await jsonLogicAsync(rule, data, functions)
        assert result == 16  # double(5) + double(3) = 10 + 6 = 16

    @pytest.mark.asyncio
    async def test_async_function_error_handling(self):
        """Testa tratamento de erros em funções assíncronas."""
        async def failing_function():
            await asyncio.sleep(0.01)
            raise ValueError("Erro simulado")

        functions = {"fail": failing_function}

        rule = {"apply": ["fail"]}

        with pytest.raises(ValueError, match="Erro simulado"):
            await jsonLogicAsync(rule, {}, functions)

    @pytest.mark.asyncio
    async def test_async_with_logical_operations(self):
        """Testa funções assíncronas com operações lógicas."""
        async def is_even_async(x):
            await asyncio.sleep(0.01)
            return x % 2 == 0

        async def is_positive_async(x):
            await asyncio.sleep(0.01)
            return x > 0

        functions = {
            "is_even": is_even_async,
            "is_positive": is_positive_async
        }

        data = {"number": 4}

        # Verifica se é par E positivo
        rule = {
            "and": [
                {"apply": ["is_even", {"var": "number"}]},
                {"apply": ["is_positive", {"var": "number"}]}
            ]
        }

        result = await jsonLogicAsync(rule, data, functions)
        assert result is True

        # Testa com número negativo
        data["number"] = -4
        result = await jsonLogicAsync(rule, data, functions)
        assert result is False  # É par mas não é positivo

    @pytest.mark.asyncio
    async def test_async_with_conditional_operations(self):
        """Testa funções assíncronas com operações condicionais."""
        async def get_grade_async(score):
            await asyncio.sleep(0.01)
            if score >= 90:
                return "A"
            elif score >= 80:
                return "B"
            elif score >= 70:
                return "C"
            else:
                return "F"

        functions = {"get_grade": get_grade_async}

        data = {"score": 85}

        # Usa operador ternário com função assíncrona
        rule = {
            "?:": [
                {">": [{"var": "score"}, 70]},
                {"apply": ["get_grade", {"var": "score"}]},
                "Failed"
            ]
        }

        result = await jsonLogicAsync(rule, data, functions)
        assert result == "B"

    @pytest.mark.asyncio
    async def test_json_logic_auto_execution_with_async(self):
        """Testa execução completa do jsonLogicAuto com funções assíncronas."""
        async def multiply_async(a, b):
            await asyncio.sleep(0.01)
            return a * b

        functions = {
            "add": lambda a, b: a + b,
            "multiply_async": multiply_async,
        }

        data = {"x": 5, "y": 3}
        rule = {"apply": ["add", {"var": "x"}, {"var": "y"}]}

        result = jsonLogicAuto(rule, data, functions)
        
        # Se retornou uma corrotina, deve ser executada
        if asyncio.iscoroutine(result):
            final_result = await result
            assert final_result == 8
        else:
            assert result == 8


if __name__ == "__main__":
    # Para executar os testes manualmente
    pytest.main([__file__, "-v"])
