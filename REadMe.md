# 🎬 San Francisco Film Locations Chatbot

An intelligent chatbot that explores thousands of San Francisco filming locations using natural language queries. Built with GeoPandas, Streamlit, and Google's Gemini AI.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GeoPandas](https://img.shields.io/badge/GeoPandas-139C5A?style=for-the-badge&logo=pandas&logoColor=white)

## 🌟 Features

- **Natural Language Queries**: Ask questions in plain English
- **Interactive Maps**: Visualize filming locations with Folium maps
- **Smart Data Analysis**: GeoPandas-powered spatial queries
- **Downloadable Results**: Export query results as CSV
- **Real-time Processing**: AI-powered query understanding and code generation

## 🚀 Live Demo

**[Try it now on Streamlit Cloud →](https://film-hackathon-app-68quvgslnrkvpxtxasnq7c.streamlit.app/)**

## 📊 Tech Stack

### Core Technologies
- **Frontend**: Streamlit
- **Backend**: Python 3.10+
- **Geospatial Analysis**: GeoPandas, Shapely
- **AI/ML**: Google Gemini 2.0 Flash
- **Mapping**: Folium
- **Data Processing**: Pandas, NumPy

### Architecture Components
- **Query Processor**: 3-stage pipeline (Preprocessing → Planning → Code Generation)
- **Chatbot Coordinator**: Intent classification and routing
- **Response Formatter**: Converts technical results to user-friendly messages
- **Map Analyzer**: Determines if queries need spatial visualization
- **Code Executor**: Safe execution of dynamically generated GeoPandas code

---

## 🏗️ Query Processing Pipeline

The heart of the application is a sophisticated 3-stage pipeline that transforms natural language into executable GeoPandas code: