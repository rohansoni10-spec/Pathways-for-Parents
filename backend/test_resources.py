"""
Test script for Resources API endpoints.
Tests filtering by category and search functionality.
"""

import asyncio
import httpx
from typing import Optional

BASE_URL = "http://localhost:8000"


async def test_get_all_resources():
    """Test getting all resources without filters."""
    print("\n=== Test 1: Get All Resources ===")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/v1/resources")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            resources = response.json()
            print(f"Total resources: {len(resources)}")
            if resources:
                print(f"First resource: {resources[0]['title']}")
        else:
            print(f"Error: {response.text}")


async def test_filter_by_category(category: str):
    """Test filtering resources by category."""
    print(f"\n=== Test 2: Filter by Category '{category}' ===")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/api/v1/resources",
            params={"category": category}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            resources = response.json()
            print(f"Resources found: {len(resources)}")
            for resource in resources:
                print(f"  - {resource['title']} (Category: {resource['category']})")
        else:
            print(f"Error: {response.text}")


async def test_search_resources(search_term: str):
    """Test searching resources by keyword."""
    print(f"\n=== Test 3: Search for '{search_term}' ===")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/api/v1/resources",
            params={"search": search_term}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            resources = response.json()
            print(f"Resources found: {len(resources)}")
            for resource in resources:
                print(f"  - {resource['title']}")
                print(f"    Tags: {', '.join(resource['tags'])}")
        else:
            print(f"Error: {response.text}")


async def test_combined_filter_and_search(category: str, search_term: str):
    """Test combining category filter and search."""
    print(f"\n=== Test 4: Filter by '{category}' AND Search for '{search_term}' ===")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/api/v1/resources",
            params={"category": category, "search": search_term}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            resources = response.json()
            print(f"Resources found: {len(resources)}")
            for resource in resources:
                print(f"  - {resource['title']} (Category: {resource['category']})")
        else:
            print(f"Error: {response.text}")


async def test_get_resource_by_id(resource_id: str):
    """Test getting a specific resource by ID."""
    print(f"\n=== Test 5: Get Resource by ID '{resource_id}' ===")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/v1/resources/{resource_id}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            resource = response.json()
            print(f"Title: {resource['title']}")
            print(f"Category: {resource['category']}")
            print(f"Description: {resource['description'][:100]}...")
            print(f"URL: {resource['url']}")
            print(f"Tags: {', '.join(resource['tags'])}")
        else:
            print(f"Error: {response.text}")


async def test_get_nonexistent_resource():
    """Test getting a resource that doesn't exist."""
    print("\n=== Test 6: Get Non-existent Resource ===")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/v1/resources/nonexistent")
        print(f"Status: {response.status_code}")
        if response.status_code == 404:
            print("✓ Correctly returned 404 for non-existent resource")
            print(f"Error message: {response.json()['detail']}")
        else:
            print(f"Unexpected response: {response.text}")


async def test_case_insensitive_search():
    """Test that search is case-insensitive."""
    print("\n=== Test 7: Case-Insensitive Search ===")
    search_terms = ["IEP", "iep", "Iep"]
    
    for term in search_terms:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/api/v1/resources",
                params={"search": term}
            )
            if response.status_code == 200:
                resources = response.json()
                print(f"Search '{term}': {len(resources)} results")
            else:
                print(f"Error searching for '{term}': {response.text}")


async def main():
    """Run all tests."""
    print("=" * 60)
    print("RESOURCES API TEST SUITE")
    print("=" * 60)
    
    try:
        # Test 1: Get all resources
        await test_get_all_resources()
        
        # Test 2: Filter by different categories
        await test_filter_by_category("Diagnosis")
        await test_filter_by_category("IEP")
        await test_filter_by_category("Therapy")
        
        # Test 3: Search by keyword
        await test_search_resources("iep")
        await test_search_resources("therapy")
        await test_search_resources("early intervention")
        
        # Test 4: Combined filter and search
        await test_combined_filter_and_search("IEP", "meeting")
        
        # Test 5: Get specific resource
        await test_get_resource_by_id("r1")
        await test_get_resource_by_id("r3")
        
        # Test 6: Non-existent resource
        await test_get_nonexistent_resource()
        
        # Test 7: Case-insensitive search
        await test_case_insensitive_search()
        
        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())