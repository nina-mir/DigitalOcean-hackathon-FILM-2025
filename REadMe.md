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

---

## 📊 Dataset Information

### Source
**[SF Movies Dataset - San Francisco Open Data Portal](https://data.sfgov.org/Culture-and-Recreation/SF-Movies/djub-g8wi/about_data)**

This application uses official data from the San Francisco Film Commission, documenting films and TV shows shot in San Francisco since 1915.

### Dataset Statistics
- **Total Records**: 2,084 filming locations
- **Unique Films**: ~1,000+ movies and TV shows
- **Time Span**: 1915 - Present
- **Data Format**: GeoPackage (converted from original CSV with geocoded coordinates)

### Schema Overview

| Column | Type | Description | Usage in App |
|--------|------|-------------|--------------|
| **Title** | Text | Film or TV show name | Primary identifier for films |
| **Release Year** | Number | Year of release | Temporal filtering and analysis |
| **Locations** | Text | Specific SF filming location | Spatial queries and mapping |
| **Fun Facts** | Text | Trivia about location/filming | Contextual information display |
| **Production Company** | Text | Production studio | *(Available but not actively used)* |
| **Distributor** | Text | Distribution company | *(Available but not actively used)* |
| **Director** | Text | Director name | Person-based queries |
| **Writer** | Text | Screenplay writer | Person-based queries |
| **Actor 1** | Text | Lead actor | Actor frequency analysis |
| **Actor 2** | Text | Supporting actor | Multi-actor queries |
| **Actor 3** | Text | Additional actor | Comprehensive actor searches |

### Data Processing Pipeline
```
SF Open Data Portal (CSV)
         ↓
Geocoding (Address → Coordinates)
         ↓
Geometry Creation (Point objects)
         ↓
GeoPackage Export (.gpkg)
         ↓
GeoPandas DataFrame (in-memory)
```

### Key Data Characteristics

#### 1. Row Granularity
**Critical**: Each row represents **ONE filming location** for **ONE film**, not one film.

**Example:**
```
Vertigo (1958) was filmed at 8 locations in SF
→ Appears in 8 separate rows in the dataset
→ Same film data (Title, Year, Director, Actors) repeated 8 times
```

**Implications for Queries:**
- **Counting films**: Must deduplicate by `(Title, Year)` combination
- **Counting locations**: Use all rows directly
- **Person frequency**: Deduplicate first, then aggregate

#### 2. Missing Data Patterns
- **Coordinates**: ~5% of locations lack precise geocoding
- **Fun Facts**: Present for ~30% of locations
- **Production Company/Distributor**: Sparse coverage (~40%)
- **Actors**: Not all films have 3 actors listed

#### 3. Temporal Distribution
```
1915-1950:   ~50 films
1950-1970:   ~150 films
1970-1990:   ~300 films
1990-2010:   ~600 films
2010-Present: ~900 films
```

### Data Quality & Cleaning

The application implements robust data cleaning:
```python
# Automatic cleaning applied to all queries:
- Null/NaN values filtered
- Empty strings removed
- Whitespace-only entries excluded
- String representations of null ('None', 'nan') handled
- Year field coerced to numeric with error handling
```

### Notable Films in Dataset

Some iconic films included:
- **Vertigo** (1958) - Alfred Hitchcock
- **Bullitt** (1968) - Steve McQueen
- **Dirty Harry** (1971) - Clint Eastwood
- **The Maltese Falcon** (1941) - Humphrey Bogart
- **Mrs. Doubtfire** (1993) - Robin Williams
- **The Rock** (1996) - Nicolas Cage, Sean Connery
- **Milk** (2008) - Sean Penn
- **Venom** (2018) - Tom Hardy

### Geographic Coverage

**Most Filmed Locations:**
1. Golden Gate Bridge
2. City Hall
3. Union Square
4. Fisherman's Wharf
5. Alcatraz Island
6. Lombard Street
7. Chinatown
8. Financial District

**Neighborhoods Represented:**
- Downtown/Financial District
- Chinatown
- North Beach
- Pacific Heights
- Haight-Ashbury
- Mission District
- Marina District
- Presidio
- And more...

### Data Update Frequency

The SF Open Data Portal dataset is updated periodically by the San Francisco Film Commission. This application uses a snapshot from **May 7, 2025**.

To update the dataset:
1. Download latest CSV from [SF Open Data Portal](https://data.sfgov.org/Culture-and-Recreation/SF-Movies/djub-g8wi)
2. Geocode new locations (using Nominatim, Google Maps API, or similar)
3. Convert to GeoPackage format
4. Replace `sf_film_May7_2025_data.gpkg`

---

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
```
┌─────────────────────────────────────────────────────────────────┐
│                    USER QUERY (Natural Language)                 │
│              "What films were shot at Golden Gate Bridge?"       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     STAGE 1: PREPROCESSING                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Intent Classification (Data Query vs Greeting/Help)   │  │
│  │  • Query Decomposition into Atomic Tasks                 │  │
│  │  • Filter Extraction (Spatial, Attribute, Temporal)      │  │
│  │  • Data Modification Detection & Rejection               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│                             ▼                                    │
│  Output: Structured JSON                                         │
│  {                                                               │
│    "tasks": ["Find films at Golden Gate Bridge"],               │
│    "filters": [{                                                 │
│      "field": "Locations",                                       │
│      "condition": "contains",                                    │
│      "value": "Golden Gate Bridge"                              │
│    }],                                                           │
│    "filter_logic": "AND"                                         │
│  }                                                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STAGE 2: NLP ACTION PLANNING                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Understands Database Row Granularity                  │  │
│  │  • Determines if Film-Level Deduplication Needed         │  │
│  │  • Creates Natural Language Execution Plan               │  │
│  │  • Identifies Required GeoPandas Operations              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│                             ▼                                    │
│  Output: Action Plan                                             │
│  "1. Load films dataframe                                        │
│   2. Filter rows where Locations contains 'Golden Gate Bridge'  │
│   3. Return distinct film titles"                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STAGE 3: CODE GENERATION                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Generates Executable Python/GeoPandas Code            │  │
│  │  • Handles Nested Data Structures                        │  │
│  │  • Implements Data Cleaning (nulls, whitespace)          │  │
│  │  • Creates Standardized Return Format                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│                             ▼                                    │
│  Output: Python Function                                         │
│  def process_sf_film_query(gdf):                                │
│      filtered = gdf[gdf['Locations'].str.contains(              │
│          'Golden Gate Bridge', na=False)]                       │
│      films = filtered[['Title','Year']].drop_duplicates()       │
│      return {'data': films.to_dict('records'), ...}             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     CODE EXECUTION & VALIDATION                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Safe Execution in Controlled Namespace                │  │
│  │  • Input Validation (no malicious code patterns)         │  │
│  │  • Error Handling & User-Friendly Messages               │  │
│  │  • Result Type Detection (DataFrame, Dict, List, etc.)   │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       MAP ANALYSIS (Optional)                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Probes Result Structure for Location Data            │  │
│  │  • Matches Location Names to Geometries                 │  │
│  │  • Determines if Spatial Visualization Needed           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│                    If mappable data found                        │
│                             ▼                                    │
│                    Generate Folium Map                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RESPONSE FORMATTING                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  • Converts Technical Results to Chat Messages           │  │
│  │  • Formats DataFrames, Lists, Dicts for Display         │  │
│  │  • Handles Nested Data Unwrapping                        │  │
│  │  • Adds Download Buttons for Tables                     │  │
│  │  • Embeds Interactive Maps                               │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    USER RECEIVES RESULTS                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  ✅ Natural Language Summary                             │  │
│  │  📊 Interactive Data Tables (downloadable)               │  │
│  │  🗺️ Folium Map Visualization                            │  │
│  │  💡 Suggested Follow-up Queries                          │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Design Principles

1. **Read-Only Operations**: System rejects any data modification attempts
2. **Film-Level vs Location-Level Awareness**: Database has one row per filming location; system intelligently deduplicates when counting films
3. **Safe Code Execution**: Generated code validated for security patterns before execution
4. **Graceful Error Handling**: Technical errors translated to user-friendly messages
5. **Context-Aware Responses**: Different formatting for DataFrames, maps, counts, lists

---

## 📁 Project Structure
```
sf-film-chatbot/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── sf_film_May7_2025_data.gpkg    # GeoPackage database
│
├── src/
│   ├── pandas_script.py            # QueryProcessor (3-stage pipeline)
│   ├── chatbot_coordinator.py      # Intent routing & orchestration
│   ├── response_formatter.py       # Result formatting for chat display
│   ├── ai_service.py               # Gemini API wrapper
│   ├── code_executor.py            # Safe code execution environment
│   ├── system_instructions.py      # Prompt template management
│   ├── data_loader.py              # GeoDataFrame initialization
│   ├── logger.py                   # Structured logging with geometry serialization
│   ├── map_analyzer.py             # Location data detection for mapping
│   ├── map_generator.py            # Folium map creation
│   └── config.py                   # Configuration & secrets management
│
└── instructions/
    ├── preprocessing.md            # Stage 1 system prompt
    ├── nlp_plan.md                 # Stage 2 system prompt
    └── code_generation.md          # Stage 3 system prompt
```

---

## 🚀 Local Setup

### Prerequisites
- Python 3.10 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/sf-film-chatbot.git
cd sf-film-chatbot
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

5. **Run the app**
```bash
streamlit run app.py
```

---

## ☁️ Production Deployment

### Deploy on DigitalOcean App Platform

For production deployment with enhanced features:

#### 1. **One-Click Deploy**
[![Deploy to DO](https://www.deploytodo.com/do-btn-blue.svg)](https://cloud.digitalocean.com/apps/new)

#### 2. **Manual Deployment Steps**
```bash
# 1. Create App Platform app
doctl apps create --spec .do/app.yaml

# 2. Set environment variables
doctl apps update YOUR_APP_ID --env GEMINI_API_KEY=your_key

# 3. Deploy
git push origin main
```

#### 3. **Add Authentication with Auth0**

For multi-user support with saved queries:
```python
# Install Auth0 SDK
pip install authlib

# Add to app.py
from authlib.integrations.requests_client import OAuth2Session

# Configure Auth0
oauth = OAuth2Session(
    client_id='YOUR_AUTH0_CLIENT_ID',
    client_secret='YOUR_AUTH0_CLIENT_SECRET',
    redirect_uri='https://your-app.ondigitalocean.app/callback'
)
```

**Benefits of Auth0 Integration:**
- User authentication & profiles
- Save favorite queries
- Query history per user
- Share custom film tours
- Rate limiting per user

---

## 🗺️ Future Enhancements

### 1. Walking Tours Generator
Create personalized SF film location walking tours:
```python
def generate_walking_tour(film_ids, start_location):
    """
    Generate optimized walking route through filming locations
    
    Features:
    - TSP algorithm for shortest path
    - Time estimates between locations
    - Historical film trivia at each stop
    - Photo spots recommendations
    - Export to Google Maps / Apple Maps
    """
    pass
```

**Example Tours:**
- "Hitchcock's San Francisco" (Vertigo locations)
- "Classic Film Noir Trail" (The Maltese Falcon, Dark Passage)
- "Modern Action Movies" (The Rock, Matrix Resurrections)
- "Robin Williams Memorial Tour" (Mrs. Doubtfire, Dead Poets Society)

**Implementation Roadmap:**
1. **Route Optimization**: Use NetworkX for traveling salesman problem
2. **Walking Distance Calculation**: Integrate OSRM or Google Maps Directions API
3. **Tour Metadata**: Duration, difficulty, accessibility info
4. **Mobile-Friendly Export**: GPX files, deep links to navigation apps
5. **Audio Guide Integration**: Text-to-speech for location narration

### 2. User Data Persistence

With DigitalOcean + Auth0:
```sql
-- PostgreSQL schema for user data
CREATE TABLE user_profiles (
    user_id VARCHAR PRIMARY KEY,
    email VARCHAR UNIQUE,
    created_at TIMESTAMP
);

CREATE TABLE saved_queries (
    query_id SERIAL PRIMARY KEY,
    user_id VARCHAR REFERENCES user_profiles(user_id),
    query_text TEXT,
    results JSONB,
    created_at TIMESTAMP
);

CREATE TABLE custom_tours (
    tour_id SERIAL PRIMARY KEY,
    user_id VARCHAR REFERENCES user_profiles(user_id),
    tour_name VARCHAR,
    locations JSONB,
    is_public BOOLEAN DEFAULT false,
    created_at TIMESTAMP
);

CREATE TABLE tour_ratings (
    rating_id SERIAL PRIMARY KEY,
    tour_id INTEGER REFERENCES custom_tours(tour_id),
    user_id VARCHAR REFERENCES user_profiles(user_id),
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    review TEXT,
    created_at TIMESTAMP
);
```

### 3. Social Features
- Share custom tours with friends
- Rate filming locations
- Upload photos at locations
- Community-curated "must-see" spots
- Tour completion badges
- Leaderboards for tour enthusiasts

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Add more AI models (Claude, GPT-4)
- [ ] Implement caching for faster responses
- [ ] Add voice input support
- [ ] Create mobile app version
- [ ] Expand to other cities' film data
- [ ] Add augmented reality features for

