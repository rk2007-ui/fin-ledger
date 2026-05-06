import streamlit as st
import google.generativeai as genai
import json
import math

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fin Ledger · AI Financial Advisor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --gold:    #C9A84C;
    --gold-lt: #E8C97A;
    --dark:    #0A0E17;
    --card:    #111827;
    --border:  #1F2937;
    --muted:   #6B7280;
    --white:   #F9FAFB;
    --green:   #10B981;
    --red:     #EF4444;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--dark);
    color: var(--white);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--card);
    border-right: 1px solid var(--border);
    padding-top: 2rem;
}
section[data-testid="stSidebar"] * { color: var(--white) !important; }

/* Hide default streamlit header */
header[data-testid="stHeader"] { display: none; }
#MainMenu, footer { display: none; }

/* Main area */
.main .block-container { padding: 2rem 2.5rem; max-width: 900px; }

/* Logo */
.logo-wrap {
    text-align: center;
    padding: 1.5rem 0 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.logo-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: var(--gold);
    letter-spacing: -0.5px;
    margin: 0;
}
.logo-sub {
    font-size: 0.75rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 4px;
}

/* Stat cards */
.stat-row { display: flex; gap: 12px; margin-bottom: 1.5rem; }
.stat-card {
    flex: 1;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.stat-label { font-size: 0.68rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1.5px; }
.stat-value { font-size: 1.4rem; font-weight: 600; color: var(--gold); margin-top: 4px; }

/* Chat messages */
.msg-user {
    display: flex;
    justify-content: flex-end;
    margin: 0.8rem 0;
}
.msg-bot {
    display: flex;
    justify-content: flex-start;
    margin: 0.8rem 0;
}
.bubble-user {
    background: var(--gold);
    color: #111;
    border-radius: 18px 18px 4px 18px;
    padding: 0.75rem 1.1rem;
    max-width: 72%;
    font-size: 0.92rem;
    line-height: 1.5;
}
.bubble-bot {
    background: var(--card);
    border: 1px solid var(--border);
    color: var(--white);
    border-radius: 18px 18px 18px 4px;
    padding: 0.75rem 1.1rem;
    max-width: 78%;
    font-size: 0.92rem;
    line-height: 1.6;
}
.bot-avatar {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, var(--gold), var(--gold-lt));
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem;
    margin-right: 8px;
    flex-shrink: 0;
}

/* Tool result card */
.tool-card {
    background: #0D1117;
    border: 1px solid var(--gold);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-top: 0.5rem;
    font-size: 0.85rem;
}
.tool-title {
    font-size: 0.7rem;
    color: var(--gold);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 0.6rem;
    font-weight: 600;
}
.tool-row { display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid var(--border); }
.tool-row:last-child { border-bottom: none; }
.tool-key { color: var(--muted); }
.tool-val { color: var(--green); font-weight: 500; }

/* Input */
.stTextInput > div > div > input {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--white) !important;
    padding: 0.75rem 1rem !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.15) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--gold), var(--gold-lt)) !important;
    color: #111 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.5rem 1.5rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* Section label */
.section-label {
    font-size: 0.68rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

/* Disclaimer */
.disclaimer {
    font-size: 0.72rem;
    color: var(--muted);
    background: var(--card);
    border-left: 3px solid var(--gold);
    padding: 0.5rem 0.8rem;
    border-radius: 0 6px 6px 0;
    margin-top: 1rem;
}

/* Welcome card */
.welcome-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
}
.welcome-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.8rem;
    color: var(--gold);
    margin-bottom: 0.5rem;
}
.welcome-sub { color: var(--muted); font-size: 0.9rem; line-height: 1.6; }

/* Suggestion chips */
.chip-row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 1rem; justify-content: center; }
.chip {
    background: #1F2937;
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 0.8rem;
    color: var(--white);
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)


# ── Financial Tool Functions ──────────────────────────────────────────────────
def calculate_budget(monthly_income: float, monthly_expenses: float, savings_goal: float = 0):
    surplus = monthly_income - monthly_expenses
    savings_rate = (surplus / monthly_income * 100) if monthly_income > 0 else 0
    needs = monthly_income * 0.50
    wants = monthly_income * 0.30
    savings_ideal = monthly_income * 0.20
    return {
        "monthly_income": f"${monthly_income:,.0f}",
        "monthly_expenses": f"${monthly_expenses:,.0f}",
        "monthly_surplus": f"${surplus:,.0f}",
        "savings_rate": f"{savings_rate:.1f}%",
        "50_needs_budget": f"${needs:,.0f}",
        "30_wants_budget": f"${wants:,.0f}",
        "20_savings_ideal": f"${savings_ideal:,.0f}",
        "savings_goal_met": "✅ Yes" if surplus >= savings_goal else f"❌ Short by ${savings_goal - surplus:,.0f}",
        "status": "✅ Surplus" if surplus > 0 else "🔴 Deficit"
    }

def debt_payoff_calculator(debt_amount: float, interest_rate: float, monthly_payment: float):
    monthly_rate = interest_rate / 100 / 12
    if monthly_payment <= debt_amount * monthly_rate:
        return {"error": "Monthly payment too low to cover interest. Please increase payment."}
    if monthly_rate == 0:
        months = math.ceil(debt_amount / monthly_payment)
    else:
        months = math.ceil(
            -math.log(1 - (debt_amount * monthly_rate) / monthly_payment) / math.log(1 + monthly_rate)
        )
    total_paid = monthly_payment * months
    total_interest = total_paid - debt_amount
    years = months // 12
    remaining_months = months % 12
    timeline = f"{years}y {remaining_months}m" if years > 0 else f"{months} months"
    return {
        "debt_amount": f"${debt_amount:,.0f}",
        "interest_rate": f"{interest_rate}%",
        "monthly_payment": f"${monthly_payment:,.0f}",
        "payoff_timeline": timeline,
        "total_paid": f"${total_paid:,.0f}",
        "total_interest": f"${total_interest:,.0f}",
        "interest_percentage": f"{(total_interest/debt_amount*100):.1f}% of principal"
    }

def savings_goal_tracker(goal_amount: float, current_savings: float, monthly_contribution: float):
    remaining = goal_amount - current_savings
    if monthly_contribution <= 0:
        return {"error": "Monthly contribution must be greater than 0"}
    months = math.ceil(remaining / monthly_contribution)
    years = months // 12
    rem_months = months % 12
    timeline = f"{years}y {rem_months}m" if years > 0 else f"{months} months"
    progress_pct = (current_savings / goal_amount * 100) if goal_amount > 0 else 0
    return {
        "goal_amount": f"${goal_amount:,.0f}",
        "current_savings": f"${current_savings:,.0f}",
        "remaining_amount": f"${remaining:,.0f}",
        "monthly_contribution": f"${monthly_contribution:,.0f}",
        "time_to_goal": timeline,
        "progress": f"{progress_pct:.1f}% complete",
        "total_months": str(months)
    }

def investment_advisor(monthly_surplus: float, risk_level: str, investment_goal: str):
    strategies = {
        "low": {
            "allocation": "80% Bonds / 15% Index Funds / 5% Cash",
            "instruments": "PPF, Fixed Deposits, Government Bonds, Debt Mutual Funds",
            "expected_return": "5–7% annually",
            "risk_note": "Capital preservation focused"
        },
        "medium": {
            "allocation": "50% Equity / 40% Bonds / 10% Gold",
            "instruments": "Index Funds (Nifty 50), Balanced Mutual Funds, REITs",
            "expected_return": "10–14% annually",
            "risk_note": "Balanced growth and stability"
        },
        "high": {
            "allocation": "80% Equity / 10% Bonds / 10% Alternative",
            "instruments": "Direct Stocks, Small-cap Funds, ETFs, Sectoral Funds",
            "expected_return": "15–20% annually (with higher risk)",
            "risk_note": "Growth focused, volatility expected"
        }
    }
    s = strategies.get(risk_level.lower(), strategies["medium"])
    annual_invested = monthly_surplus * 12
    projected_10y = annual_invested * 10 * 1.12
    return {
        "monthly_to_invest": f"${monthly_surplus:,.0f}",
        "investment_goal": investment_goal,
        "risk_level": risk_level.upper(),
        "recommended_allocation": s["allocation"],
        "instruments": s["instruments"],
        "expected_return": s["expected_return"],
        "risk_note": s["risk_note"],
        "10yr_projection": f"${projected_10y:,.0f} (estimated)",
        "disclaimer": "⚠️ Consult a CFP for personalized advice"
    }

TOOLS = {
    "calculate_budget": calculate_budget,
    "debt_payoff_calculator": debt_payoff_calculator,
    "savings_goal_tracker": savings_goal_tracker,
    "investment_advisor": investment_advisor,
}

TOOL_SCHEMAS = [
    {
        "name": "calculate_budget",
        "description": "Calculates monthly budget breakdown based on income and expenses. Use when user shares income and spending details.",
        "parameters": {
            "type": "object",
            "properties": {
                "monthly_income": {"type": "number", "description": "User's total monthly income"},
                "monthly_expenses": {"type": "number", "description": "User's total monthly expenses"},
                "savings_goal": {"type": "number", "description": "Optional monthly savings target"}
            },
            "required": ["monthly_income", "monthly_expenses"]
        }
    },
    {
        "name": "debt_payoff_calculator",
        "description": "Calculates debt payoff timeline and total interest. Use when user mentions loans, credit card debt, or EMI.",
        "parameters": {
            "type": "object",
            "properties": {
                "debt_amount": {"type": "number", "description": "Total debt amount"},
                "interest_rate": {"type": "number", "description": "Annual interest rate in %"},
                "monthly_payment": {"type": "number", "description": "Monthly payment amount"}
            },
            "required": ["debt_amount", "interest_rate", "monthly_payment"]
        }
    },
    {
        "name": "savings_goal_tracker",
        "description": "Tracks progress toward a savings goal and calculates timeline. Use when user mentions saving for something specific.",
        "parameters": {
            "type": "object",
            "properties": {
                "goal_amount": {"type": "number", "description": "Total savings target"},
                "current_savings": {"type": "number", "description": "Amount already saved"},
                "monthly_contribution": {"type": "number", "description": "Monthly savings amount"}
            },
            "required": ["goal_amount", "current_savings", "monthly_contribution"]
        }
    },
    {
        "name": "investment_advisor",
        "description": "Gives general investment advice based on risk appetite. Use when user asks about investing.",
        "parameters": {
            "type": "object",
            "properties": {
                "monthly_surplus": {"type": "number", "description": "Money available to invest monthly"},
                "risk_level": {"type": "string", "enum": ["low", "medium", "high"]},
                "investment_goal": {"type": "string", "description": "Investment objective e.g. retirement, house"}
            },
            "required": ["monthly_surplus", "risk_level", "investment_goal"]
        }
    }
]

SYSTEM_PROMPT = """You are Fin Ledger, a warm and knowledgeable AI financial advisor.

Your capabilities:
- Analyze income, expenses, and budgets
- Calculate debt payoff timelines
- Track savings goals
- Provide general investment guidance

Rules:
- Always use the available tools when the user provides financial numbers
- Never give personalized investment advice requiring a license
- Always recommend consulting a CFP for major financial decisions
- Be clear, concise, and encouraging
- Format numbers clearly with $ signs
- After using a tool, explain the results in plain, friendly English
- Keep responses focused and practical"""


# ── Gemini Setup ──────────────────────────────────────────────────────────────
def get_gemini_client(api_key: str):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=SYSTEM_PROMPT,
        tools=TOOL_SCHEMAS
    )

def render_tool_card(tool_name: str, result: dict):
    display_name = tool_name.replace("_", " ").title()
    rows = "".join(
        f'<div class="tool-row"><span class="tool-key">{k.replace("_"," ").title()}</span>'
        f'<span class="tool-val">{v}</span></div>'
        for k, v in result.items()
    )
    return f"""
    <div class="tool-card">
        <div class="tool-title">📊 {display_name} Results</div>
        {rows}
    </div>"""

def chat_with_fin_ledger(client, user_message: str, history: list):
    messages = []
    for h in history:
        messages.append({"role": h["role"], "parts": [h["content"]]})

    chat = client.start_chat(history=messages)
    response = chat.send_message(user_message)

    tool_results_html = ""
    final_text = ""

    # Handle tool calls
    for part in response.parts:
        if hasattr(part, "function_call") and part.function_call.name:
            fn = part.function_call
            tool_name = fn.name
            args = dict(fn.args)

            if tool_name in TOOLS:
                result = TOOLS[tool_name](**args)
                tool_results_html += render_tool_card(tool_name, result)

                # Send tool result back
                tool_response = chat.send_message(
                    genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=tool_name,
                            response={"result": result}
                        )
                    )
                )
                for p in tool_response.parts:
                    if hasattr(p, "text") and p.text:
                        final_text += p.text
        elif hasattr(part, "text") and part.text:
            final_text += part.text

    return final_text.strip(), tool_results_html


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="logo-wrap">
        <div class="logo-title">💰 Fin Ledger</div>
        <div class="logo-sub">AI Financial Advisor</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Configuration</div>', unsafe_allow_html=True)
    api_key = st.text_input("Gemini API Key", type="password", placeholder="AIzaSy...")

    st.markdown("---")
    st.markdown('<div class="section-label">Quick Tools</div>', unsafe_allow_html=True)

    suggestions = [
        "📊 Budget my income & expenses",
        "💳 Calculate debt payoff",
        "🎯 Track my savings goal",
        "📈 Invest my surplus",
    ]
    for s in suggestions:
        if st.button(s, use_container_width=True):
            st.session_state["prefill"] = s

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()

    st.markdown("""
    <div class="disclaimer">
        ⚠️ Fin Ledger provides general financial information only. 
        Always consult a certified financial planner (CFP) for 
        personalized advice.
    </div>
    """, unsafe_allow_html=True)


# ── Main Chat Area ────────────────────────────────────────────────────────────
st.markdown("""
<h1 style="font-family:'DM Serif Display',serif; color:#C9A84C; font-size:2rem; margin-bottom:0.2rem;">
    Fin Ledger
</h1>
<p style="color:#6B7280; font-size:0.9rem; margin-bottom:1.5rem;">
    Your AI-powered personal finance advisor
</p>
""", unsafe_allow_html=True)

# Init messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Welcome screen
if not st.session_state["messages"]:
    st.markdown("""
    <div class="welcome-card">
        <div class="welcome-title">Welcome to Fin Ledger 👋</div>
        <div class="welcome-sub">
            I'm your personal AI financial advisor. I can help you budget smarter,<br>
            pay off debt faster, reach your savings goals, and invest wisely.<br><br>
            Try one of the prompts below or type your own question!
        </div>
        <div class="chip-row">
            <span class="chip">💼 I earn $5000, spend $3800</span>
            <span class="chip">💳 $10k debt at 18% interest</span>
            <span class="chip">🏠 Saving $20k for a house</span>
            <span class="chip">📈 How to invest $800/month</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Render chat history
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="msg-user">
            <div class="bubble-user">{msg["content"]}</div>
        </div>""", unsafe_allow_html=True)
    else:
        tool_html = msg.get("tool_html", "")
        st.markdown(f"""
        <div class="msg-bot">
            <div class="bot-avatar">💰</div>
            <div>
                <div class="bubble-bot">{msg["content"]}</div>
                {tool_html}
            </div>
        </div>""", unsafe_allow_html=True)

# Input area
prefill = st.session_state.pop("prefill", "")
user_input = st.chat_input("Ask Fin Ledger anything about your finances...")

if prefill:
    user_input = prefill

if user_input:
    if not api_key:
        st.error("⚠️ Please enter your Gemini API Key in the sidebar to start chatting.")
    else:
        # Add user message
        st.session_state["messages"].append({"role": "user", "content": user_input})

        with st.spinner("Fin Ledger is analyzing..."):
            try:
                client = get_gemini_client(api_key)
                history = st.session_state["messages"][:-1]
                reply, tool_html = chat_with_fin_ledger(client, user_input, history)

                if not reply:
                    reply = "I've analyzed your financial data above. Would you like me to explain anything in more detail?"

                st.session_state["messages"].append({
                    "role": "model",
                    "content": reply,
                    "tool_html": tool_html
                })
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.session_state["messages"].pop()

        st.rerun()
