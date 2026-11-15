import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from tavily import TavilyClient

# Setup LLM (Keys are hardcoded here for local testing)
llm = ChatGroq(
    model="openai/gpt-oss-20b", 
    temperature=0.1,
    api_key="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"  
)

# Setup Tavily (Keys are hardcoded here for local testing)
tavily = TavilyClient("tvly-30mVFt-hveqtztjEu5RsqqOOIHzBeqYQsMcfQ9Po2lO1JGF3z")  #def search_web(query: str) -> str:
    """Search the web using Tavily."""
    try:
        response = tavily.search(query=query, search_depth="advanced", max_results=5)
        results = response.get("results", [])
        if not results:
            return "No results found."
        
        formatted = ""
        for i, res in enumerate(results, 1):
            formatted += f"{i}. {res.get('title', '')}: {res.get('content', '')} (URL: {res.get('url', '')})\n"
        return formatted
    except Exception as e:
        return f"Search failed: {e}"

async def run_procurement(query: str):
    print(f"🔍 Starting research for: {query}")
    
    # 1. Researcher Agent: Search the web
    search_results = search_web(f"best {query} buy online price specifications 2024")
    print("✅ Search completed.")
    
    # 2. Analyst Agent: Analyze and Compare
    print("🧠 Analyzing results...")
    analyst_prompt = f"""
    You are a Senior Procurement Analyst.
    A user requested: "{query}"
    
    Here are the search results:
    {search_results}
    
    Based on these results, identify the top 3 products that match the request. 
    Compare their prices, specs, and features. Provide a clear recommendation.
    
    Do not invent prices or specifications if they are not available in the search results.
    """
    
    analysis = llm.invoke([
        SystemMessage(content="You are a helpful procurement expert."),
        HumanMessage(content=analyst_prompt)
    ])
    print("✅ Analysis completed.")
    
    # 3. Reporter Agent: Generate HTML Report
    print("📝 Generating HTML Report...")
    reporter_prompt = f"""
    You are an expert technical writer.
    Create a professional, modern HTML report based on this analysis.
    
    Analysis:
    {analysis.content}
    
    The HTML should include:
    - A title: Procurement Recommendation Report
    - A summary of the request
    - A comparison table of the top 3 products
    - Product prices and specifications
    - Advantages and disadvantages
    - A final recommendation section
    
    Use inline CSS for styling. Make the report clean, professional, and readable.
    ONLY return the HTML code. Do not include markdown blocks like ```html.
    """
    
    report = llm.invoke([
        SystemMessage(content="You are an expert HTML report writer."),
        HumanMessage(content=reporter_prompt)
    ])
    
    # Clean the output in case the LLM adds markdown blocks
    html_result = report.content.replace("```html", "").replace("```", "").strip()
    
    print("✅ Report generated successfully!")
    return html_result
