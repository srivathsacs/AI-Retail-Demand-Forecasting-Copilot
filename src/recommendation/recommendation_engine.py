import os
import re

from dotenv import load_dotenv
from google import genai

from config import (
    CHROMA_DB_DIR,
    GEMINI_MODEL,
    RAG_COLLECTION_NAME,
    RAG_TOP_K,
)

from inventory import InventoryAnalysis
from metrics import BusinessAnalysis

from rag.knowledge_retriever import KnowledgeRetriever

from recommendation.prompt_builder import PromptBuilder
from recommendation.recommendation import Recommendation


class RecommendationEngine:
    """
    Generate AI recommendations from business context and
    retrieved knowledge.
    """

    def __init__(self) -> None:

        load_dotenv()

        self._client = genai.Client(
            api_key=os.getenv("GOOGLE_API_KEY")
        )

        self._retriever = KnowledgeRetriever(
            chroma_db_path=str(CHROMA_DB_DIR),
            collection_name=RAG_COLLECTION_NAME,
        )

        self._prompt_builder = PromptBuilder()

    def generate(
        self,
        inventory: InventoryAnalysis,
        business: BusinessAnalysis,
        user_prompt: str | None = None,
    ) -> Recommendation:
        """
        Generate an AI recommendation.
        """

        retrieval_query = (
            f"""
Projected Inventory: {inventory.projected_inventory:.2f}
Inventory Gap: {inventory.inventory_gap:.2f}
Stockout Risk: {inventory.stockout_risk}
Overstock Risk: {inventory.overstock_risk}
Risk Severity: {inventory.risk_severity}

Potential Lost Sales: {business.potential_lost_sales:.2f}
Revenue Risk: {business.revenue_risk:.2f}
Inventory At Risk: {business.inventory_at_risk:.2f}
Recommended Order Quantity: {business.recommended_order_quantity:.2f}
Inventory Health Score: {business.inventory_health_score:.0f}
"""
        ).strip()

        retrieved_context = self._retriever.retrieve(
            query=retrieval_query,
            top_k=RAG_TOP_K,
        )

        prompt = self._prompt_builder.build(
            inventory=inventory,
            business=business,
            retrieved_context=retrieved_context,
            user_prompt=user_prompt,
        )

        response = self._client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        response_text = response.text.strip()

        summary = ""
        recommendation = ""
        rationale = ""

        summary_match = re.search(
            r"Executive Summary:\s*(.*?)(?=Recommendation:|$)",
            response_text,
            flags=re.DOTALL | re.IGNORECASE,
        )

        recommendation_match = re.search(
            r"Recommendation:\s*(.*?)(?=Business Rationale:|$)",
            response_text,
            flags=re.DOTALL | re.IGNORECASE,
        )

        rationale_match = re.search(
            r"Business Rationale:\s*(.*)$",
            response_text,
            flags=re.DOTALL | re.IGNORECASE,
        )

        if summary_match:
            summary = summary_match.group(1).strip()

        if recommendation_match:
            recommendation = recommendation_match.group(1).strip()

        if rationale_match:
            rationale = rationale_match.group(1).strip()

        if not summary:
            summary = response_text

        if not recommendation:
            recommendation = response_text

        if not rationale:
            rationale = response_text

        return Recommendation(
            summary=summary,
            recommendation=recommendation,
            rationale=rationale,
        )