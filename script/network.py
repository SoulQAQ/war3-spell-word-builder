#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
网络请求封装模块
提供统一的 HTTP 请求接口
"""

import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Union

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError as exc:
    raise RuntimeError("缺少 requests 依赖，请先执行: pip install requests") from exc


@dataclass
class HttpResponse:
    """
    统一响应数据结构
    
    Attributes:
        success: 请求是否成功
        status_code: HTTP 状态码
        data: 响应数据（JSON 解析后的对象）
        text: 响应文本
        message: 响应消息或错误信息
        headers: 响应头
        elapsed_ms: 请求耗时（毫秒）
    """
    success: bool
    status_code: int
    data: Any = None
    text: str = ""
    message: str = ""
    headers: Dict[str, str] = field(default_factory=dict)
    elapsed_ms: float = 0.0


class HttpClient:
    """HTTP 客户端封装类"""

    def __init__(
        self,
        base_url: str = "",
        timeout: int = 30,
        retry_count: int = 2,
        headers: Optional[Dict[str, str]] = None
    ):
        """
        初始化 HTTP 客户端
        
        Args:
            base_url: 基础 URL
            timeout: 请求超时时间（秒）
            retry_count: 重试次数
            headers: 默认请求头
        """
        self.base_url = base_url.rstrip('/') if base_url else ""
        self.timeout = timeout
        self.default_headers = headers or {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        # 创建带重试机制的 session
        self.session = requests.Session()
        retry_strategy = Retry(
            total=retry_count,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _build_url(self, endpoint: str) -> str:
        """
        构建完整 URL
        
        Args:
            endpoint: 接口路径
            
        Returns:
            str: 完整 URL
        """
        if endpoint.startswith('http://') or endpoint.startswith('https://'):
            return endpoint
        if self.base_url:
            return f"{self.base_url}/{endpoint.lstrip('/')}"
        return endpoint

    def _handle_response(self, response: requests.Response, elapsed_ms: float) -> HttpResponse:
        """
        处理响应
        
        Args:
            response: requests 响应对象
            elapsed_ms: 请求耗时（毫秒）
            
        Returns:
            HttpResponse: 统一响应对象
        """
        try:
            data = response.json()
        except (json.JSONDecodeError, ValueError):
            data = None

        return HttpResponse(
            success=response.ok,
            status_code=response.status_code,
            data=data,
            text=response.text,
            message=response.reason or "",
            headers=dict(response.headers),
            elapsed_ms=elapsed_ms
        )

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str, bytes]] = None,
        timeout: Optional[int] = None
    ) -> HttpResponse:
        """
        发送 HTTP 请求
        
        Args:
            method: 请求方法 (GET, POST, PUT, DELETE)
            url: 请求 URL
            headers: 请求头
            params: 查询参数
            json_data: JSON 请求体
            data: 表单数据或原始数据
            timeout: 超时时间
            
        Returns:
            HttpResponse: 统一响应对象
        """
        full_url = self._build_url(url)
        request_headers = {**self.default_headers, **(headers or {})}
        request_timeout = timeout or self.timeout

        start_time = time.time()
        
        try:
            response = self.session.request(
                method=method.upper(),
                url=full_url,
                headers=request_headers,
                params=params,
                json=json_data,
                data=data,
                timeout=request_timeout
            )
            elapsed_ms = (time.time() - start_time) * 1000
            return self._handle_response(response, elapsed_ms)
            
        except requests.Timeout:
            elapsed_ms = (time.time() - start_time) * 1000
            return HttpResponse(
                success=False,
                status_code=0,
                data=None,
                text="",
                message="Request timeout",
                headers={},
                elapsed_ms=elapsed_ms
            )
        except requests.ConnectionError as e:
            elapsed_ms = (time.time() - start_time) * 1000
            return HttpResponse(
                success=False,
                status_code=0,
                data=None,
                text="",
                message=f"Connection error: {str(e)}",
                headers={},
                elapsed_ms=elapsed_ms
            )
        except requests.RequestException as e:
            elapsed_ms = (time.time() - start_time) * 1000
            return HttpResponse(
                success=False,
                status_code=0,
                data=None,
                text="",
                message=f"Request failed: {str(e)}",
                headers={},
                elapsed_ms=elapsed_ms
            )

    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> HttpResponse:
        """
        发送 GET 请求
        
        Args:
            url: 请求 URL
            params: 查询参数
            headers: 请求头
            timeout: 超时时间
            
        Returns:
            HttpResponse: 统一响应对象
        """
        return self.request('GET', url, headers=headers, params=params, timeout=timeout)

    def post(
        self,
        url: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str, bytes]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> HttpResponse:
        """
        发送 POST 请求
        
        Args:
            url: 请求 URL
            json_data: JSON 请求体
            data: 表单数据或原始数据
            headers: 请求头
            timeout: 超时时间
            
        Returns:
            HttpResponse: 统一响应对象
        """
        return self.request('POST', url, headers=headers, json_data=json_data, data=data, timeout=timeout)

    def put(
        self,
        url: str,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str, bytes]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> HttpResponse:
        """
        发送 PUT 请求
        
        Args:
            url: 请求 URL
            json_data: JSON 请求体
            data: 表单数据或原始数据
            headers: 请求头
            timeout: 超时时间
            
        Returns:
            HttpResponse: 统一响应对象
        """
        return self.request('PUT', url, headers=headers, json_data=json_data, data=data, timeout=timeout)

    def delete(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> HttpResponse:
        """
        发送 DELETE 请求
        
        Args:
            url: 请求 URL
            headers: 请求头
            timeout: 超时时间
            
        Returns:
            HttpResponse: 统一响应对象
        """
        return self.request('DELETE', url, headers=headers, timeout=timeout)

    def download(
        self,
        url: str,
        save_path: str,
        chunk_size: int = 8192,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> HttpResponse:
        """
        下载文件
        
        Args:
            url: 文件 URL
            save_path: 保存路径
            chunk_size: 分块大小
            headers: 请求头
            timeout: 超时时间
            
        Returns:
            HttpResponse: 统一响应对象
        """
        full_url = self._build_url(url)
        request_headers = {**self.default_headers, **(headers or {})}
        request_timeout = timeout or self.timeout

        start_time = time.time()
        
        try:
            response = self.session.get(
                full_url,
                headers=request_headers,
                timeout=request_timeout,
                stream=True
            )

            if not response.ok:
                elapsed_ms = (time.time() - start_time) * 1000
                return self._handle_response(response, elapsed_ms)

            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    f.write(chunk)

            elapsed_ms = (time.time() - start_time) * 1000
            return HttpResponse(
                success=True,
                status_code=response.status_code,
                data=save_path,
                text="",
                message="Download successful",
                headers=dict(response.headers),
                elapsed_ms=elapsed_ms
            )
            
        except requests.RequestException as e:
            elapsed_ms = (time.time() - start_time) * 1000
            return HttpResponse(
                success=False,
                status_code=0,
                data=None,
                text="",
                message=f"Download failed: {str(e)}",
                headers={},
                elapsed_ms=elapsed_ms
            )

    def close(self) -> None:
        """关闭会话"""
        self.session.close()

    def __enter__(self) -> 'HttpClient':
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """上下文管理器出口"""
        self.close()


# 全局 HTTP 客户端实例
_http_client: Optional[HttpClient] = None


def get_http_client(base_url: str = "", **kwargs) -> HttpClient:
    """
    获取或创建 HTTP 客户端实例
    
    Args:
        base_url: 基础 URL
        **kwargs: 其他参数传递给 HttpClient 构造函数
        
    Returns:
        HttpClient: HTTP 客户端实例
    """
    global _http_client
    if _http_client is None or base_url:
        _http_client = HttpClient(base_url=base_url, **kwargs)
    return _http_client


def create_http_client(**kwargs) -> HttpClient:
    """
    创建新的 HTTP 客户端实例
    
    Args:
        **kwargs: 参数传递给 HttpClient 构造函数
        
    Returns:
        HttpClient: 新的 HTTP 客户端实例
    """
    return HttpClient(**kwargs)