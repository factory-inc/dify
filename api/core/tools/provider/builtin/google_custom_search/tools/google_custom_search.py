import json
from typing import Any, Union

from googleapiclient.discovery import build

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool


class CustomSearchAPI:
    """
    Google Custom Search tool provider.
    """
    api_key: str = None
    engine_id: str = None

    def __init__(self, api_key: str, engine_id: str) -> None:
        """Google Custom Search tool provider."""
        self.api_key = api_key
        self.engine_id = engine_id
        self.service = build("customsearch", "v1", developerKey=self.api_key)

    def run(self, query: str, **kwargs: Any) -> str:
        num_results = kwargs.get("num_results", 10)

        response = self.service.cse().list(
            q=query,
            num=num_results,
            cx=self.engine_id,
            lr='lang_ja',
        ).execute()

        result = []
        for item in response['items']:
            result.append({
                "title": item.get('title', ''),
                "snippet": item.get('snippet', ''),
                "url": item.get('link', '')
            })
                
        return json.dumps({
            "search_provider": "Google Custom Search",
            "query": query,
            "results": result,
        }, ensure_ascii=False)


class GoogleCustomSearchTool(BuiltinTool):
    def _invoke(self, 
                user_id: str,
               tool_parameters: dict[str, Any], 
        ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
            invoke tools
        """
        query = tool_parameters['query']
        num_results = tool_parameters.get('num_results', 10)
        api_key = self.runtime.credentials['google_custom_search_api_key']
        engine_id = self.runtime.credentials['google_custom_search_engine_id']
        result = CustomSearchAPI(api_key, engine_id).run(query, num_results=num_results)
        return self.create_text_message(text=result)