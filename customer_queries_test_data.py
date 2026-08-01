


customer_queries = [
    {"query": "What is your return policy?",
     "expected_output": "Items can be returned within 30 days of purchase, unworn and with original tags.."},
    {"query": "Where is my order ORD123?"},
    {"query": "whats the standard shipping time and cost?",
     "expected_output": "Standard shipping takes 5-7 business days and shipping charges of $10 for orders below $50, free shipping for orders above $50"},
    {"query": "Not able to access account even with right password?"},
    {"query": "Account locked, what to do?"},
    {"query": "where is my order ord333"},
    {"query": "is cash accepted?"},
    {"query": "coupon not working, what to do?"},
    {"query": "i want to cancel my order?"},
    {"query": "Cancel my order,already made a purchase,please help. ORD774"},
    {"query": "My email is john.smith@gmail.com and my phone is 555-123-4567, can you confirm my order was received?"}
]


customer_queries_tool_cases = [
    {"query": "Where is my order ORD123?"},
    {"query": "where is my order ord333"},
    {"query": "Cancel my order,already made a purchase,please help. ORD774"}
]



customer_queries_context_cases = [
    {"query": "What is your return policy?",
     "expected_output": "Items can be returned within 30 days of purchase, unworn and with original tags.."},
    {"query": "whats the standard shipping time and cost?",
     "expected_output": "Standard shipping takes 5-7 business days and shipping charges of $10 for orders below $50, free shipping for orders above $50"}
]