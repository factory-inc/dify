from typing import Any

from core.tools.errors import ToolProviderCredentialValidationError
from core.tools.provider.builtin.google_custom_search.tools.google_custom_search import GoogleCustomSearchTool
from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController


class GoogleCustomSearchProvider(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            GoogleCustomSearchTool().fork_tool_runtime(
                runtime={
                    "credentials": credentials,
                }
            ).invoke(
                user_id='',
                tool_parameters={
                    "query": "test",
                    "num_results": 1
                },
            )
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
