# Fleet Industry Monitoring Application (Async Version)

## ✅ Status: FULLY FUNCTIONAL

This application has been successfully converted to use async/await patterns and includes a sophisticated formatting agent for better data presentation. All components have been verified and are working correctly.

## 🚀 Quick Start

1. **Verify everything is working:**
```bash
python3 verify_app.py
```

2. **Run the application:**
```bash
# Console mode (interactive)
python3 main.py

# Web application
python3 run_app.py web
# Then visit: http://localhost:8000/dashboard.html
```

## 📋 Requirements

- Python 3.8+
- Internet connection (for web search)
- Required packages (automatically managed)

## 🔧 Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Verify installation:**
```bash
python3 verify_app.py
```

3. **Start using the application!**

## 🎯 Key Features

### ✨ Complete Async Architecture
- **Database Operations**: Async SQLAlchemy with SQLite (easy setup)
- **Web Search**: Async Tavily API integration
- **Agent Communication**: Async AutoGen agent workflows
- **Web API**: FastAPI with async endpoints

### 🤖 Advanced Agent System
- **QueryAgent**: Interprets user queries and delegates tasks
- **SearchAgent**: Performs async web searches using Tavily API
- **FormattingAgent**: Cleans, structures, and formats raw web data
- **DataProcessingAgent**: Processes formatted data for storage
- **ResponseAgent**: Generates well-formatted responses

### 📊 Intelligent Data Formatting
The FormattingAgent provides:
- **Data Cleaning**: Removes duplicates and irrelevant information
- **Structure Standardization**: Converts raw web data into consistent JSON
- **Entity Extraction**: Identifies companies, industries, financial metrics
- **Quality Assessment**: Calculates completeness scores and tracks sources
- **Smart Summarization**: Generates executive summaries

### 🎨 Modern Web Dashboard
- **Responsive Design**: Works on desktop and mobile
- **Real-time Search**: Live search with loading indicators
- **Structured Display**: Organized presentation of company data
- **Error Handling**: Graceful error messages and fallbacks

## 📁 Project Structure

```
fleet/
├── main.py                 # Console application entry point
├── app.py                  # FastAPI web application
├── agents.py               # Agent definitions and workflows
├── database.py             # Async database operations
├── tools.py                # Web search tools
├── formatting_tools.py     # Data formatting utilities
├── config.py               # Configuration settings
├── dashboard.html          # Web dashboard interface
├── run_app.py              # Unified application launcher
├── verify_app.py           # Complete verification script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔄 Agent Workflow

```
User Query → QueryAgent → SearchAgent → FormattingAgent → DataProcessingAgent → ResponseAgent → Formatted Response
```

1. **QueryAgent** interprets the user's request
2. **SearchAgent** searches the web for relevant information
3. **FormattingAgent** cleans and structures the raw data
4. **DataProcessingAgent** stores the formatted data in the database
5. **ResponseAgent** generates a comprehensive response

## 📊 Formatted Data Structure

```json
{
  "company_info": {
    "name": "Company Name",
    "industry": "Industry Category",
    "description": "Company description"
  },
  "key_metrics": {
    "revenue": "Revenue information",
    "employees": "Employee count",
    "market_cap": "Market capitalization"
  },
  "recent_news": [
    {
      "headline": "News headline",
      "summary": "News summary",
      "url": "Source URL",
      "extracted_at": "Timestamp"
    }
  ],
  "financial_highlights": {
    "stock_price": "Current stock price",
    "profit": "Profit information"
  },
  "summary": "Executive summary of all data",
  "data_quality": {
    "completeness": 0.85,
    "last_updated": "2025-09-11T10:30:00",
    "sources": ["List of data sources"]
  }
}
```

## 🌐 API Endpoints

- `GET /`: Root endpoint with status
- `GET /query/{query}`: Search for companies/industries
- `GET /health`: Health check endpoint
- `Static`: `/dashboard.html` - Web dashboard

## ⚙️ Configuration

Edit `config.py` to customize settings:

```python
class Config:
    OPENAI_API_KEY = "your-openai-api-key"      # Optional (for GPT models)
    TAVILY_API_KEY = "your-tavily-api-key"      # Required for web search
    DB_NAME = "industry_monitoring"              # SQLite database name
    DB_USER = "user"                            # Not used in SQLite mode
    DB_PASSWORD = "password"                    # Not used in SQLite mode
    DB_HOST = "localhost"                       # Not used in SQLite mode
    DB_PORT = "5432"                           # Not used in SQLite mode
```

## 🗄️ Database

The application uses **SQLite** by default for easy setup:
- **File**: `industry_monitoring.db` (created automatically)
- **Schema**: Companies table with name, industry, JSON data, timestamps
- **Async Operations**: All database operations are fully async

## 🧪 Testing & Verification

### Quick Test
```bash
python3 verify_app.py
```

### Component Tests
```bash
python3 test_db.py      # Test database functionality
python3 test_agents.py  # Test agent components
```

## 🚀 Running the Application

### Console Mode
```bash
python3 main.py
```
Interactive console where you can type queries and see agent responses.

### Web Mode
```bash
python3 run_app.py web
```
Starts the web server. Access the dashboard at `http://localhost:8000/dashboard.html`

### Direct Web Server
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## 🛠️ Troubleshooting

### All components verified ✅
If you ran `python3 verify_app.py` and all tests passed, the application is ready to use!

### Common Issues (if any)

| Issue | Solution |
|-------|----------|
| Import errors | Run `pip install -r requirements.txt` |
| Database errors | Check that SQLite is available (usually built-in) |
| Web search fails | Verify Tavily API key in config.py |
| Agent errors | Ensure all dependencies are installed |

## 📦 Dependencies

All required packages are automatically installed:

- `autogen-agentchat` - Multi-agent chat framework
- `tavily-python` - Web search API
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy[asyncio]` - Async database ORM
- `aiosqlite` - Async SQLite driver
- `autogen-ext[openai]` - OpenAI integration
- `httpx` - Async HTTP client
- `aiofiles` - Async file operations
- `python-dateutil` - Date parsing
- `regex` - Advanced regex patterns

## 🎉 Success!

Your Fleet Industry Monitoring Application is now:
- ✅ Fully async
- ✅ Complete with formatting agent
- ✅ Database verified
- ✅ Web interface ready
- ✅ All components tested

Start exploring companies and industries with intelligent data formatting!
