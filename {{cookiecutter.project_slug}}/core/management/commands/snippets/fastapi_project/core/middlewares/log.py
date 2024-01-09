import json
import time
import uuid
from collections.abc import Callable
from string import Template

from fastapi import FastAPI, Request, Response
from rich.console import Console
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware

LOG_TEMPLATE = Template(
    """
    Logger: $logger_id
    Hora da requisição: $request_time
    Tempo de execução: $time

    Status Code: $status_code
    Method: $method
    Content-Type: $content_type
    Content-Length: $content_length
    Accept: $content_accept
    Path: $path
    Token: $token
    
    Body:
    $body
    """
)


class LogObject:
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
        body: str,
    ):
        self.logger_id = log_id
        self.autorization = autorization
        self.content_type = content_type
        self.content_length = content_length
        self.content_accept = content_accept
        self.request_method = request_method
        self.request_path = request_path
        self.execute_time = execute_time
        self.status_code = status_code
        self.body = body
        self.color = "green"
        self._errors_status_code = ["4", "5"]
        self._warnings_status_code = ["3"]

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
        _request_time = time.strftime("%H:%M:%S")
        _console.print()
        _console.rule(
            f"[{self.color}] {self.logger_id} - {title} | {self.status_code} | {self.execute_time} ms[/] ",
            style=f"{self.color}",
        )

        _console.print(
            LOG_TEMPLATE.substitute(
                status_code=self.status_code,
                request_time=_request_time,
                logger_id=self.logger_id,
                method=self.request_method,
                path=self.request_path,
                token=self.autorization,
                time=f"{self.execute_time} ms",
                content_type=self.content_type,
                content_length=self.content_length,
                content_accept=self.content_accept,
                body=json.dumps(self.body, indent=4, sort_keys=True),
            )
        )

        _console.print()
        _console.rule(f"[{self.color}]{self.execute_time} ms[/]", style=f"{self.color}")
        _console.print()


class CustomLog(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
    ) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            start_time = time.time()
            response = await call_next(request)
            response_body = [section async for section in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))

            LogObject(
                log_id=request.headers.get("X-Request-ID", str(uuid.uuid4())),
                autorization=request.headers.get("Authorization", None),
                content_type=request.headers.get("Content-Type", None),
                content_length=request.headers.get("Content-Length", None),
                content_accept=request.headers.get("Accept", None),
                request_method=request.method,
                request_path=request.url.path,
                execute_time=round((time.time() - start_time) * 1000, 3),
                body=json.loads(b"".join(response_body)),
                status_code=response.status_code,
            ).show_log()

            return response

        except Exception:
            print(f"Error no middleware: {Exception}")
            return await call_next(request)
