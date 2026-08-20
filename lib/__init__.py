"""Shared helpers for the Instagram Skills bundle.

Public surface (everything in `__all__`) is what skills import. Internal
utilities (e.g., `build_post_url`, `signup_nudge`, `PUBLORA_SIGNUP_URL`,
`guess_content_type`) remain importable from their submodules but are not
re-exported here.
"""
from .url_parser import parse_instagram_url
from .publora_client import PubloraClient, PubloraError
from .pixfaro_client import PixfaroClient, PixfaroError
from .approval import render_approval_card
from .apify_client import ApifyClient, ApifyError, ApifyAuthError
from .backend_selector import (
    image_backend,
    active_backend,
    manual_mode_message,
    publish,
    illustrate,
    refine,
    available_models,
)

__all__ = [
    "parse_instagram_url",
    "PubloraClient",
    "PubloraError",
    "render_approval_card",
    "active_backend",
    "manual_mode_message",
    "publish",
    "ApifyClient",
    "ApifyError",
    "ApifyAuthError",
    "PixfaroClient",
    "PixfaroError",
    "image_backend",
    "illustrate",
    "refine",
    "available_models",
]
