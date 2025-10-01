"""
Swarms AI integration for Thrift E-commerce Content Generator.

This module integrates the Swarms framework to provide AI-powered analysis
of thrift store products using specialized agents for different tasks.
"""

import os
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# Optional imports - handle gracefully if not available
try:
    from swarms import Agent

    _swarms_available = True
except ImportError:
    Agent = None
    _swarms_available = False

try:
    from openai import OpenAI

    _openai_available = True
except ImportError:
    OpenAI = None
    _openai_available = False

from .models.thrift_product import ProductItem, ProductAnalysis, PricingGuidance


@dataclass
class ThriftAnalysisResult:
    """Complete result from thrift product analysis."""

    product_analysis: ProductAnalysis
    pricing_guidance: PricingGuidance
    image_suggestions: Dict[str, Any]
    generated_at: datetime


class ThriftContentSwarm:
    """
    Swarm of AI agents specialized for thrift e-commerce content generation.

    This class coordinates multiple AI agents to provide comprehensive
    product analysis, description generation, and pricing guidance.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Thrift Content Swarm.

        Args:
            api_key: OpenAI API key (optional, can use environment variable)
        """
        if not _swarms_available:
            raise ImportError(
                "Swarms framework is not available. Install with: pip install swarms>=6.0.0"
            )

        if not _openai_available:
            raise ImportError(
                "OpenAI package is not available. Install with: pip install openai>=1.0.0"
            )

        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.client = OpenAI(api_key=self.api_key)
        self._initialize_agents()

    def _create_system_prompt(self, name: str, description: str, task: str) -> str:
        """Create a system prompt for an agent."""
        return f"""You are {name}, {description}.

Your primary task is: {task}

Guidelines:
- Provide detailed, professional analysis appropriate for e-commerce
- Focus on highlighting value, quality, and uniqueness
- Be transparent about condition and any flaws
- Use benefit-oriented language that appeals to customers
- Format your response as requested (JSON when specified)
- Maintain a "high-end thrift" tone: curated, valuable, sustainable

Remember: This is for a professional e-commerce thrift store. Present items attractively while being honest."""

    def _initialize_agents(self):
        """Initialize the specialized agents for thrift content generation."""

        # Image & Feature Analysis Agent
        self.image_agent = Agent(
            agent_name="Image & Feature Analyzer",
            system_prompt=self._create_system_prompt(
                name="Image & Feature Analyzer",
                description="an expert at analyzing product images and identifying key features, condition, and quality",
                task="Analyze product images and descriptions to identify key features, materials, "
                "condition assessment, and visual qualities for e-commerce listings",
            ),
            model_name="gpt-4o-mini",
            max_loops=1,
            temperature=0.3,
            openai_api_key=self.api_key,
        )

        # Description Generator Agent
        self.description_agent = Agent(
            agent_name="Description Generator",
            system_prompt=self._create_system_prompt(
                name="Description Generator",
                description="an expert copywriter specializing in e-commerce product descriptions",
                task="Create compelling, SEO-optimized product titles and descriptions "
                "that highlight benefits, features, and value for online shoppers",
            ),
            model_name="gpt-4o-mini",
            max_loops=1,
            temperature=0.6,
            openai_api_key=self.api_key,
        )

        # Pricing Specialist Agent
        self.pricing_agent = Agent(
            agent_name="Pricing Specialist",
            system_prompt=self._create_system_prompt(
                name="Pricing Specialist",
                description="an expert at pricing thrift and resale items competitively",
                task="Analyze product details to provide data-driven pricing recommendations "
                "based on market research, condition, brand value, and competitive positioning",
            ),
            model_name="gpt-4o-mini",
            max_loops=1,
            temperature=0.4,
            openai_api_key=self.api_key,
        )

        # Image Enhancement Advisor Agent
        self.image_enhancement_agent = Agent(
            agent_name="Image Enhancement Advisor",
            system_prompt=self._create_system_prompt(
                name="Image Enhancement Advisor",
                description="an expert in product photography and visual presentation for e-commerce",
                task="Suggest image enhancements, additional angles needed, and visual improvements "
                "to make product photos more appealing and professional",
            ),
            model_name="gpt-4o-mini",
            max_loops=1,
            temperature=0.5,
            openai_api_key=self.api_key,
        )

    def _prepare_product_context(self, product: ProductItem) -> str:
        """Prepare context string from product data."""
        context_parts = [
            f"Item Type: {product.item_type}",
            f"Condition: {product.condition}",
        ]

        if product.brand:
            context_parts.append(f"Brand: {product.brand}")
        if product.model:
            context_parts.append(f"Model: {product.model}")
        if product.key_features:
            context_parts.append(f"Key Features: {', '.join(product.key_features)}")
        if product.known_flaws:
            context_parts.append(f"Known Flaws: {', '.join(product.known_flaws)}")
        if product.target_audience:
            context_parts.append(f"Target Audience: {product.target_audience}")
        if product.original_retail_price:
            context_parts.append(f"Original Retail Price: ${product.original_retail_price:.2f}")
        if product.acquisition_cost:
            context_parts.append(f"Acquisition Cost: ${product.acquisition_cost:.2f}")
        if product.user_description:
            context_parts.append(f"User Description: {product.user_description}")
        if product.image_urls:
            context_parts.append(f"Number of Images: {len(product.image_urls)}")

        return "\n".join(context_parts)

    def analyze_product_features(self, product: ProductItem) -> Dict[str, Any]:
        """
        Analyze product features and condition using the image agent.

        Args:
            product: ProductItem to analyze

        Returns:
            Dictionary containing feature analysis
        """
        context = self._prepare_product_context(product)

        prompt = f"""
{context}

TASK: Analyze this product for e-commerce listing. Provide:
1. Comprehensive list of features (materials, dimensions, functionality, style)
2. Condition assessment (detailed evaluation)
3. Quality indicators (brand reputation, craftsmanship, durability cues)
4. Unique selling points
5. Potential concerns or limitations

Provide your analysis in JSON format with the following structure:
{{
    "features": ["list", "of", "detailed", "features"],
    "condition_assessment": "detailed condition evaluation",
    "quality_score": 7.5,
    "unique_selling_points": ["what", "makes", "this", "special"],
    "concerns": ["any", "limitations", "or", "issues"],
    "material_composition": ["materials", "detected"]
}}
"""

        try:
            response = self.image_agent.run(prompt)
            # Try to parse JSON from response
            try:
                # Look for JSON in the response
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    result = json.loads(response[json_start:json_end])
                    return result
                else:
                    # Fallback: return response as is
                    return {"raw_response": response, "error": "Could not parse JSON"}
            except json.JSONDecodeError:
                return {"raw_response": response, "error": "JSON parsing failed"}
        except Exception as e:
            return {"error": str(e)}

    def generate_descriptions(
        self, product: ProductItem, feature_analysis: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Generate product title and descriptions using the description agent.

        Args:
            product: ProductItem to describe
            feature_analysis: Analysis from analyze_product_features

        Returns:
            Dictionary with product_title, short_description, long_description
        """
        context = self._prepare_product_context(product)
        features_str = json.dumps(feature_analysis, indent=2)

        prompt = f"""
{context}

FEATURE ANALYSIS:
{features_str}

TASK: Generate compelling e-commerce content:
1. Product Title (40-60 characters, include brand if notable, key feature, and condition)
2. Short Description (2-3 sentences, perfect for social media or quick glance, highlight key benefits)
3. Long Description (3-5 paragraphs, full product page, include:
   - Opening hook highlighting value/uniqueness
   - Detailed features with benefits
   - Condition specifics (transparent about any wear)
   - Who it's perfect for (target audience)
   - Call to action emphasizing sustainability/value)

Use a "high-end thrift" tone: professional, valuable, curated, sustainable.

Provide your content in JSON format:
{{
    "product_title": "Compelling Title Here",
    "short_description": "2-3 compelling sentences for social media...",
    "long_description": "Full description with paragraphs separated by \\n\\n...",
    "seo_keywords": ["relevant", "search", "keywords"]
}}
"""

        try:
            response = self.description_agent.run(prompt)
            # Try to parse JSON from response
            try:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    result = json.loads(response[json_start:json_end])
                    return result
                else:
                    return {"error": "Could not parse JSON", "raw_response": response}
            except json.JSONDecodeError:
                return {"error": "JSON parsing failed", "raw_response": response}
        except Exception as e:
            return {"error": str(e)}

    def generate_pricing_guidance(
        self, product: ProductItem, feature_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate pricing guidance using the pricing specialist agent.

        Args:
            product: ProductItem to price
            feature_analysis: Analysis from analyze_product_features

        Returns:
            Dictionary with pricing recommendations
        """
        context = self._prepare_product_context(product)
        features_str = json.dumps(feature_analysis, indent=2)

        prompt = f"""
{context}

FEATURE ANALYSIS:
{features_str}

TASK: Provide data-driven pricing guidance for this thrift item:
1. Research similar new items (estimate new retail price)
2. Research used market (estimate typical resale prices)
3. Factor in: condition, brand value, professional curation, market demand
4. Suggest competitive price range
5. Provide specific recommended price with rationale

Consider:
- High-end thrift positioning (not bargain basement)
- Professional presentation adds value
- Sustainability appeal to customers
- Profit margin if acquisition cost provided

Provide pricing analysis in JSON format:
{{
    "new_price_equivalent": 150.00,
    "used_market_avg": 75.00,
    "price_range_min": 65.00,
    "price_range_max": 95.00,
    "recommended_price": 79.99,
    "pricing_rationale": "Detailed explanation of why this price...",
    "comparable_items": [
        {{"source": "eBay", "price": 70.00, "condition": "Good"}},
        {{"source": "Poshmark", "price": 85.00, "condition": "Excellent"}}
    ],
    "profit_margin_percent": 60.5
}}
"""

        try:
            response = self.pricing_agent.run(prompt)
            # Try to parse JSON from response
            try:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    result = json.loads(response[json_start:json_end])
                    return result
                else:
                    return {"error": "Could not parse JSON", "raw_response": response}
            except json.JSONDecodeError:
                return {"error": "JSON parsing failed", "raw_response": response}
        except Exception as e:
            return {"error": str(e)}

    def suggest_image_enhancements(
        self, product: ProductItem, feature_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Suggest image enhancements and additional views needed.

        Args:
            product: ProductItem with image information
            feature_analysis: Analysis from analyze_product_features

        Returns:
            Dictionary with image enhancement suggestions
        """
        context = self._prepare_product_context(product)

        prompt = f"""
{context}

Current number of images: {len(product.image_urls)}

TASK: Suggest image improvements for professional e-commerce presentation:
1. What additional angles/views are needed? (front, back, side, top, detail shots, etc.)
2. Suggested background (clean, neutral, professional)
3. Lighting improvements needed
4. Detail shots to highlight (materials, tags, unique features, condition indicators)
5. Any retouching suggestions (remove dust, smooth wrinkles, but stay transparent)

Provide suggestions in JSON format:
{{
    "additional_views_needed": ["back view", "detail of closure", "brand tag closeup"],
    "background_suggestion": "Clean white or light gray neutral background",
    "lighting_notes": "Bright, even lighting to show true colors",
    "detail_shots": ["Show material texture closeup", "Capture brand logo"],
    "enhancement_notes": "Remove background clutter, adjust brightness slightly"
}}
"""

        try:
            response = self.image_enhancement_agent.run(prompt)
            try:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    result = json.loads(response[json_start:json_end])
                    return result
                else:
                    return {"raw_response": response}
            except json.JSONDecodeError:
                return {"raw_response": response}
        except Exception as e:
            return {"error": str(e)}

    def perform_comprehensive_analysis(
        self, product: ProductItem
    ) -> ThriftAnalysisResult:
        """
        Perform comprehensive analysis of a thrift product.

        This coordinates all agents to provide complete product analysis,
        descriptions, pricing, and image suggestions.

        Args:
            product: ProductItem to analyze

        Returns:
            ThriftAnalysisResult with all generated content
        """
        # Step 1: Analyze product features
        feature_analysis = self.analyze_product_features(product)

        # Step 2: Generate descriptions
        descriptions = self.generate_descriptions(product, feature_analysis)

        # Step 3: Generate pricing guidance
        pricing_data = self.generate_pricing_guidance(product, feature_analysis)

        # Step 4: Get image suggestions
        image_suggestions = self.suggest_image_enhancements(product, feature_analysis)

        # Create ProductAnalysis
        product_analysis = ProductAnalysis(
            product_id=product.id,
            product_title=descriptions.get("product_title", f"{product.item_type} - {product.brand or 'Unbranded'}"),
            short_description=descriptions.get("short_description", "High-quality thrift find."),
            long_description=descriptions.get("long_description", "A carefully curated thrift item."),
            detected_features=feature_analysis.get("features", product.key_features),
            seo_keywords=descriptions.get("seo_keywords", []),
            condition_assessment=feature_analysis.get("condition_assessment", product.condition),
            quality_score=feature_analysis.get("quality_score"),
        )

        # Create PricingGuidance
        pricing_guidance = PricingGuidance(
            product_id=product.id,
            recommended_price=pricing_data.get("recommended_price", 29.99),
            price_range_min=pricing_data.get("price_range_min", 24.99),
            price_range_max=pricing_data.get("price_range_max", 34.99),
            new_price_equivalent=pricing_data.get("new_price_equivalent"),
            used_market_avg=pricing_data.get("used_market_avg"),
            pricing_rationale=pricing_data.get("pricing_rationale", "Competitive market pricing"),
            comparable_items=pricing_data.get("comparable_items", []),
            profit_margin=(
                ((pricing_data.get("recommended_price", 0) - product.acquisition_cost) / 
                 pricing_data.get("recommended_price", 1) * 100)
                if product.acquisition_cost and pricing_data.get("recommended_price")
                else None
            ),
        )

        return ThriftAnalysisResult(
            product_analysis=product_analysis,
            pricing_guidance=pricing_guidance,
            image_suggestions=image_suggestions,
            generated_at=datetime.now(timezone.utc),
        )


def is_thrift_swarms_available() -> bool:
    """Check if Swarms and OpenAI are available for thrift content generation."""
    return _swarms_available and _openai_available
