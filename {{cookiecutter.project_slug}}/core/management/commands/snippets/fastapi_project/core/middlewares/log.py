import json
import time
import uuid
from collections.abc import Callable

from core.config import settings
from fastapi import Request, Response
from rich.console import Console
from starlette.concurrency import iterate_in_threadpool


class CustomLog(object):
    def __init__(
        self,
        log_id: str,
        autorization: str,
        content_type: str,
        content_length: str,
        content_accept: str,
        request_method: str,
        request_path: str,
        execute_time: int,
        status_code: str,
        body: str = None,
    ) -> None:
        self.status_code = status_code
        self.logger_id = log_id
        self.autorization = autorization
        self.content_type = content_type
        self.content_length = content_length
        self.content_accept = content_accept
        self.request_method = request_method
        self.request_path = request_path
        self.execute_time = execute_time
        self.body = body
        self.color = "green"
        self._errors_status_code = ["4", "5"]
        self._warnings_status_code = [
            "3",
        ]

    def show_log(self) -> None:
        if str(self.status_code)[0] in self._errors_status_code:
            self.color = "red"
            self._log(title="Error")

        elif str(self.status_code)[0] in self._warnings_status_code:
            self.color = "yellow"
            self._log(title="Warning")

        else:
            self._log(title="Success")

    def _create_line_message(self, message: str) -> str:
        return f"[white]{message}[/]"

    def _log(self, title: str) -> None:
        _console = Console()
        _status_code = f"Status Code: {self.status_code}"
        _request_time = f"Hora da requisição: {time.strftime('%H:%M:%S')}"
        _logger_id = f"Logger: {self.logger_id}"
        _method = f"Method: {self.request_method}"
        _path = f"Path: {self.request_path}"
        _token = f"Token: {self.autorization}"
        _time = f"Tempo: {self.execute_time} milisegundos"
        _content_type = f"Content-Type: {self.content_type}"
        _content_length = f"Content-Length: {self.content_length}"
        _content_accept = f"Accept: {self.content_accept}"
        _console.print()
        _console.rule(
            f"[{self.color}] {_logger_id} > {title} | {_status_code} | {_time}[/] ",
            style=f"{self.color}",
        )
        _console.print(self._create_line_message(_request_time))
        _console.print(self._create_line_message(_method))
        _console.print(self._create_line_message(_content_type))
        _console.print(self._create_line_message(_content_length))
        _console.print(self._create_line_message(_content_accept))
        _console.print(self._create_line_message(_path))
        _console.print(self._create_line_message(_token))
        _console.print("BODY:")
        _console.print(self.body)
        _console.print()
        _console.rule(
            f"[{self.color}]{self.execute_time} miliseconds[/]", style=f"{self.color}"
        )
        _console.print()
        _console.print()


async def log_middleware(request: Request, call_next: Callable) -> Response:
    if settings.debug == "false":
        return await call_next(request)

    try:
        _log_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        _authorization = request.headers.get("Authorization", None)
        _content_type = request.headers.get("Content-Type", None)
        _content_length = request.headers.get("Content-Length", None)
        _content_accept = request.headers.get("Accept", None)
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        response_body = [section async for section in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        _response_body = json.loads(b"".join(response_body))

        CustomLog(
            log_id=_log_id,
            autorization=_authorization,
            content_type=_content_type,
            content_length=_content_length,
            content_accept=_content_accept,
            request_method=request.method,
            request_path=request.url.path,
            execute_time=round(process_time, 3),
            body=_response_body,
            status_code=response.status_code,
        ).show_log()

        return response

    except Exception:
        print(f"Error no middleware: {Exception}")
        return await call_next(request)
