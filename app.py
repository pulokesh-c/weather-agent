import streamlit as st
import base64

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from agent import agent


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Weather Agent",
    page_icon="🌦️",
    layout="wide"
)


# ============================================================
# BACKGROUND IMAGE HELPER
# ============================================================

def get_base64_image(image_path):

    with open(image_path, "rb") as image_file:

        return base64.b64encode(
            image_file.read()
        ).decode()


# ============================================================
# LOAD BACKGROUND
# ============================================================

background_image = get_base64_image(
    "assets/weather_background.png"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(

    f"""
    <style>

    /* ========================================================
       MAIN APP BACKGROUND
    ======================================================== */

    .stApp {{

        background-image:
            linear-gradient(
                rgba(20, 45, 75, 0.25),
                rgba(20, 45, 75, 0.25)
            ),
            url("data:image/png;base64,{background_image}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;

    }}


    /* ========================================================
       MAIN CONTENT
    ======================================================== */

    .main {{

        background: transparent;

    }}


    /* ========================================================
       SIDEBAR
    ======================================================== */

    [data-testid="stSidebar"] {{

        background:
            linear-gradient(
                180deg,
                rgba(220, 235, 250, 0.88),
                rgba(205, 225, 245, 0.82)
            );

        backdrop-filter: blur(18px);

        border-right:
            1px solid rgba(255, 255, 255, 0.5);

    }}


    [data-testid="stSidebar"] * {{

        color: #26374a;

    }}


    /* ========================================================
       HEADINGS
    ======================================================== */

    h1 {{

        color: #17365d !important;

        font-weight: 800;

    }}

    h2, h3 {{

        color: #263d5b !important;

    }}


    /* ========================================================
       SUGGESTION BUTTONS
    ======================================================== */

    .stButton > button {{

        width: 100%;

        min-height: 58px;

        border-radius: 14px;

        border:
            1px solid rgba(255, 255, 255, 0.7);

        background:
            rgba(255, 255, 255, 0.82);

        backdrop-filter: blur(10px);

        color: #25374d;

        font-size: 16px;

        transition:
            0.2s ease-in-out;

        box-shadow:
            0px 4px 12px rgba(0, 0, 0, 0.08);

    }}


    .stButton > button:hover {{

        transform: translateY(-2px);

        border-color: #5d9cec;

        background:
            rgba(255, 255, 255, 0.95);

        box-shadow:
            0px 8px 20px rgba(40, 100, 180, 0.18);

    }}


    /* ========================================================
       CHAT MESSAGES
    ======================================================== */

    [data-testid="stChatMessage"] {{

        background:
            rgba(255, 255, 255, 0.88);

        backdrop-filter: blur(14px);

        border-radius: 18px;

        padding: 14px;

        margin-bottom: 14px;

        box-shadow:
            0px 6px 20px rgba(0, 0, 0, 0.08);

    }}


    /* ========================================================
       CHAT INPUT
    ======================================================== */

    [data-testid="stChatInput"] {{

        background:
            rgba(255, 255, 255, 0.88);

        backdrop-filter: blur(15px);

        border-radius: 18px;

        border:
            1px solid rgba(255, 255, 255, 0.7);

        box-shadow:
            0px 6px 20px rgba(0, 0, 0, 0.12);

    }}


    /* ========================================================
       EXPANDER
    ======================================================== */

    [data-testid="stExpander"] {{

        background:
            rgba(255, 255, 255, 0.82);

        backdrop-filter: blur(12px);

        border-radius: 14px;

        border:
            1px solid rgba(255, 255, 255, 0.7);

    }}


    /* ========================================================
       CAPABILITY CARDS
    ======================================================== */

    .capability {{

        background:
            rgba(255, 255, 255, 0.5);

        padding: 10px;

        border-radius: 10px;

        margin-bottom: 8px;

    }}


    /* ========================================================
       HIDE STREAMLIT DEFAULT ELEMENTS
    ======================================================== */

    #MainMenu {{

        visibility: hidden;

    }}

    footer {{

        visibility: hidden;

    }}

    </style>
    """,

    unsafe_allow_html=True

)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🌦️ Weather Agent")

    st.caption(
        "Your AI-powered weather assistant."
    )

    st.divider()


    st.subheader("✨ What I can do")


    st.markdown(
        """
        <div class="capability">
        🌡️ <b>Check temperature</b>
        </div>

        <div class="capability">
        🌧️ <b>Check rain probability</b>
        </div>

        <div class="capability">
        💨 <b>Check wind & humidity</b>
        </div>

        <div class="capability">
        🧮 <b>Perform calculations</b>
        </div>
        """,

        unsafe_allow_html=True
    )


    st.divider()


    st.subheader("💡 Example questions")

    st.markdown(
        """
        🌦️ What's the weather in Kolkata?

        ☂️ Will it rain in Mumbai today?

        💨 How windy is Delhi right now?

        🔄 Convert Kolkata's maximum temperature to Fahrenheit.
        """
    )


    st.divider()


    if st.button("🗑️ Clear conversation"):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# MAIN HEADER
# ============================================================

st.title("🌦️ Weather Agent")

st.subheader(
    "Your AI-powered weather assistant"
)

st.write(
    "Ask about temperature, rain, humidity, wind conditions, "
    "or perform weather-related calculations."
)


# ============================================================
# SUGGESTION QUESTIONS
# ============================================================

st.markdown("## ✨ Try asking")


col1, col2 = st.columns(2)


with col1:

    temperature_button = st.button(
        "🌡️ Temperature in Kolkata"
    )

    delhi_weather_button = st.button(
        "💨 Current weather in Delhi"
    )


with col2:

    rain_button = st.button(
        "☂️ Will it rain in Mumbai?"
    )

    fahrenheit_button = st.button(
        "🔄 Kolkata temperature → Fahrenheit"
    )


# ============================================================
# DETERMINE USER QUERY
# ============================================================

user_query = None


if temperature_button:

    user_query = (
        "What is the temperature in Kolkata today?"
    )


elif delhi_weather_button:

    user_query = (
        "What is the current weather in Delhi today?"
    )


elif rain_button:

    user_query = (
        "Will it rain in Mumbai today?"
    )


elif fahrenheit_button:

    user_query = (
        "Get today's maximum temperature in Kolkata "
        "and convert it to Fahrenheit."
    )


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message("user"):

            st.write(message["content"])


    elif message["role"] == "assistant":

        with st.chat_message("assistant"):

            st.write(message["content"])

            if "agent_messages" in message:

                with st.expander(
                    "🔍 See how the agent solved this"
                ):

                    for agent_message in message["agent_messages"]:

                        # HUMAN MESSAGE

                        if isinstance(
                            agent_message,
                            HumanMessage
                        ):

                            st.markdown(
                                "**👤 User request**"
                            )

                            st.write(
                                agent_message.content
                            )


                        # AI MESSAGE

                        elif isinstance(
                            agent_message,
                            AIMessage
                        ):

                            if agent_message.tool_calls:

                                st.markdown(
                                    "**🧠 Agent decided to use:**"
                                )

                                for tool_call in agent_message.tool_calls:

                                    st.code(
                                        f"Tool: "
                                        f"{tool_call['name']}"
                                    )

                                    st.json(
                                        tool_call["args"]
                                    )


                        # TOOL MESSAGE

                        elif isinstance(
                            agent_message,
                            ToolMessage
                        ):

                            st.markdown(
                                "**⚙️ Tool result**"
                            )

                            st.info(
                                agent_message.content
                            )


# ============================================================
# CHAT INPUT
# ============================================================

chat_input = st.chat_input(
    "Ask me anything about today's weather..."
)


if chat_input:

    user_query = chat_input


# ============================================================
# AGENT EXECUTION
# ============================================================

if user_query:

    # --------------------------------------------------------
    # SHOW USER MESSAGE
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.write(user_query)


    # --------------------------------------------------------
    # SAVE USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )


    # --------------------------------------------------------
    # RUN AGENT
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🌦️ Checking the weather..."
        ):

            result = agent.invoke(
                {
                    "messages": [
                        HumanMessage(
                            content=user_query
                        )
                    ]
                }
            )


        # ----------------------------------------------------
        # GET ALL AGENT MESSAGES
        # ----------------------------------------------------

        agent_messages = result["messages"]


        # ----------------------------------------------------
        # GET FINAL MESSAGE
        # ----------------------------------------------------

        final_message = agent_messages[-1]


        # ----------------------------------------------------
        # HANDLE GEMINI CONTENT FORMAT
        # ----------------------------------------------------

        final_content = final_message.content


        if isinstance(final_content, list):

            try:

                final_content = final_content[0]["text"]

            except Exception:

                final_content = str(final_content)


        # ----------------------------------------------------
        # DISPLAY FINAL RESPONSE
        # ----------------------------------------------------

        st.write(final_content)


        # ----------------------------------------------------
        # SHOW AGENT TRACE
        # ----------------------------------------------------

        with st.expander(
            "🔍 See how the agent solved this"
        ):

            for agent_message in agent_messages:


                # ------------------------------------------------
                # HUMAN MESSAGE
                # ------------------------------------------------

                if isinstance(
                    agent_message,
                    HumanMessage
                ):

                    st.markdown(
                        "**👤 User request**"
                    )

                    st.write(
                        agent_message.content
                    )


                # ------------------------------------------------
                # AI MESSAGE WITH TOOL CALL
                # ------------------------------------------------

                elif isinstance(
                    agent_message,
                    AIMessage
                ):

                    if agent_message.tool_calls:

                        st.markdown(
                            "**🧠 Agent decided to use:**"
                        )

                        for tool_call in agent_message.tool_calls:

                            st.code(
                                f"Tool: "
                                f"{tool_call['name']}"
                            )

                            st.json(
                                tool_call["args"]
                            )


                # ------------------------------------------------
                # TOOL RESULT
                # ------------------------------------------------

                elif isinstance(
                    agent_message,
                    ToolMessage
                ):

                    st.markdown(
                        "**⚙️ Tool result**"
                    )

                    st.info(
                        agent_message.content
                    )


    # ========================================================
    # SAVE ASSISTANT RESPONSE
    # ========================================================

    st.session_state.messages.append(

        {
            "role": "assistant",

            "content": final_content,

            "agent_messages": agent_messages
        }
    )