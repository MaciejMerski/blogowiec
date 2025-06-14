import streamlit as st
from crewai import Agent, Crew
from langchain.chat_models import ChatOpenAI
import os

# --- Ustawienia interfejsu ---
st.set_page_config(page_title="Blogowy CrewAI", layout="centered")
st.title("🧠 Generator Wpisów Blogowych z CrewAI")

# --- Formularz wejściowy ---
product_url = st.text_input("📦 Wklej link do produktu ze sklepu", "")

generate = st.button("🎯 Generuj wpis")

# --- Gdy kliknięto przycisk ---
if generate and product_url:
    with st.spinner("Tworzę wpis..."):

        # --- Agent LLM (używa klucza OpenAI) ---
        openai_api_key = os.getenv("OPENAI_API_KEY")
        llm = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key)

        # --- Agent 1: Strateg Treści ---
        strategist = Agent(
            role="Strateg Treści",
            goal="Zaproponuj pomysł i strukturę wpisu blogowego na podstawie produktu",
            backstory="Jesteś specjalistą od storytellingu i marketingu w e-commerce z naciskiem na alkohole premium i delikatesy",
            llm=llm,
            verbose=True
        )

        # --- Agent 2: Pisarz ---
        writer = Agent(
            role="Pisarz",
            goal="Na podstawie pomysłu napisz lekki, ciekawy i estetyczny szkic wpisu blogowego",
            backstory="Tworzysz przyjazne i informacyjne treści na blog sklepu z alkoholami i upominkami",
            llm=llm,
            verbose=True
        )

        # --- Crew: zespół agentów ---
        crew = Crew(
            agents=[strategist, writer],
            verbose=True
        )

        result = crew.run(product_url)

        # --- Wynik ---
        st.success("✅ Gotowe!")
        st.markdown("### ✍️ Wygenerowany wpis:")
        st.markdown(result)


