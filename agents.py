# from autogen_ext.models.openai import OpenAIChatCompletionClient
# from autogen_agentchat.agents import AssistantAgent
# from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
# from tavily import TavilyClient
# from database import store_data,query_db
# from tools import search_web
# from formatting_tools import format_web_data
# import asyncio
# from autogen_agentchat.conditions import (
#     MaxMessageTermination,
#     TextMentionTermination,
# )
# # text_termination = TextMentionTermination("SAY GOODBYE")
# # max_messages_termination = MaxMessageTermination(max_messages=5)
# # terminate=text_termination | max_messages_termination

# def create_team(llm_client):
#     # Initialize Tavily client
#     # tavily_client = TavilyClient(api_key=config.TAVILY_API_KEY)

#     # Query Agent: Interprets user query and initiates workflow
#     query_agent = AssistantAgent(
#         name="QueryAgent",
#         model_client=llm_client,
#         system_message="You interpret user queries, extract key entities and intent, and delegate tasks to the SearchAgent."
#     )

#     # Search Agent: Performs web search using Tavily API
#     search_agent = AssistantAgent(
#         name="SearchAgent",
#         model_client=llm_client,
#         system_message="You perform web searches using the Tavily API and gather relevant raw data. Pass unprocessed results to FormattingAgent for structuring.",
#         tools=[search_web]
#     )

#     # Formatting Agent: Formats and structures web-scraped data
#     formatting_agent = AssistantAgent(
#         name="FormattingAgent",
#         model_client=llm_client,
#         system_message="""You are responsible for formatting and structuring data extracted from web searches. 
#         Your tasks include:
#         1. Clean and organize raw web data into structured formats
#         2. Extract key information like company names, industries, financial data, news highlights
#         3. Format data into consistent JSON structures with proper categorization
#         4. Remove duplicates and irrelevant information
#         5. Standardize company names and industry classifications
#         6. Create summaries and key insights from the formatted data
#         7. Ensure data quality and consistency before passing to DataProcessingAgent
        
#         Always format your output as structured JSON with clear sections like:
#         - company_info: {name, industry, description}
#         - key_metrics: {revenue, employees, market_cap, etc.}
#         - recent_news: [list of relevant news items]
#         - financial_highlights: {key financial data}
#         - market_position: {competitive analysis}
#         - summary: {brief executive summary}
#         """,
#         tools=[format_web_data]
#     )

#     # Data Processing Agent: Processes search results and prepares data for storage
#     data_processing_agent = AssistantAgent(
#         name="DataProcessingAgent",
#         model_client=llm_client,
#         system_message="You process formatted and structured data from FormattingAgent and prepare it for storage in PostgreSQL. Store the clean, structured data with proper metadata.",
#         tools=[store_data]
#     )

#     # Formatting Agent: Formats and structures web-scraped data
#     formatting_agent = AssistantAgent(
#         name="FormattingAgent",
#         model_client=llm_client,
#         system_message="""You are responsible for formatting and structuring data extracted from web searches. 
#         Your tasks include:
#         1. Clean and organize raw web data into structured formats
#         2. Extract key information like company names, industries, financial data, news highlights
#         3. Format data into consistent JSON structures with proper categorization
#         4. Remove duplicates and irrelevant information
#         5. Standardize company names and industry classifications
#         6. Create summaries and key insights from the formatted data
#         7. Ensure data quality and consistency before passing to DataProcessingAgent
        
#         Always format your output as structured JSON with clear sections like:
#         - company_info: {name, industry, description}
#         - key_metrics: {revenue, employees, market_cap, etc.}
#         - recent_news: [list of relevant news items]
#         - financial_highlights: {key financial data}
#         - market_position: {competitive analysis}
#         - summary: {brief executive summary}
#         """
#     )
    
#     formatting_agent1 = AssistantAgent(
#         name="FormattingAgentFinal",
#         model_client=llm_client,
#     system_message="""You are responsible for converting structured or raw web data into a clear, user-friendly answer.
    
#     Your tasks include:
#     1. Analyze and compare the extracted data
#     2. Present comparisons in **well-structured tables** (if numeric or categorical comparison is useful)
#     3. Provide **clear text explanations** instead of JSON or code
#     4. Extract insights such as trends, rankings, and competitive differences
#     5. Give a **final verdict or resolution** to directly answer the user query in plain text
#     6. Do not output JSON, YAML, or raw structured data formats
#     7. Ensure the response reads like a professional market or industry analysis

#     Example style:
#     - Start with a short summary of findings
#     - Use a comparison table if needed (e.g., models, prices, ranges, market share)
#     - Provide a concluding paragraph with the **final verdict** answering the user's intent
#     """
#     )

#     # Response Agent: Generates final response based on database query
#     response_agent = AssistantAgent(
#         name="ResponseAgent",
#         model_client=llm_client,
#         system_message="You generate concise, accurate, and well-formatted responses based on database query results. Present information in a clear, professional manner with proper structure and highlights.",
#         tools=[query_db]
#     )
    
#     terminate = AssistantAgent(
#         "Terminate", model_client=llm_client, system_message="Say Goodbye"
#     )

 
#     # Build the graph using DiGraphBuilder
#     builder = DiGraphBuilder()
#     builder.add_node(query_agent).add_node(search_agent).add_node(formatting_agent).add_node(data_processing_agent).add_node(response_agent).add_node(terminate).add_node(formatting_agent1)
#     builder.add_edge(query_agent, search_agent)
#     builder.add_edge(search_agent, formatting_agent)
#     builder.add_edge(formatting_agent, data_processing_agent)
#     builder.add_edge(data_processing_agent, response_agent)
#     builder.add_edge(response_agent, formatting_agent1)
#     builder.add_edge(formatting_agent1, terminate)
 
#     # Build and validate the graph
#     graph = builder.build()
 
#     # Create the flow with GraphFlow
#     team = GraphFlow(
#         participants=builder.get_participants(),
#         graph=graph,
#         termination_condition= TextMentionTermination("GOODBYE")
#     )
 
#     return team


# agents.py

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.agents import AssistantAgent,MessageFilterAgent,MessageFilterConfig,PerSourceFilter
from database import store_data, query_db
from tools import search_web
from formatting_tools import format_web_data


def create_team(llm_client: OpenAIChatCompletionClient):
    """
    Build the agent team for Industry Monitoring System.
    The workflow:
    QueryAgent -> SearchAgent -> FormattingAgent -> DataProcessingAgent -> ResponseAgent -> FormattingAgentFinal -> Terminate
    """

    # ---------- Agents ----------

    query_agent = AssistantAgent(
        name="QueryAgent",
        model_client=llm_client,
        system_message=(
            "You interpret user queries, extract key entities and intent, "
            "and delegate tasks to the SearchAgent."
        )
    )

    search_agent = AssistantAgent(
        name="SearchAgent",
        model_client=llm_client,
        system_message=(
            "You perform web searches using the Tavily API and gather relevant raw data. "
            "Pass unprocessed results to FormattingAgent for structuring."
        ),
        tools=[search_web]
    )

    # formatting_agent = AssistantAgent(
    #     name="FormattingAgent",
    #     model_client=llm_client,
    #     system_message=(
    #         "You are responsible for formatting and structuring data extracted from web searches. "
    #         "Tasks:\n"
    #         "1. Clean and organize raw web data into structured formats\n"
    #         "2. Extract key information (company names, industries, financials, news highlights)\n"
    #         "3. Format data into consistent JSON structures\n"
    #         "4. Remove duplicates and irrelevant info\n"
    #         "5. Standardize company names and industries\n"
    #         "6. Create summaries and key insights\n"
    #         "7. Ensure data quality before passing to DataProcessingAgent"
    #     ),
    #     tools=[format_web_data]
    # )

    data_processing_agent = AssistantAgent(
        name="DataProcessingAgent",
        model_client=llm_client,
        system_message=(
            "You process structured data from SearchAgent and prepare it for storage in PostgreSQL. "
            "Store the clean data with proper metadata. as company , industry, data"
        ),
        tools=[store_data]
    )

    response_agent = AssistantAgent(
        name="ResponseAgent",
        model_client=llm_client,
        system_message=(
            "You generate concise, accurate, and professional responses. "
            "Query the database when needed and present clear analysis, "
            "avoiding raw JSON or code outputs."
        ),
        tools=[query_db]
    )

    formatting_agent_final = AssistantAgent(
        name="FormattingAgentFinal",
        model_client=llm_client,
        system_message=(
            "You are responsible for converting structured or raw data into a clear, user-friendly answer. "
            "Tasks:\n"
            "1. Analyze and compare extracted data\n"
            "2. Present comparisons in tables if useful\n"
            "3. Provide clear text explanations, not JSON/YAML\n"
            "4. Extract insights: trends, rankings, competitive differences\n"
            "5. Provide a final verdict answering the user query professionally"
        )
    )

    terminate_agent = AssistantAgent(
        name="Terminate",
        model_client=llm_client,
        system_message="Just Say Goodbye nothing else"
    )

    FilterTerminateAgent=MessageFilterAgent(
    name="TerminateAgent",
    wrapped_agent=terminate_agent,
    filter=MessageFilterConfig(per_source=[PerSourceFilter(source="FormattingAgentFinal",position="last",count=0)])
)

    # ---------- Graph Workflow ----------

    builder = DiGraphBuilder()
    builder.add_node(query_agent)
    builder.add_node(search_agent)
    # builder.add_node(formatting_agent)
    builder.add_node(data_processing_agent)
    builder.add_node(response_agent)
    builder.add_node(formatting_agent_final)
    builder.add_node(FilterTerminateAgent)

    # Define edges
    builder.add_edge(query_agent, search_agent)
    builder.add_edge(search_agent,data_processing_agent)
    # builder.add_edge(search_agent, formatting_agent)
    # builder.add_edge(formatting_agent, data_processing_agent)
    builder.add_edge(data_processing_agent, response_agent)
    builder.add_edge(response_agent, formatting_agent_final)
    builder.add_edge(formatting_agent_final, FilterTerminateAgent)

    # Build graph
    graph = builder.build()

    # Create async GraphFlow with termination condition
    team = GraphFlow(
        participants=builder.get_participants(),
        graph=graph,
        termination_condition=TextMentionTermination("Goodbye")
    )

    return team