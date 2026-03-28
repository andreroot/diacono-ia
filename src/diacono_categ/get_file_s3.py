from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


DEFAULT_CACHE_DIR = Path.home() / ".cache" / "diacono-ia"
DEFAULT_LOCAL_RESOURCE_DIR = Path(__file__).resolve().parent / "resource"


def _config_source() -> str:
	return os.getenv("DIACONO_CONFIG_SOURCE", "auto").strip().lower()


def _cache_dir() -> Path:
	custom_dir = os.getenv("DIACONO_CONFIG_CACHE_DIR")
	return Path(custom_dir).expanduser() if custom_dir else DEFAULT_CACHE_DIR


def _local_resource_path(filename: str) -> Path:
	print(DEFAULT_LOCAL_RESOURCE_DIR)
	return DEFAULT_LOCAL_RESOURCE_DIR / filename


def _cache_file_path(filename: str) -> Path:
	return _cache_dir() / filename


def _should_use_s3() -> bool:
	source = _config_source()
	if source == "s3":
		return True
	if source == "local":
		return False
	return bool(os.getenv("DIACONO_S3_BUCKET"))


def _build_s3_key(filename: str) -> str:
	prefix = os.getenv("DIACONO_S3_PREFIX", "").strip("/")
	return f"{prefix}/{filename}" if prefix else filename


def _download_from_s3(filename: str) -> Path:
	import boto3
	
	bucket = os.getenv("DIACONO_S3_BUCKET")
	if not bucket:
		raise RuntimeError("Defina DIACONO_S3_BUCKET para carregar configuracoes do S3.")

	# try:
    #     pass
	# except ImportError as exc:
	# 	raise RuntimeError(
	# 		"Dependencia boto3 nao encontrada. Instale o pacote com suporte ao S3."
	# 	) from exc

	destination = _cache_file_path(filename)
	destination.parent.mkdir(parents=True, exist_ok=True)

	client_kwargs: dict[str, Any] = {}
	region_name = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
	endpoint_url = os.getenv("AWS_ENDPOINT_URL")
	if region_name:
		client_kwargs["region_name"] = region_name
	if endpoint_url:
		client_kwargs["endpoint_url"] = endpoint_url

	boto3.client("s3", **client_kwargs).download_file(
		bucket,
		_build_s3_key(filename),
		str(destination),
	)
	return destination


def get_config_file_path(filename: str) -> Path:
	local_path = _local_resource_path(filename)
	source = _config_source()

	if _should_use_s3():
		try:
			return _download_from_s3(filename)
		except Exception:
			if source == "s3":
				raise
			if local_path.exists():
				return local_path
			
			cache_path = _cache_file_path(filename)
			if cache_path.exists():
				return cache_path
			raise

	if local_path.exists():
		return local_path

	cache_path = _cache_file_path(filename)
	if cache_path.exists():
		return cache_path

	raise FileNotFoundError(
		f"Arquivo de configuracao nao encontrado: {filename}. "
		"Inclua o recurso no pacote ou configure o S3."
	)


def load_json_config(filename: str) -> dict[str, Any]:
	config_path = get_config_file_path(filename)
	print(f"Carregando configuracao de: {config_path}")
	with config_path.open("r", encoding="utf-8") as file_obj:
		return json.load(file_obj)
