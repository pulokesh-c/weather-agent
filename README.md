# 🌦️ Weather Agent
## 🌐 Live Demo

🚀 **[Try the Weather Agent](https://pulokesh-weather-agent.streamlit.app/)**

An AI-powered weather assistant built using **LangChain, Google Gemini, and Streamlit**.

The application uses an LLM agent with multiple tools to understand natural-language queries, decide which tools to use, execute them, and generate a final response.

---

## 🚀 Features

- 🌡️ Check today's minimum and maximum temperature
- 🌧️ Check today's probability of rain
- 💧 Check current humidity
- 💨 Check wind conditions
- 🧮 Perform mathematical calculations
- 🔗 Chain multiple tools together automatically
- 🤖 AI agent decides which tool(s) to use
- 🧠 Supports multi-step reasoning
- 🔍 View how the agent solved a query

---

## 💬 Example

### User

> Get today's maximum temperature in Kolkata and convert it to Fahrenheit.

The agent automatically performs:

```text
User Question
      ↓
Temperature Tool
      ↓
Extract Maximum Temperature
      ↓
Calculator Tool
      ↓
Final Natural Language Response
🏗️ Architecture
                ┌─────────────────┐
                │      User       │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Streamlit UI  │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ LangChain Agent │
                │                 │
                │   Gemini LLM    │
                └────────┬────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
   Temperature Tool   Rain Tool    Calculator Tool
          │              │              │
          └──────────────┼──────────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Open-Meteo APIs │
                └─────────────────┘
🛠️ Tech Stack
Python
LangChain
Google Gemini
Streamlit
Open-Meteo API
Requests
python-dotenv
📂 Project Structure
weather-agent/
│
├── agent.py
│   └── LangChain agent configuration
│
├── tools.py
│   └── Weather and calculator tools
│
├── app.py
│   └── Streamlit user interface
│
├── assets/
│   └── weather_background.png
│
├── requirements.txt
│
├── .gitignore
│
└── README.md
⚙️ How It Works

The agent receives a natural-language question and decides whether it needs to use one or more tools.

For example:

What is the maximum temperature in Kolkata
and convert it to Fahrenheit?

The execution flow becomes:

1. User sends a question

        ↓

2. LangChain Agent analyzes the request

        ↓

3. Agent selects:

   temperature_check(location="Kolkata")

        ↓

4. Tool returns:

   Maximum temperature: 31.6°C

        ↓

5. Agent decides another calculation is required

        ↓

6. Agent selects:

   calculator(expression="(31.6 * 9/5) + 32")

        ↓

7. Calculator returns:

   88.88°F

        ↓

8. Gemini generates a natural-language response

This demonstrates multi-tool orchestration, where the output of one tool becomes context for the next tool call.

🧠 Agent Capabilities

The agent can decide dynamically which tools are required.

Example 1: Single Tool

Question:

What is the temperature in Kolkata today?

Agent flow:

User
  ↓
Gemini LLM
  ↓
Temperature Tool
  ↓
Final Response
Example 2: Multiple Tools

Question:

Will it rain in Kolkata and what is the temperature?

Agent flow:

User
  ↓
Gemini LLM
  ↓
├── Temperature Tool
│
└── Rain Tool
        ↓
Final Response
Example 3: Sequential Tool Calling

Question:

Get today's maximum temperature in Kolkata
and convert it to Fahrenheit.

Agent flow:

User
  ↓
Temperature Tool
  ↓
30.7°C
  ↓
Calculator Tool
  ↓
87.26°F
  ↓
Final Answer

The agent determines that the second tool requires information returned by the first tool.

▶️ Run Locally
1. Clone the repository
git clone https://github.com/pulokesh-c/weather-agent.git
cd weather-agent
2. Create a virtual environment
python3 -m venv .venv
3. Activate the virtual environment
macOS / Linux
source .venv/bin/activate
Windows
.venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt
5. Add your Gemini API key

Create a .env file in the project root:

GOOGLE_API_KEY=your_api_key_here

⚠️ Never commit your API key to GitHub.

6. Run the application
streamlit run app.py

The application will open in your browser.

🔑 Environment Variables

Create a .env file:

GOOGLE_API_KEY=your_gemini_api_key

The .env file is excluded from Git using .gitignore.

🎯 Concepts Demonstrated

This project demonstrates practical implementation of:

LLM Tool Calling
LangChain Tools
AI Agents
Agent Execution Loops
Multi-Step Agent Reasoning
Multi-Tool Orchestration
Sequential Tool Calling
Tool Result → Next Tool Input
Dynamic Tool Selection
Conversation Message Flow
External API Integration
Streamlit Application Development
Environment Variable Management
🔮 Future Improvements

Possible future enhancements include:

📅 Multi-day weather forecasts
⚠️ Weather alerts
📍 Location autocomplete
💬 Persistent chat history
🌍 More weather data sources
📊 Weather visualizations
🧠 Memory for previous conversations
🔄 Streaming agent responses
🕸️ LangGraph implementation for more advanced agent workflows
👨‍💻 Author

Pulokesh Chatterjee

Data Scientist | AI & Generative AI Enthusiast

⭐ If you found this project interesting, feel free to star the repository!