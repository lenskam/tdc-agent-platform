import os
import json
import logging
from typing import List, Optional, Dict, Any
from langchain_core.tools import tool
import requests

logger = logging.getLogger(__name__)

DHIS2_BASE_URL = os.getenv("DHIS2_BASE_URL", "")
DHIS2_USERNAME = os.getenv("DHIS2_USERNAME", "")
DHIS2_PASSWORD = os.getenv("DHIS2_PASSWORD", "")


class DHIS2Tools:
    @tool("fetch_dhis2_analytics")
    def fetch_dhis2_analytics(
        indicators: str,
        period: str,
        org_unit: str,
        dimensions: Optional[str] = None
    ) -> str:
        """
        Fetches analytics data from DHIS2.

        Args:
            indicators: Comma-separated indicator UIDs or codes (e.g., "ANC4Coverage,DeliveryBySkilled")
            period: Period in format YYYY or YYYYMM (e.g., "2023", "202301")
            org_unit: Organisation Unit UID or code (e.g., "ImspTQPwCqd")
            dimensions: Optional additional dimensions (e.g., "category:sex")

        Returns:
            JSON string with analytics data or error message
        """
        if not DHIS2_BASE_URL or not DHIS2_USERNAME or not DHIS2_PASSWORD:
            return json.dumps({
                "success": False,
                "error": "DHIS2 credentials not configured. Set DHIS2_BASE_URL, DHIS2_USERNAME, DHIS2_PASSWORD in .env"
            })

        try:
            url = f"{DHIS2_BASE_URL}/api/analytics"
            
            params = {
                "ds": indicators,
                "pe": period,
                "ou": org_unit,
                "format": "json",
                "skipMeta": "true"
            }
            
            if dimensions:
                params["dimension"] = dimensions

            response = requests.get(
                url,
                params=params,
                auth=(DHIS2_USERNAME, DHIS2_PASSWORD),
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                
                headers = data.get("headers", [])
                rows = data.get("rows", [])
                
                result = {
                    "success": True,
                    "period": period,
                    "org_unit": org_unit,
                    "indicators": indicators,
                    "headers": [h.get("name") for h in headers],
                    "row_count": len(rows),
                    "data": rows[:100]
                }
                
                return json.dumps(result)
            else:
                return json.dumps({
                    "success": False,
                    "error": f"DHIS2 API error: {response.status_code}",
                    "details": response.text
                })

        except requests.exceptions.RequestException as e:
            logger.error(f"DHIS2 request failed: {e}")
            return json.dumps({
                "success": False,
                "error": str(e)
            })

    @tool("get_dhis2_metadata")
    def get_dhis2_metadata(
        type: str,
        query: Optional[str] = None,
        page_size: int = 50
    ) -> str:
        """
        Fetches metadata from DHIS2.

        Args:
            type: Type of metadata - "indicators", "dataElements", "orgUnits", "categories"
            query: Optional search query for filtering
            page_size: Number of results to return (default: 50)

        Returns:
            JSON string with metadata or error message
        """
        if not DHIS2_BASE_URL or not DHIS2_USERNAME or not DHIS2_PASSWORD:
            return json.dumps({
                "success": False,
                "error": "DHIS2 credentials not configured"
            })

        valid_types = ["indicators", "dataElements", "organisationUnits", "categories", "categoryOptionCombos"]
        if type not in valid_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid type. Must be one of: {valid_types}"
            })

        try:
            endpoint_map = {
                "indicators": "indicators",
                "dataElements": "dataElements",
                "orgUnits": "organisationUnits",
                "categories": "categories",
                "categoryOptionCombos": "categoryOptionCombos"
            }
            
            url = f"{DHIS2_BASE_URL}/api/{endpoint_map[type]}"
            
            params = {
                "pageSize": page_size,
                "fields": "id,name,code,description"
            }
            
            if query:
                params["filter"] = f"name:ilike:{query}"

            response = requests.get(
                url,
                params=params,
                auth=(DHIS2_USERNAME, DHIS2_PASSWORD),
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                items = data.get(type, [])
                
                result = {
                    "success": True,
                    "type": type,
                    "count": len(items),
                    "items": items
                }
                
                return json.dumps(result)
            else:
                return json.dumps({
                    "success": False,
                    "error": f"DHIS2 API error: {response.status_code}",
                    "details": response.text
                })

        except requests.exceptions.RequestException as e:
            logger.error(f"DHIS2 metadata request failed: {e}")
            return json.dumps({
                "success": False,
                "error": str(e)
            })

    @tool("list_dhis2_indicators")
    def list_dhis2_indicators(category: Optional[str] = None) -> str:
        """
        Lists available indicators in DHIS2.

        Args:
            category: Optional indicator category to filter by

        Returns:
            JSON string with available indicators
        """
        return get_dhis2_metadata("indicators", query=category)


dhis2_tools = [
    DHIS2Tools.fetch_dhis2_analytics,
    DHIS2Tools.get_dhis2_metadata,
    DHIS2Tools.list_dhis2_indicators
]
