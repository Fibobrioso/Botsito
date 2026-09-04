import pytest

from botsito.yaml_estricto import YamlError, cargar_yaml


def test_clave_duplicada_es_error() -> None:
    with pytest.raises(YamlError, match="clave duplicada 'valor' en la linea 3"):
        cargar_yaml("a: 1\nvalor: '0.75'\nvalor: '0.80'\n")
    with pytest.raises(YamlError, match="clave duplicada"):
        cargar_yaml("x:\n  - {a: 1, a: 2}\n")


def test_fechas_quedan_como_texto() -> None:
    doc = cargar_yaml("fecha: 2026-09-20\ncuando: 2026-09-20 10:00:00\n")
    assert doc == {"fecha": "2026-09-20", "cuando": "2026-09-20 10:00:00"}


def test_resto_de_tipos_como_pyyaml() -> None:
    doc = cargar_yaml("n: 3\nt: 1:05:00\nb: yes\ns: '07:00'\nv: null\n")
    assert doc == {"n": 3, "t": 3900, "b": True, "s": "07:00", "v": None}


def test_yaml_roto() -> None:
    with pytest.raises(YamlError, match="YAML invalido"):
        cargar_yaml("a: [1,\n")


def test_clave_no_hashable_es_yaml_error() -> None:
    with pytest.raises(YamlError, match="clave no admitida"):
        cargar_yaml("? [1, 2]\n: x\n")
