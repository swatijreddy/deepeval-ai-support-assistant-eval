

import re
from anthropic import Anthropic
from dotenv import load_dotenv
from customer_queries_test_data import customer_queries,customer_queries_tool_cases

from deepeval.test_case import LLMTestCase
from deepeval.test_case import ToolCall 

load_dotenv()

client = Anthropic()
MODEL = "claude-haiku-4-5-20251001"


knowledge_base = [
    "Return Policy: Items can be returned within 30 days of purchase, unworn and with original tags...",
    "Shipping: Standard shipping takes 5-7 business days, express shipping takes 2-3 days...",
    "Payment methods accepted: Accepts various payment options, including credit, debit, like Visa, Mastercard, or American Express and gift cards. Also accept FSA, HSA, EBT cards. No cash accepted",
    "Order cancellation: Orders cannot be cancelled once the product is shipped",
    "Discount codes/promotions: Only one discount/promo code can be applied per transaction",
    "Shipping cost: Free shipping for orders above $50, shipping charges of $10 for orders below $50",
    "Account/password issues: For password reset, refer below link. Account locked - please reach us @+1 876-767-8752, any other account related issue, drop an email to (customer_care247@gmail.com)"
]


def retrieve_context(question):
    keywords = ["return", "policy", "shipping", "payment", "cancel", "discount", "code", "promo", "account", "password", "issues"]
    relevant_information = []
    question_lower = question.lower()

    for info in knowledge_base:
        info_lower = info.lower()
        for keyword in keywords:
            if keyword in question_lower and keyword in info_lower:
                relevant_information.append(info)
                break

    return relevant_information


fake_orders = {
    "ORD123": "shipped, expected delivery in 2 days",
    "ORD456": "delivered on July 20th",
    "ORD774": "in transit,will update shipping details asap",
    "ORD350": "out for delivery",
    "ORD874": "delay in delivery,waitibf for product re-stock"}


def check_order_status(order_id):
    if order_id in fake_orders:
        return f"Order {order_id}: {fake_orders[order_id]}"
    else:
        return f"Order {order_id} not found "


def extract_order_id(query):
    match_order = re.search(r"ORD\d+",query,re.IGNORECASE)
    if match_order:
        return match_order.group()
    else :
       return None

def generate_reply(query):

    order_id = extract_order_id(query)
    policy_info = retrieve_context(query)
    tool_called = None

    if order_id is not None:
      order_status = check_order_status(order_id)
      context = f"{order_status}\n{policy_info}"
      tool_called = "check_order_status"

    else: 
      context = policy_info

    prompt = f"""You are a customer support assistant who give relevant answer/reply to customer questions/queries.\n
        Reply only with the information given to you below, dont add anything you weren't told.\n
        If you dont have any information doesn't answer the question,reply: "reach out to customer_care247@gmail.com for further help."\n


        Start your message with a greeting, end the conversation with Thank you!\n
        

        Customer_Queries:
        {query}
        
        Information  to answer :
        {context}

        """
    
    message = client.messages.create(
        model = MODEL,
        temperature = 0,
        max_tokens = 150,
        messages = [{
            "role": "user",
            "content": prompt
        }
        ])

    reply =  message.content[0].text.strip()
    return reply,context,tool_called


  
def build_test_case(case,expected_tool = None,expected_output=None):
    
    query = case["query"]
    expected_output = case.get("expected_output")

    if query in all_replies:
       reply, context, tool_called = all_replies[query]
    else:
        reply, context, tool_called = generate_reply(query)

    context_field = [context] if isinstance(context, str) else context

    return LLMTestCase(
        input=query,
        actual_output=reply,
        context=context_field,
        retrieval_context=context_field,
        expected_output=expected_output,
        tools_called=[ToolCall(name=tool_called)] if tool_called else [],
        expected_tools=[ToolCall(name=expected_tool)] if expected_tool else []

    )


def get_all_replies():

    all_replies = {}
    for case in customer_queries:
        query = case["query"]
        output = generate_reply(query)
        all_replies[query] = output
    return all_replies

all_replies = get_all_replies()