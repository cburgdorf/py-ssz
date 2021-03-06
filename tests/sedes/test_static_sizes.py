import pytest

from ssz.sedes import (
    ByteVector,
    Container,
    List,
    Vector,
    boolean,
    byte,
    byte_list,
    bytes32,
    bytes48,
    bytes96,
    uint8,
    uint256,
)


@pytest.mark.parametrize(
    ("sedes", "size"),
    (
        (boolean, 1),
        (uint8, 1),
        (uint256, 32),
        (Vector(uint8, 0), 0),
        (Vector(uint8, 2), 2),
        (Container((("a", uint8), ("b", Vector(uint8, 4)))), 5),
        (Vector(List(uint8), 0), 0),
        (Vector(Container((("a", uint8), ("b", Vector(uint8, 4)))), 4), 20),
        (byte, 1),
        (ByteVector(0), 0),
        (bytes32, 32),
        (bytes48, 48),
        (bytes96, 96),
    ),
)
def test_static_size(sedes, size):
    assert sedes.is_static_sized
    assert sedes.get_static_size() == size


@pytest.mark.parametrize(
    "sedes",
    (
        List(uint8),
        List(Vector(uint8, 2)),
        List(List(uint8)),
        List(Container((("a", uint8), ("b", Vector(uint8, 4))))),
        Vector(List(uint8), 2),
        Container((("a", List(uint8)),)),
        Container((("a", uint8), ("b", List(uint8)), ("c", uint8))),
        Container((("a", Container((("a", List(uint8)),))),)),
        byte_list,
    ),
)
def test_dynamic_size(sedes):
    assert not sedes.is_static_sized
    with pytest.raises(ValueError):
        sedes.get_static_size()
