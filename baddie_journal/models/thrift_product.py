"""
Thrift product models for e-commerce content generation.

This module contains data models for thrift store items, product analysis,
and pricing guidance for the High-End Thrift E-commerce Content Generator.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any


@dataclass
class ProductItem:
    """Represents a thrift store product item."""

    id: int
    item_type: str  # e.g., "Handbag", "Riding Mower", "Utility Wagon"
    brand: Optional[str] = None
    model: Optional[str] = None
    condition: str = "Used"  # "New with tags", "Excellent used", "Functional with cosmetic wear"
    key_features: List[str] = field(default_factory=list)
    known_flaws: List[str] = field(default_factory=list)
    target_audience: Optional[str] = None
    original_retail_price: Optional[float] = None
    acquisition_cost: Optional[float] = None
    image_urls: List[str] = field(default_factory=list)
    user_description: Optional[str] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        """Initialize timestamp if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "item_type": self.item_type,
            "brand": self.brand,
            "model": self.model,
            "condition": self.condition,
            "key_features": self.key_features,
            "known_flaws": self.known_flaws,
            "target_audience": self.target_audience,
            "original_retail_price": self.original_retail_price,
            "acquisition_cost": self.acquisition_cost,
            "image_urls": self.image_urls,
            "user_description": self.user_description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


@dataclass
class ProductAnalysis:
    """Result from AI analysis of a product."""

    product_id: int
    product_title: str
    short_description: str
    long_description: str
    detected_features: List[str] = field(default_factory=list)
    seo_keywords: List[str] = field(default_factory=list)
    condition_assessment: Optional[str] = None
    quality_score: Optional[float] = None  # 0-10 scale
    generated_at: Optional[datetime] = None

    def __post_init__(self):
        """Initialize timestamp if not provided."""
        if self.generated_at is None:
            self.generated_at = datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "product_id": self.product_id,
            "product_title": self.product_title,
            "short_description": self.short_description,
            "long_description": self.long_description,
            "detected_features": self.detected_features,
            "seo_keywords": self.seo_keywords,
            "condition_assessment": self.condition_assessment,
            "quality_score": self.quality_score,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
        }


@dataclass
class PricingGuidance:
    """Pricing guidance for a product."""

    product_id: int
    recommended_price: float
    price_range_min: float
    price_range_max: float
    new_price_equivalent: Optional[float] = None
    used_market_avg: Optional[float] = None
    pricing_rationale: str = ""
    comparable_items: List[Dict[str, Any]] = field(default_factory=list)
    profit_margin: Optional[float] = None
    generated_at: Optional[datetime] = None

    def __post_init__(self):
        """Initialize timestamp if not provided."""
        if self.generated_at is None:
            self.generated_at = datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "product_id": self.product_id,
            "recommended_price": self.recommended_price,
            "price_range_min": self.price_range_min,
            "price_range_max": self.price_range_max,
            "new_price_equivalent": self.new_price_equivalent,
            "used_market_avg": self.used_market_avg,
            "pricing_rationale": self.pricing_rationale,
            "comparable_items": self.comparable_items,
            "profit_margin": self.profit_margin,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
        }


@dataclass
class ProductListing:
    """Complete product listing with all generated content."""

    product: ProductItem
    analysis: ProductAnalysis
    pricing: PricingGuidance
    enhanced_images: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "product": self.product.to_dict(),
            "analysis": self.analysis.to_dict(),
            "pricing": self.pricing.to_dict(),
            "enhanced_images": self.enhanced_images,
        }

    def format_mini_page(self) -> str:
        """Format as a mini product page for easy copy-paste."""
        return f"""### Product Listing: {self.analysis.product_title}

**Product Images:**
{chr(10).join(f'[Image {i+1}]({url})' for i, url in enumerate(self.enhanced_images or self.product.image_urls))}

**Short Description:**
{self.analysis.short_description}

**Recommended Price:** ${self.pricing.recommended_price:.2f}

---

**Options for Your Listing:**

*   **Description Type:**
    *   **Short Description** (as above)
    *   **Long Description** (See below for full text)
*   **Price Selection:**
    *   **Recommended Price: ${self.pricing.recommended_price:.2f}**
    *   **Custom Price** (Refer to detailed pricing guidance below)

---

**Full Product Description for IONOS/Website:**

**Product Title:** {self.analysis.product_title}

{self.analysis.long_description}

---

**Detailed Pricing Guidance:**

*   New Price Equivalent: ${self.pricing.new_price_equivalent:.2f if self.pricing.new_price_equivalent else 0:.2f}
*   Used Market Assessment: ${self.pricing.used_market_avg:.2f if self.pricing.used_market_avg else 0:.2f}
*   Recommended Price Range: ${self.pricing.price_range_min:.2f} - ${self.pricing.price_range_max:.2f}
*   Why ${self.pricing.recommended_price:.2f}?: {self.pricing.pricing_rationale}
"""
