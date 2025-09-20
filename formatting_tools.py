"""
Formatting utilities for structuring and cleaning web-scraped data
"""
import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime


async def format_company_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format raw company data from web scraping into structured format
    
    Args:
        raw_data: Raw data from web search results
        
    Returns:
        Structured company data dictionary
    """
    formatted_data = {
        "company_info": {},
        "key_metrics": {},
        "recent_news": [],
        "financial_highlights": {},
        "market_position": {},
        "summary": "",
        "data_quality": {
            "completeness": 0.0,
            "last_updated": datetime.now().isoformat(),
            "sources": []
        }
    }
    
    # Extract company information
    if isinstance(raw_data, dict) and "results" in raw_data:
        results = raw_data["results"]
        
        for result in results:
            # Extract company name and industry
            title = result.get("title", "")
            content = result.get("content", "")
            url = result.get("url", "")
            
            # Add source tracking
            formatted_data["data_quality"]["sources"].append({
                "url": url,
                "title": title,
                "scraped_at": datetime.now().isoformat()
            })
            
            # Extract company info from title and content
            company_name = extract_company_name(title, content)
            if company_name and not formatted_data["company_info"].get("name"):
                formatted_data["company_info"]["name"] = company_name
            
            # Extract industry information
            industry = extract_industry(title, content)
            if industry and not formatted_data["company_info"].get("industry"):
                formatted_data["company_info"]["industry"] = industry
            
            # Extract key metrics
            metrics = extract_metrics(content)
            formatted_data["key_metrics"].update(metrics)
            
            # Extract news items
            news_item = extract_news_item(title, content, url)
            if news_item:
                formatted_data["recent_news"].append(news_item)
            
            # Extract financial data
            financial_data = extract_financial_data(content)
            formatted_data["financial_highlights"].update(financial_data)
    
    # Generate summary
    formatted_data["summary"] = generate_summary(formatted_data)
    
    # Calculate data quality score
    formatted_data["data_quality"]["completeness"] = calculate_completeness(formatted_data)
    
    return formatted_data


def extract_company_name(title: str, content: str) -> Optional[str]:
    """Extract company name from title and content"""
    # Common patterns for company names
    patterns = [
        r'([A-Z][a-zA-Z\s&]+(?:Inc|Corp|LLC|Ltd|Co|Company|Corporation)\.?)',
        r'([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*)\s*(?:stock|shares|announces|reports)',
        r'([A-Z][a-zA-Z\s]+)\s*(?:\([\w]+\))'  # Company (TICKER)
    ]
    
    text = f"{title} {content}"
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            return clean_company_name(matches[0])
    
    return None


def extract_industry(title: str, content: str) -> Optional[str]:
    """Extract industry information"""
    industry_keywords = {
        "technology": ["tech", "software", "AI", "artificial intelligence", "cloud", "SaaS"],
        "healthcare": ["healthcare", "pharmaceutical", "biotech", "medical", "drug"],
        "finance": ["bank", "financial", "fintech", "investment", "insurance"],
        "energy": ["energy", "oil", "gas", "renewable", "solar", "wind"],
        "retail": ["retail", "e-commerce", "shopping", "consumer goods"],
        "automotive": ["automotive", "car", "vehicle", "electric vehicle", "EV"],
        "real estate": ["real estate", "property", "REIT", "construction"],
        "telecommunications": ["telecom", "wireless", "5G", "network"]
    }
    
    text = f"{title} {content}".lower()
    
    for industry, keywords in industry_keywords.items():
        if any(keyword in text for keyword in keywords):
            return industry.title()
    
    return None


def extract_metrics(content: str) -> Dict[str, Any]:
    """Extract key business metrics from content"""
    metrics = {}
    
    # Revenue patterns
    revenue_patterns = [
        r'revenue.*?\$([0-9,.]+ (?:billion|million|B|M))',
        r'\$([0-9,.]+ (?:billion|million|B|M)).*?revenue'
    ]
    
    for pattern in revenue_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            metrics["revenue"] = match.group(1)
            break
    
    # Employee count
    employee_patterns = [
        r'([0-9,]+)\s*employees',
        r'workforce.*?([0-9,]+)',
        r'employs.*?([0-9,]+)'
    ]
    
    for pattern in employee_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            metrics["employees"] = match.group(1).replace(',', '')
            break
    
    # Market cap
    market_cap_patterns = [
        r'market cap.*?\$([0-9,.]+ (?:billion|million|B|M))',
        r'valuation.*?\$([0-9,.]+ (?:billion|million|B|M))'
    ]
    
    for pattern in market_cap_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            metrics["market_cap"] = match.group(1)
            break
    
    return metrics


def extract_news_item(title: str, content: str, url: str) -> Optional[Dict[str, str]]:
    """Extract news item information"""
    if not title or not content:
        return None
    
    return {
        "headline": title.strip(),
        "summary": content[:200] + "..." if len(content) > 200 else content,
        "url": url,
        "extracted_at": datetime.now().isoformat()
    }


def extract_financial_data(content: str) -> Dict[str, Any]:
    """Extract financial highlights from content"""
    financial_data = {}
    
    # Stock price patterns
    price_patterns = [
        r'stock price.*?\$([0-9,.]+)',
        r'trading at.*?\$([0-9,.]+)',
        r'shares.*?\$([0-9,.]+)'
    ]
    
    for pattern in price_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            financial_data["stock_price"] = f"${match.group(1)}"
            break
    
    # Profit/earnings patterns
    profit_patterns = [
        r'profit.*?\$([0-9,.]+ (?:billion|million|B|M))',
        r'earnings.*?\$([0-9,.]+ (?:billion|million|B|M))',
        r'net income.*?\$([0-9,.]+ (?:billion|million|B|M))'
    ]
    
    for pattern in profit_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            financial_data["profit"] = match.group(1)
            break
    
    return financial_data


def clean_company_name(name: str) -> str:
    """Clean and standardize company name"""
    # Remove extra whitespace
    name = re.sub(r'\s+', ' ', name.strip())
    
    # Standardize corporate suffixes
    suffixes = {
        "Inc.": "Inc",
        "Corp.": "Corp",
        "Co.": "Co",
        "Ltd.": "Ltd"
    }
    
    for old_suffix, new_suffix in suffixes.items():
        name = name.replace(old_suffix, new_suffix)
    
    return name


def generate_summary(data: Dict[str, Any]) -> str:
    """Generate executive summary from formatted data"""
    company_name = data.get("company_info", {}).get("name", "Unknown Company")
    industry = data.get("company_info", {}).get("industry", "Unknown Industry")
    
    summary_parts = [f"{company_name} operates in the {industry} sector."]
    
    # Add key metrics to summary
    metrics = data.get("key_metrics", {})
    if metrics.get("revenue"):
        summary_parts.append(f"The company reports revenue of {metrics['revenue']}.")
    
    if metrics.get("employees"):
        summary_parts.append(f"It employs approximately {metrics['employees']} people.")
    
    # Add recent news context
    news_count = len(data.get("recent_news", []))
    if news_count > 0:
        summary_parts.append(f"Recent news coverage includes {news_count} relevant articles.")
    
    return " ".join(summary_parts)


def calculate_completeness(data: Dict[str, Any]) -> float:
    """Calculate data completeness score (0-1)"""
    total_fields = 8  # Total important fields to check
    filled_fields = 0
    
    # Check company info
    company_info = data.get("company_info", {})
    if company_info.get("name"):
        filled_fields += 1
    if company_info.get("industry"):
        filled_fields += 1
    
    # Check metrics
    metrics = data.get("key_metrics", {})
    if metrics.get("revenue"):
        filled_fields += 1
    if metrics.get("employees"):
        filled_fields += 1
    
    # Check financial data
    financial = data.get("financial_highlights", {})
    if financial.get("stock_price"):
        filled_fields += 1
    if financial.get("profit"):
        filled_fields += 1
    
    # Check news
    if data.get("recent_news"):
        filled_fields += 1
    
    # Check summary
    if data.get("summary"):
        filled_fields += 1
    
    return filled_fields / total_fields


# Tool function for the formatting agent
async def format_web_data(raw_data: str) -> dict:
    """
    Tool function for formatting raw web data
    This function can be used by the FormattingAgent
    """
    try:
        # Parse raw data if it's a JSON string
        if isinstance(raw_data, str):
            try:
                data = json.loads(raw_data)
            except json.JSONDecodeError:
                # If not JSON, treat as plain text and create a simple structure
                data = {"results": [{"title": "Raw Data", "content": raw_data, "url": ""}]}
        else:
            data = raw_data
        
        # Format the data
        formatted_result = await format_company_data(data)
        return formatted_result
        
    except Exception as e:
        return {
            "error": f"Failed to format data: {str(e)}",
            "raw_data": raw_data,
            "timestamp": datetime.now().isoformat()
        }
