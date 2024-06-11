# Copyright (C) 2024 Jack Green (jackgreen.co)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import gzip
import secrets
import struct
from typing import Callable, Self

import zstandard as zstd
from flask import Flask, Response, request
from redis.client import StrictRedis

import minify_html

MAX_PADDING_SIZE = 512


class Minify(object):
    def __init__(self: Self):
        pass

    def apply_minify_html(self: Self, html: str, path: str) -> str:
        key = f"cache:{hash(path)}"

        if self.use_cache and self.redis.exists(key):
            return self.redis.get(key)

        data = minify_html.minify(html)
        self.redis.set(key, data)

        return data

    def create_gzip_with_padding(self: Self, data: bytes, padding_size: int) -> bytes:
        padding = secrets.token_bytes(padding_size)

        header = (
            b"\x1f\x8b\x08\x04"
            + (0).to_bytes(4, byteorder="little")
            + b"\x00"
            + b"\xff"
            + (padding_size + 2).to_bytes(2, byteorder="little")
            + b"\x00\x00"
        )

        compressed_data = gzip.compress(data)[10:]

        return header + padding + compressed_data

    def create_zstd_with_padding(self: Self, data: bytes, padding_size: int) -> bytes:
        padding = secrets.token_bytes(padding_size)

        compressed_data = zstd.compress(data)

        frame_id = 0x184D2A50
        frame_size = len(padding)

        header = struct.pack("<I", frame_id) + struct.pack("<I", frame_size)
        skippable_frame = header + padding

        return skippable_frame + compressed_data

    def select_compression_algorithm(self: Self, accepted_encodings: str) -> Callable:
        accepted_encodings = [encoding.strip() for encoding in accepted_encodings.lower().split(",")]
        accepted_encodings = sorted(
            accepted_encodings,
            key=lambda encoding: float(encoding.split(";q=")[1]) if ";q=" in encoding else 1.0,
            reverse=True,
        )

        for encoding in accepted_encodings:
            if encoding == "identity":
                return lambda response: response
            if encoding == "*":
                return self.gzip_response
            if encoding == "gzip":
                return self.gzip_response
            if encoding == "zstd":
                return self.zstd_response

        return lambda response: response

    def gzip_response(self: Self, response: Response) -> Response:
        padding_size = secrets.randbelow(MAX_PADDING_SIZE + 1)

        data = self.create_gzip_with_padding(response.data, padding_size)
        response.set_data(data)
        response.headers["Content-Encoding"] = "gzip"
        response.headers["Content-Length"] = len(response.data)
        return response

    def zstd_response(self: Self, response: Response) -> Response:
        padding_size = secrets.randbelow(MAX_PADDING_SIZE + 1)

        data = self.create_zstd_with_padding(response.data, padding_size)
        response.set_data(data)
        response.headers["Content-Encoding"] = "zstd"
        response.headers["Content-Length"] = len(response.data)
        return response

    def after_request_minify(self: Self, response: Response) -> Response:
        response.direct_passthrough = False
        if response.content_type.startswith("text/html") and request.method == "GET":
            data = self.apply_minify_html(response.get_data(as_text=True), request.path)
            response.set_data(data)
        return response

    def after_request_compress(self: Self, response: Response) -> Response:
        alg = self.select_compression_algorithm(request.headers.get("Accept-Encoding", ""))
        return alg(response)

    def init_app(self: Self, app: Flask, redis: StrictRedis):
        self.redis = redis
        self.use_cache = app.config.get("MINIFY_USE_CACHE", False)

        with app.app_context():
            app.after_request(self.after_request_compress)
            app.after_request(self.after_request_minify)


minify = Minify()
