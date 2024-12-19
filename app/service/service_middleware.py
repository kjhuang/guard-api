"""
service middleware
"""

from typing import Any, Callable


async def service_middleware(service: Any, method_name: str, *args, **kwargs):
    """
    Middleware to dynamically execute pre- and post-hooks for a service method.
    """
    method: Callable = getattr(service, method_name)

    # Execute the pre-hook if defined
    if hasattr(service, f"pre_{method_name}_hook"):
        pre_hook = getattr(service, f"pre_{method_name}_hook")
        await pre_hook(*args, **kwargs)

    # Execute the main method
    result = await method(*args, **kwargs)

    # Execute the post-hook if defined
    if hasattr(service, f"post_{method_name}_hook"):
        post_hook = getattr(service, f"post_{method_name}_hook")
        await post_hook(result)

    return result
