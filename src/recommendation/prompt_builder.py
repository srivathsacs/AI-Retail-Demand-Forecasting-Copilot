from inventory import InventoryAnalysis
from metrics import BusinessAnalysis


class PromptBuilder:
    """
    Build the prompt for the Recommendation Engine.
    """

    def build(
        self,
        inventory: InventoryAnalysis,
        business: BusinessAnalysis,
        retrieved_context: list[dict],
        user_prompt: str | None = None,
    ) -> str:
        """
        Build the final prompt for the language model.
        """

        context = "\n\n".join(
            chunk["content"]
            for chunk in retrieved_context
        )

        prompt = f"""
You are an AI Retail Demand Forecasting Copilot.

Use ONLY the business context and retrieved knowledge provided below.

Business Context

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

Retrieved Knowledge

{context}
"""

        if user_prompt:
            prompt += f"""

Additional User Request

{user_prompt}
"""

        prompt += """

Instructions

- Base your response ONLY on the Business Context and Retrieved Knowledge.
- Do NOT add introductory text.
- Do NOT add concluding remarks.
- Do NOT use Markdown.
- Do NOT use bold formatting.
- Do NOT use numbered lists.
- Return exactly the following format.

Executive Summary:
<summary>

Recommendation:
<recommendation>

Business Rationale:
<rationale>
"""

        return prompt.strip()