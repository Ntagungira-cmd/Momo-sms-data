#!/usr/bin/env python3
"""
Data Structures & Algorithms (DSA) Integration
Comparing Linear Search vs Dictionary Lookup for SMS Transaction Records


"""

import time
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import statistics


class Transaction:
    """Represents an SMS transaction record"""
    
    def __init__(self, transaction_id: str, sender: str, recipient: str, 
                 amount: float, timestamp: datetime, status: str = "completed"):
        self.id = transaction_id
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = timestamp
        self.status = status
    
    def __repr__(self):
        return f"Transaction(id='{self.id}', sender='{self.sender}', amount={self.amount})"
    
    def to_dict(self):
        """Convert transaction to dictionary format"""
        return {
            'id': self.id,
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp.isoformat(),
            'status': self.status
        }


def generate_sample_transactions(count: int = 50) -> List[Transaction]:
    """
    Generate sample transaction data for testing
    
    Args:
        count: Number of transactions to generate (default 50)
    
    Returns:
        List of Transaction objects
    """
    transactions = []
    
    # Sample phone numbers and names
    phone_numbers = [f"+250{random.randint(700000000, 799999999)}" for _ in range(20)]
    names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry", 
             "Ivy", "Jack", "Karen", "Leo", "Mary", "Nick", "Olivia", "Paul"]
    
    for i in range(count):
        transaction_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        sender = random.choice(names)
        recipient = random.choice(names)
        amount = round(random.uniform(100, 50000), 2)  # Random amount between 100-50000
        
        # Random timestamp within the last 30 days
        days_ago = random.randint(0, 30)
        timestamp = datetime.now() - timedelta(days=days_ago, 
                                              hours=random.randint(0, 23),
                                              minutes=random.randint(0, 59))
        
        status = random.choice(["completed", "pending", "failed"])
        
        transactions.append(Transaction(transaction_id, sender, recipient, 
                                      amount, timestamp, status))
    
    return transactions


def linear_search(transactions: List[Transaction], target_id: str) -> Optional[Transaction]:
    """
    Linear Search Implementation
    
    Time Complexity: O(n) - worst case
    Space Complexity: O(1)
    
    Args:
        transactions: List of Transaction objects
        target_id: ID to search for
    
    Returns:
        Transaction object if found, None otherwise
    """
    for transaction in transactions:
        if transaction.id == target_id:
            return transaction
    return None


def dictionary_lookup(transaction_dict: Dict[str, Transaction], target_id: str) -> Optional[Transaction]:
    """
    Dictionary Lookup Implementation
    
    Time Complexity: O(1) - average case
    Space Complexity: O(n) - for storing the dictionary
    
    Args:
        transaction_dict: Dictionary mapping IDs to Transaction objects
        target_id: ID to search for
    
    Returns:
        Transaction object if found, None otherwise
    """
    return transaction_dict.get(target_id)


def create_transaction_dictionary(transactions: List[Transaction]) -> Dict[str, Transaction]:
    """
    Create a dictionary from list of transactions for faster lookup
    
    Args:
        transactions: List of Transaction objects
    
    Returns:
        Dictionary mapping transaction IDs to Transaction objects
    """
    return {transaction.id: transaction for transaction in transactions}


def measure_search_performance(transactions: List[Transaction], 
                             search_ids: List[str], 
                             iterations: int = 100) -> Tuple[float, float]:
    """
    Measure and compare performance of linear search vs dictionary lookup
    
    Args:
        transactions: List of Transaction objects
        search_ids: List of IDs to search for
        iterations: Number of iterations for more accurate timing
    
    Returns:
        Tuple of (linear_search_time, dictionary_lookup_time) in seconds
    """
    # Prepare dictionary for lookup
    transaction_dict = create_transaction_dictionary(transactions)
    
    # Measure Linear Search
    linear_times = []
    for _ in range(iterations):
        start_time = time.perf_counter()
        for search_id in search_ids:
            linear_search(transactions, search_id)
        end_time = time.perf_counter()
        linear_times.append(end_time - start_time)
    
    # Measure Dictionary Lookup
    dict_times = []
    for _ in range(iterations):
        start_time = time.perf_counter()
        for search_id in search_ids:
            dictionary_lookup(transaction_dict, search_id)
        end_time = time.perf_counter()
        dict_times.append(end_time - start_time)
    
    return statistics.mean(linear_times), statistics.mean(dict_times)


def binary_search_suggestion():
    """
    Suggestion for Binary Search implementation
    Note: This would require sorted data
    """
    return """
    BINARY SEARCH OPTIMIZATION:
    
    If we sort transactions by ID, we could implement binary search:
    - Time Complexity: O(log n)
    - Space Complexity: O(1)
    - Requirement: Sorted data
    
    def binary_search(sorted_transactions, target_id):
        left, right = 0, len(sorted_transactions) - 1
        
        while left <= right:
            mid = (left + right) // 2
            mid_id = sorted_transactions[mid].id
            
            if mid_id == target_id:
                return sorted_transactions[mid]
            elif mid_id < target_id:
                left = mid + 1
            else:
                right = mid - 1
        
        return None
    """


def print_analysis():
    """Print detailed analysis of the algorithms"""
    print("\n" + "="*80)
    print("ALGORITHM ANALYSIS & REFLECTION")
    print("="*80)
    
    print("\n1. WHY IS DICTIONARY LOOKUP FASTER?")
    print("-" * 40)
    print("• Hash Table Implementation: Dictionaries use hash tables internally")
    print("• Direct Access: Hash function computes the index directly")
    print("• Average O(1): Constant time complexity for lookups")
    print("• No Sequential Scanning: Unlike linear search, doesn't check every element")
    
    print("\n2. TIME COMPLEXITY COMPARISON:")
    print("-" * 40)
    print("• Linear Search: O(n) - worst case checks all n elements")
    print("• Dictionary Lookup: O(1) - average case, direct hash-based access")
    print("• Binary Search: O(log n) - requires sorted data")
    
    print("\n3. SPACE COMPLEXITY COMPARISON:")
    print("-" * 40)
    print("• Linear Search: O(1) - no extra space needed")
    print("• Dictionary Lookup: O(n) - stores all elements in hash table")
    print("• Binary Search: O(1) - no extra space if data already sorted")
    
    print("\n4. OTHER DATA STRUCTURES & ALGORITHMS:")
    print("-" * 40)
    print("• B-Trees: O(log n) - excellent for database indexing")
    print("• Trie: O(m) where m is key length - good for string prefixes")
    print("• Bloom Filter: O(1) - probabilistic, space-efficient for membership testing")
    print("• Binary Search Tree: O(log n) average - maintains sorted order")
    print("• Hash Set: O(1) - if only need to check existence, not retrieve full record")
    
    print("\n5. REAL-WORLD RECOMMENDATIONS:")
    print("-" * 40)
    print("• For frequent lookups: Use dictionary/hash table")
    print("• For sorted data needs: Use balanced BST or sorted list + binary search")
    print("• For database systems: Use B-tree indexes")
    print("• For memory constraints: Consider compressed data structures")
    print("• For range queries: Use sorted structures or segment trees")


def main():
    """Main function to run the DSA comparison"""
    print("SMS Transaction Data Structure & Algorithm Comparison")
    print("="*60)
    
    # Generate sample data
    print("\nGenerating sample transaction data...")
    transactions = generate_sample_transactions(50)  # Generate 50 transactions
    print(f"Generated {len(transactions)} transactions")
    
    # Select random IDs for testing (ensuring some exist and some don't)
    existing_ids = random.sample([t.id for t in transactions], 15)  # 15 existing IDs
    fake_ids = [f"TXN-FAKE{i:03d}" for i in range(5)]  # 5 non-existent IDs
    test_ids = existing_ids + fake_ids
    random.shuffle(test_ids)
    
    print(f"Testing with {len(test_ids)} search queries")
    print(f"   - {len(existing_ids)} existing IDs")
    print(f"   - {len(fake_ids)} non-existent IDs")
    
    # Measure performance
    print("\nMeasuring performance...")
    linear_time, dict_time = measure_search_performance(transactions, test_ids, iterations=1000)
    
    # Display results
    print("\n" + "="*60)
    print("PERFORMANCE RESULTS")
    print("="*60)
    print(f"Dataset Size: {len(transactions)} transactions")
    print(f"Search Queries: {len(test_ids)} IDs")
    print(f"Iterations: 1000 (for statistical accuracy)")
    print()
    print(f"Linear Search Time:    {linear_time*1000:.4f} ms")
    print(f"Dictionary Lookup Time: {dict_time*1000:.4f} ms")
    print()
    print(f"Speed Improvement: {linear_time/dict_time:.2f}x faster with dictionary")
    print(f"Time Saved: {(linear_time-dict_time)*1000:.4f} ms per search cycle")
    
    # Demonstrate actual searches
    print("\n" + "="*60)
    print("SEARCH DEMONSTRATIONS")
    print("="*60)
    
    transaction_dict = create_transaction_dictionary(transactions)
    
    # Show a few example searches
    for i, search_id in enumerate(test_ids[:5]):
        print(f"\nSearch {i+1}: Looking for ID '{search_id}'")
        
        # Linear search
        start = time.perf_counter()
        linear_result = linear_search(transactions, search_id)
        linear_search_time = time.perf_counter() - start
        
        # Dictionary lookup
        start = time.perf_counter()
        dict_result = dictionary_lookup(transaction_dict, search_id)
        dict_search_time = time.perf_counter() - start
        
        if linear_result:
            print(f"   Found: {linear_result}")
        else:
            print(f"   Not found")
        
        print(f"   Linear search: {linear_search_time*1000000:.2f} μs")
        print(f"   Dict lookup:   {dict_search_time*1000000:.2f} μs")
        print(f"   Speedup: {linear_search_time/dict_search_time:.1f}x")
    
    # Print analysis
    print_analysis()
    
    print(binary_search_suggestion())
    
    print("\n" + "="*80)
    print("CONCLUSION")
    print("="*80)
    print("Dictionary lookup significantly outperforms linear search due to hash-based")
    print("direct access. For production systems handling SMS transactions, using")
    print("dictionary/hash table indexing is essential for performance at scale.")
    print("="*80)


if __name__ == "__main__":
    main()