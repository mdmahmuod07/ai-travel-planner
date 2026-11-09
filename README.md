# ✈️ AI Travel Planner - Multi-Agent System

An end-to-end, intelligent AI Travel Planner built with a **Multi-Agent System architecture** (FastAPI backend + React frontend).

The application breaks down travel planning into specialized autonomous agents that work collaboratively in real-time to design personalized, geographically optimized, day-by-day travel itineraries.

---

## 🤖 Multi-Agent Architecture

```
                          ┌──────────────────────────┐
                          │   User Interface (React) │
                          └─────────────┬────────────┘
                                        │ HTTP / EventStream (SSE)
                                        ▼
                          ┌──────────────────────────┐
                          │    FastAPI Server API    │
                          └─────────────┬────────────┘
                                        │
             ┌──────────────────────────┴──────────────────────────┐
             ▼                                                     ▼
┌──────────────────────────┐                             ┌──────────────────────────┐
│ Multi-Agent Orchestrator │                             │  Export & PDF Engine     │
└────────────┬─────────────┘                             └──────────────────────────┘
             │
 ┌───────────┼───────────────────┬───────────────────┬───────────────────┐
 ▼           ▼                   ▼                   ▼                   ▼
┌─────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌──────────────────┐
│  Agent  │ │      Agent      │ │      Agent      │ │      Agent      │ │      Agent       │
│ 1: Dest │ │ 2: Itinerary    │ │ 3: Budget & Acc │ │ 4: Dining       │ │ 5: Packing & Tips│
│ Specialist│ │ Orchestrator  │ │ Specialist      │ │ Specialist      │ │ Specialist       │
└─────────┘ └─────────────────┘ └─────────────────┘ └─────────────────┘ └──────────────────┘
```

### Specialized Agents

1. **Destination & Attraction Specialist Agent**:
   - Researches destination overview, top landmarks, seasonal best times, and hidden gems.
2. **Itinerary Orchestrator Agent**:
   - Structures day-by-day activity timelines (Morning, Afternoon, Evening) with geographic clustering to minimize transit time.
3. **Budget & Accommodation Specialist Agent**:
   - Projects cost breakdowns (Accommodation, Dining, Activities, Transport, Misc) and vets lodging options for Budget, Moderate, and Luxury tiers.
4. **Dining & Culinary Specialist Agent**:
   - Suggests authentic dining, must-try regional dishes, and applies dietary filters (Vegetarian, Vegan, Halal, Kosher, Gluten-Free, etc.).
5. **Packing & Travel Safety Specialist Agent**:
   - Formulates weather-aware packing lists (by category) alongside entry/visa rules, emergency numbers, and local etiquette.

---

## 🚀 How to Run

### 1. Backend Setup (FastAPI)

```bash
cd backend

# (Optional) Install dependencies if needed
pip install -r requirements.txt

# Start backend server (runs on http://127.0.0.1:8000)
python run.py
```

*Note: You can optionally set `GEMINI_API_KEY` or `OPENAI_API_KEY` in your environment. If no key is set, the system seamlessly uses its built-in rule-based multi-agent generator!*

### 2. Frontend Setup (React + Vite + Tailwind CSS)

```bash
cd frontend

# Install dependencies (if not already installed)
npm install

# Run Vite dev server (runs on http://localhost:3000)
npm run dev
```

---

## 🌟 Key Features

- **Real-Time Agent Progress Monitoring**: Visual log console showing each agent's live reasoning step via SSE streaming.
- **Interactive Itinerary Dashboard**: Day-by-day tabbed timeline with activities, costs, neighborhood locations, and insider tips.
- **Budget & Accommodation Breakdown**: Detailed expense summary & curated hotel options.
- **Dining & Dietary Filter**: Culinary guide matching traveler dietary requirements.
- **Interactive Packing Checklist**: Check off items as you pack, plus safety & weather tips.
- **One-Click Export**: Download complete itinerary as Markdown (`.md`) or print/save as PDF.
- **Quick-Start Presets**: Pre-configured sample trips (Tokyo, Paris, Amalfi Coast, Bali) for instant testing.
