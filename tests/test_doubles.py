from tests.doubles import StubSemDesconto
from src.desconto import Pedido

def test_pedido_com_stub():
    pedido = Pedido(StubSemDesconto())
    assert pedido.total(100) == 100