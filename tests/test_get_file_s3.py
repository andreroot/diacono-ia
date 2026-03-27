import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from diacono_categ import get_file_s3


class LoadJsonConfigTests(unittest.TestCase):
    def test_uses_local_resource_when_s3_is_disabled(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            resource_dir = Path(temp_dir) / "resource"
            resource_dir.mkdir()
            payload = {"tipo_custo": ["mercado"]}
            (resource_dir / "lista_categorias.json").write_text(
                json.dumps(payload),
                encoding="utf-8",
            )

            with patch.object(get_file_s3, "DEFAULT_LOCAL_RESOURCE_DIR", resource_dir):
                with patch.dict("os.environ", {"DIACONO_CONFIG_SOURCE": "local"}, clear=False):
                    data = get_file_s3.load_json_config("lista_categorias.json")

            self.assertEqual(data, payload)

    def test_uses_cache_when_s3_download_succeeds(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_dir = Path(temp_dir) / "cache"
            payload = {"FDI Fernao D": "gasolina"}

            def fake_download(filename: str) -> Path:
                destination = cache_dir / filename
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(json.dumps(payload), encoding="utf-8")
                return destination

            with patch.object(get_file_s3, "_download_from_s3", side_effect=fake_download):
                with patch.dict(
                    "os.environ",
                    {
                        "DIACONO_CONFIG_SOURCE": "s3",
                        "DIACONO_S3_BUCKET": "fake-bucket",
                    },
                    clear=False,
                ):
                    data = get_file_s3.load_json_config("regras_categorias.json")

            self.assertEqual(data, payload)

    def test_falls_back_to_local_if_s3_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            resource_dir = Path(temp_dir) / "resource"
            resource_dir.mkdir()
            payload = {"tipo_custo": ["farmacia"]}
            (resource_dir / "lista_categorias.json").write_text(
                json.dumps(payload),
                encoding="utf-8",
            )

            with patch.object(get_file_s3, "DEFAULT_LOCAL_RESOURCE_DIR", resource_dir):
                with patch.object(
                    get_file_s3,
                    "_download_from_s3",
                    side_effect=RuntimeError("s3 indisponivel"),
                ):
                    with patch.dict(
                        "os.environ",
                        {
                            "DIACONO_CONFIG_SOURCE": "auto",
                            "DIACONO_S3_BUCKET": "fake-bucket",
                        },
                        clear=False,
                    ):
                        data = get_file_s3.load_json_config("lista_categorias.json")

            self.assertEqual(data, payload)


if __name__ == "__main__":
    unittest.main()