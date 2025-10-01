#!/usr/bin/env python3
"""
Demo script for Thrift E-commerce Content Generator.

This script demonstrates the thrift product analysis functionality including:
- Creating sample product items
- AI-powered feature analysis
- Product description generation
- Pricing guidance
- Image enhancement suggestions
"""

import os
import sys
from datetime import datetime, timezone

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from baddie_journal.models import ProductItem, ProductListing  # noqa: E402

# Optional thrift swarms integration
try:
    from baddie_journal.thrift_swarms import ThriftContentSwarm, is_thrift_swarms_available  # noqa: E402

    THRIFT_SWARMS_AVAILABLE = is_thrift_swarms_available()
except ImportError:
    THRIFT_SWARMS_AVAILABLE = False
    ThriftContentSwarm = None


def create_sample_products() -> list[ProductItem]:
    """Create sample thrift products for demonstration."""
    print("📦 Creating sample product data...")

    products = [
        ProductItem(
            id=1,
            item_type="Vintage Leather Handbag",
            brand="Coach",
            model="Classic Satchel",
            condition="Excellent used",
            key_features=["Genuine leather", "Multiple compartments", "Adjustable strap"],
            known_flaws=["Minor wear on corners"],
            target_audience="Fashion-conscious professionals",
            original_retail_price=298.00,
            acquisition_cost=45.00,
            image_urls=["https://example.com/handbag1.jpg"],
            user_description="Beautiful vintage Coach handbag in excellent condition",
        ),
        ProductItem(
            id=2,
            item_type="Riding Lawn Mower",
            brand="John Deere",
            model="X350",
            condition="Functional with cosmetic wear",
            key_features=["42-inch deck", "Hydrostatic transmission", "Recently serviced"],
            known_flaws=["Some rust on deck", "Seat has minor tears"],
            target_audience="Homeowners with large yards",
            original_retail_price=3299.00,
            acquisition_cost=800.00,
            image_urls=["https://example.com/mower1.jpg", "https://example.com/mower2.jpg"],
            user_description="Reliable John Deere mower, runs great, just serviced",
        ),
        ProductItem(
            id=3,
            item_type="Utility Wagon",
            brand="Radio Flyer",
            condition="New with tags",
            key_features=["All-terrain wheels", "Removable sides", "Folds flat"],
            known_flaws=[],
            target_audience="Families and outdoor enthusiasts",
            original_retail_price=149.99,
            acquisition_cost=75.00,
            image_urls=["https://example.com/wagon1.jpg"],
            user_description="Brand new Radio Flyer wagon, never used",
        ),
    ]

    print(f"✅ Created {len(products)} sample products\n")
    return products


def demonstrate_basic_info(products: list[ProductItem]):
    """Display basic product information."""
    print("📋 BASIC PRODUCT INFORMATION")
    print("=" * 60)

    for product in products:
        print(f"\n🏷️  Product #{product.id}: {product.item_type}")
        print(f"   Brand: {product.brand or 'Unbranded'}")
        print(f"   Condition: {product.condition}")
        print(f"   Key Features: {', '.join(product.key_features)}")
        if product.known_flaws:
            print(f"   Known Flaws: {', '.join(product.known_flaws)}")
        if product.original_retail_price:
            print(f"   Original Retail: ${product.original_retail_price:.2f}")
        if product.acquisition_cost:
            print(f"   Acquisition Cost: ${product.acquisition_cost:.2f}")
        print(f"   Images: {len(product.image_urls)}")


def demonstrate_ai_analysis(products: list[ProductItem]):
    """Demonstrate AI-powered thrift content generation."""
    api_key = os.getenv("OPENAI_API_KEY")

    if not THRIFT_SWARMS_AVAILABLE:
        print("\n⚠️  THRIFT AI ANALYSIS - NOT AVAILABLE")
        print("-" * 60)
        print("Swarms and OpenAI packages are required for AI analysis.")
        print("Install with: pip install swarms>=6.0.0 openai>=1.0.0")
        return

    if not api_key:
        print("\n⚠️  THRIFT AI ANALYSIS - API KEY REQUIRED")
        print("-" * 60)
        print("Set OPENAI_API_KEY environment variable to enable AI analysis")
        print("Example: export OPENAI_API_KEY='your-key-here'")
        return

    print("\n\n🤖 AI-POWERED THRIFT CONTENT GENERATION")
    print("=" * 60)
    print("Using Swarms AI agents to analyze products...\n")

    try:
        swarm = ThriftContentSwarm(api_key=api_key)

        # Analyze first product in detail
        product = products[0]
        print(f"🔍 Analyzing: {product.item_type}")
        print("-" * 60)

        result = swarm.perform_comprehensive_analysis(product)

        # Display Product Analysis
        print("\n📝 GENERATED CONTENT:")
        print(f"Product Title: {result.product_analysis.product_title}")
        print(f"\nShort Description:\n{result.product_analysis.short_description}")
        print(f"\nLong Description:\n{result.product_analysis.long_description}")
        
        if result.product_analysis.seo_keywords:
            print(f"\nSEO Keywords: {', '.join(result.product_analysis.seo_keywords)}")
        
        if result.product_analysis.quality_score:
            print(f"\nQuality Score: {result.product_analysis.quality_score}/10")

        # Display Pricing Guidance
        print("\n\n💰 PRICING GUIDANCE:")
        print("-" * 60)
        print(f"Recommended Price: ${result.pricing_guidance.recommended_price:.2f}")
        print(f"Price Range: ${result.pricing_guidance.price_range_min:.2f} - ${result.pricing_guidance.price_range_max:.2f}")
        
        if result.pricing_guidance.new_price_equivalent:
            print(f"New Price Equivalent: ${result.pricing_guidance.new_price_equivalent:.2f}")
        if result.pricing_guidance.used_market_avg:
            print(f"Used Market Average: ${result.pricing_guidance.used_market_avg:.2f}")
        if result.pricing_guidance.profit_margin:
            print(f"Profit Margin: {result.pricing_guidance.profit_margin:.1f}%")
        
        print(f"\nRationale: {result.pricing_guidance.pricing_rationale}")

        # Display Image Suggestions
        print("\n\n📸 IMAGE ENHANCEMENT SUGGESTIONS:")
        print("-" * 60)
        if "additional_views_needed" in result.image_suggestions:
            print("Additional Views Needed:")
            for view in result.image_suggestions["additional_views_needed"]:
                print(f"  • {view}")
        
        if "background_suggestion" in result.image_suggestions:
            print(f"\nBackground: {result.image_suggestions['background_suggestion']}")
        
        if "lighting_notes" in result.image_suggestions:
            print(f"Lighting: {result.image_suggestions['lighting_notes']}")

        # Create and display Mini Product Page
        print("\n\n📄 MINI PRODUCT PAGE (Copy-Paste Ready)")
        print("=" * 60)
        listing = ProductListing(
            product=product,
            analysis=result.product_analysis,
            pricing=result.pricing_guidance,
            enhanced_images=product.image_urls,
        )
        print(listing.format_mini_page())

    except Exception as e:
        print(f"❌ AI analysis failed: {str(e)}")
        print("   This might be due to API key issues or network connectivity.")


def main():
    """Main demonstration function."""
    print("🌟 THRIFT E-COMMERCE CONTENT GENERATOR - DEMO")
    print("=" * 60)
    print("ThriftGenius / ReStyle AI / CuratedThrift Pro")
    print("=" * 60)

    # Create sample products
    products = create_sample_products()

    # Show basic information
    demonstrate_basic_info(products)

    # Demonstrate AI analysis
    demonstrate_ai_analysis(products)

    print("\n✨ Demo completed!")
    print("\nTo use with your own products:")
    print("1. Create ProductItem objects with your product details")
    print("2. Set OPENAI_API_KEY environment variable")
    print("3. Use ThriftContentSwarm to analyze and generate content")
    print("\nFor image uploads, extend with actual image processing libraries.")


if __name__ == "__main__":
    main()
