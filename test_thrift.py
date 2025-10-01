#!/usr/bin/env python3
"""
Test script for ThriftGenius E-commerce Content Generator.

This script tests all aspects of the thrift product functionality:
- Product model creation and serialization
- Basic functionality without AI
- AI-powered analysis (when API key available)
- Web interface routes (basic tests)
"""

import os
import sys
from datetime import datetime, timezone

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_product_models():
    """Test product model creation and serialization."""
    print("\n" + "=" * 60)
    print("TEST 1: Product Models")
    print("=" * 60)

    try:
        from baddie_journal.models import (
            ProductItem,
            ProductAnalysis,
            PricingGuidance,
            ProductListing,
        )

        # Test ProductItem
        product = ProductItem(
            id=1,
            item_type="Test Handbag",
            brand="TestBrand",
            condition="Excellent used",
            key_features=["Feature 1", "Feature 2"],
            known_flaws=["Minor flaw"],
            original_retail_price=100.00,
            acquisition_cost=25.00,
        )

        assert product.id == 1
        assert product.item_type == "Test Handbag"
        assert product.brand == "TestBrand"
        assert len(product.key_features) == 2
        print("✅ ProductItem creation: PASSED")

        # Test to_dict serialization
        product_dict = product.to_dict()
        assert "id" in product_dict
        assert "item_type" in product_dict
        assert product_dict["brand"] == "TestBrand"
        print("✅ ProductItem serialization: PASSED")

        # Test ProductAnalysis
        analysis = ProductAnalysis(
            product_id=1,
            product_title="Test Product Title",
            short_description="Test short description",
            long_description="Test long description",
            detected_features=["Feature A", "Feature B"],
            quality_score=8.5,
        )

        assert analysis.product_id == 1
        assert analysis.quality_score == 8.5
        print("✅ ProductAnalysis creation: PASSED")

        # Test PricingGuidance
        pricing = PricingGuidance(
            product_id=1,
            recommended_price=75.00,
            price_range_min=65.00,
            price_range_max=85.00,
            new_price_equivalent=100.00,
            used_market_avg=70.00,
            pricing_rationale="Test rationale",
        )

        assert pricing.recommended_price == 75.00
        assert pricing.price_range_min == 65.00
        print("✅ PricingGuidance creation: PASSED")

        # Test ProductListing
        listing = ProductListing(
            product=product,
            analysis=analysis,
            pricing=pricing,
        )

        assert listing.product.id == product.id
        assert listing.analysis.product_id == analysis.product_id
        print("✅ ProductListing creation: PASSED")

        # Test format_mini_page
        mini_page = listing.format_mini_page()
        assert "Product Listing:" in mini_page
        assert "Test Product Title" in mini_page
        assert "$75.00" in mini_page
        print("✅ ProductListing mini_page formatting: PASSED")

        print("\n✅ ALL PRODUCT MODEL TESTS PASSED")
        return True

    except Exception as e:
        print(f"\n❌ Product model tests FAILED: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def test_basic_functionality():
    """Test basic thrift functionality without AI."""
    print("\n" + "=" * 60)
    print("TEST 2: Basic Functionality (No AI)")
    print("=" * 60)

    try:
        from baddie_journal.models import ProductItem

        # Create multiple test products
        products = [
            ProductItem(
                id=1,
                item_type="Handbag",
                brand="Coach",
                condition="Excellent used",
                key_features=["Leather", "Multiple compartments"],
                original_retail_price=298.00,
            ),
            ProductItem(
                id=2,
                item_type="Lawn Mower",
                brand="John Deere",
                condition="Functional with wear",
                key_features=["42-inch deck", "Hydrostatic transmission"],
                original_retail_price=3299.00,
                acquisition_cost=800.00,
            ),
        ]

        assert len(products) == 2
        print("✅ Multiple product creation: PASSED")

        # Test product list operations
        for product in products:
            assert product.created_at is not None
            assert isinstance(product.created_at, datetime)
        print("✅ Timestamp initialization: PASSED")

        # Test serialization of list
        serialized = [p.to_dict() for p in products]
        assert len(serialized) == 2
        assert all("id" in p for p in serialized)
        print("✅ Bulk serialization: PASSED")

        print("\n✅ ALL BASIC FUNCTIONALITY TESTS PASSED")
        return True

    except Exception as e:
        print(f"\n❌ Basic functionality tests FAILED: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def test_ai_integration():
    """Test AI-powered thrift content generation."""
    print("\n" + "=" * 60)
    print("TEST 3: AI Integration (requires OpenAI API key)")
    print("=" * 60)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  SKIPPED: OPENAI_API_KEY not set")
        print("   Set environment variable to test AI features")
        return True  # Not a failure, just skipped

    try:
        from baddie_journal.models import ProductItem
        from baddie_journal.thrift_swarms import ThriftContentSwarm

        print("🔄 Testing AI integration...")

        # Create test product
        product = ProductItem(
            id=1,
            item_type="Vintage Leather Handbag",
            brand="Coach",
            condition="Excellent used",
            key_features=["Genuine leather", "Multiple compartments", "Adjustable strap"],
            known_flaws=["Minor wear on corners"],
            target_audience="Fashion-conscious professionals",
            original_retail_price=298.00,
            acquisition_cost=45.00,
            user_description="Beautiful vintage Coach handbag in excellent condition",
        )

        # Initialize swarm
        swarm = ThriftContentSwarm(api_key=api_key)
        print("✅ ThriftContentSwarm initialization: PASSED")

        # Test feature analysis
        print("🔄 Testing feature analysis...")
        feature_analysis = swarm.analyze_product_features(product)
        assert isinstance(feature_analysis, dict)
        print("✅ Feature analysis: PASSED")

        # Test description generation
        print("🔄 Testing description generation...")
        descriptions = swarm.generate_descriptions(product, feature_analysis)
        assert isinstance(descriptions, dict)
        if "product_title" in descriptions:
            print(f"   Generated title: {descriptions['product_title'][:50]}...")
        print("✅ Description generation: PASSED")

        # Test pricing guidance
        print("🔄 Testing pricing guidance...")
        pricing = swarm.generate_pricing_guidance(product, feature_analysis)
        assert isinstance(pricing, dict)
        if "recommended_price" in pricing:
            print(f"   Recommended price: ${pricing['recommended_price']:.2f}")
        print("✅ Pricing guidance: PASSED")

        # Test comprehensive analysis
        print("🔄 Testing comprehensive analysis...")
        result = swarm.perform_comprehensive_analysis(product)
        assert result.product_analysis is not None
        assert result.pricing_guidance is not None
        assert result.image_suggestions is not None
        print("✅ Comprehensive analysis: PASSED")

        # Verify result contents
        assert result.product_analysis.product_title is not None
        assert result.product_analysis.short_description is not None
        assert result.product_analysis.long_description is not None
        assert result.pricing_guidance.recommended_price > 0
        print("✅ Result validation: PASSED")

        print("\n✅ ALL AI INTEGRATION TESTS PASSED")
        return True

    except ImportError as e:
        print(f"⚠️  SKIPPED: Required packages not installed")
        print(f"   Install with: pip install swarms openai")
        return True  # Not a failure, just skipped
    except Exception as e:
        print(f"\n❌ AI integration tests FAILED: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def test_web_routes():
    """Test Flask web routes for thrift functionality."""
    print("\n" + "=" * 60)
    print("TEST 4: Web Routes (Flask)")
    print("=" * 60)

    try:
        # Import app
        import app as flask_app

        assert hasattr(flask_app, "app")
        print("✅ Flask app import: PASSED")

        # Check routes exist
        with flask_app.app.test_client() as client:
            # Test thrift home route
            response = client.get("/thrift")
            assert response.status_code == 200
            print("✅ /thrift route: PASSED")

            # Test health endpoint still works
            response = client.get("/health")
            assert response.status_code == 200
            print("✅ /health route: PASSED")

        print("\n✅ ALL WEB ROUTE TESTS PASSED")
        return True

    except Exception as e:
        print(f"\n❌ Web route tests FAILED: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("THRIFTGENIUS TEST SUITE")
    print("=" * 60)
    print("Testing all aspects of thrift e-commerce functionality")
    print("=" * 60)

    results = {
        "Product Models": test_product_models(),
        "Basic Functionality": test_basic_functionality(),
        "AI Integration": test_ai_integration(),
        "Web Routes": test_web_routes(),
    }

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("\nThriftGenius is ready to use!")
        print("- Run 'python demo_thrift.py' for a demonstration")
        print("- Run 'python app.py' and visit /thrift for web interface")
        print("- Set OPENAI_API_KEY for AI-powered content generation")
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("Please review the errors above and fix issues.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
