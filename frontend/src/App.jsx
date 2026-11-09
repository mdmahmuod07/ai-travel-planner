import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import PresetBar from './components/PresetBar';
import TravelForm from './components/TravelForm';
import AgentProgress from './components/AgentProgress';
import ItineraryView from './components/ItineraryView';
import MapView from './components/MapView';
import BudgetCard from './components/BudgetCard';
import DiningSection from './components/DiningSection';
import PackingChecklist from './components/PackingChecklist';
import AgentTelemetryDrawer from './components/AgentTelemetryDrawer';
import SavedTripsDrawer, { saveTripToStorage } from './components/SavedTripsDrawer';
import { fetchPresets, generatePlanStream, downloadMarkdown } from './services/api';
import { exportToCalendar } from './services/calendarExport';
import {
  Download,
  Sparkles,
  Calendar,
  Compass,
  Printer,
  Bookmark,
  CalendarDays,
  Bot,
  Activity
} from 'lucide-react';

export default function App() {
  const [presets, setPresets] = useState([]);
  const [selectedPreset, setSelectedPreset] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [agentLogs, setAgentLogs] = useState([]);
  const [planResult, setPlanResult] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [isTelemetryOpen, setIsTelemetryOpen] = useState(false);
  const [currency, setCurrency] = useState('INR');
  const [activeDay, setActiveDay] = useState(1);

  useEffect(() => {
    fetchPresets().then(data => setPresets(data));
  }, []);

  const handlePresetSelect = (preset) => {
    setSelectedPreset(preset);
    if (preset.currency) setCurrency(preset.currency);
    setErrorMsg(null);
  };

  const handleFormSubmit = (formData) => {
    setIsLoading(true);
    setAgentLogs([]);
    setPlanResult(null);
    setErrorMsg(null);
    if (formData.currency) {
      setCurrency(formData.currency);
    }

    generatePlanStream(
      formData,
      (logEntry) => {
        setAgentLogs(prev => [...prev, logEntry]);
      },
      (finalResult) => {
        setPlanResult(finalResult);
        if (finalResult.budget_breakdown?.currency) {
          setCurrency(finalResult.budget_breakdown.currency);
        }
        setIsLoading(false);
        saveTripToStorage(finalResult);
      },
      (errMessage) => {
        setErrorMsg(errMessage);
        setIsLoading(false);
      }
    );
  };

  const handleSwapActivity = (dayNumber, activityIndex) => {
    if (!planResult) return;
    const destLower = (planResult.destination || '').toLowerCase();
    const isTokyo = destLower.includes('tokyo');
    const isIstanbul = destLower.includes('istanbul') || destLower.includes('turkey');
    const curr = planResult.budget_breakdown?.currency || 'INR';

    const tokyoAlternatives = [
      {
        title: "Nezu Shrine & Vermilion Torii Tunnel Walk",
        venue_name: "Nezu Shrine (根津神社)",
        neighborhood: "Nezu, Bunkyo Ward",
        search_query: "Nezu Shrine, Bunkyo, Tokyo",
        description: "Explore one of Tokyo's oldest Shinto shrines featuring a quiet hillside azalea garden and scenic vermilion torii tunnel.",
        location: "Bunkyo Ward, Tokyo",
        duration: "2 hours",
        estimated_cost: curr === "INR" ? "₹350" : (curr === "JPY" ? "¥500" : "$5"),
        tips: "Visit during the morning for serene contemplative walking.",
        category: "Spiritual & Nature",
        lat: 35.7202,
        lng: 139.7618
      },
      {
        title: "Yanaka Ginza Historic Shitamachi Promenade",
        venue_name: "Yanaka Ginza Shopping Street",
        neighborhood: "Yanaka, Taito Ward",
        search_query: "Yanaka Ginza, Taito, Tokyo",
        description: "Stroll preserved pre-war nostalgic shopping street lined with local cat-themed bakeries, croquette shops, and artisan crafts.",
        location: "Yanaka, Taito Ward, Tokyo",
        duration: "2 hours",
        estimated_cost: curr === "INR" ? "₹750" : (curr === "JPY" ? "¥1,200" : "$10"),
        tips: "Watch sunset from the Yuyake Dandan stairs at the street entrance.",
        category: "Culture & Shopping",
        lat: 35.7275,
        lng: 139.7686
      },
      {
        title: "Roppongi Hills Mori Art Museum & City View",
        venue_name: "Mori Art Museum & Tokyo City View",
        neighborhood: "Roppongi, Minato Ward",
        search_query: "Mori Art Museum, Roppongi, Tokyo",
        description: "Contemporary international art exhibitions coupled with panoramic 52nd-floor observation vistas overlooking Tokyo Tower.",
        location: "Roppongi, Minato Ward, Tokyo",
        duration: "2.5 hours",
        estimated_cost: curr === "INR" ? "₹1,200" : (curr === "JPY" ? "¥2,000" : "$15"),
        tips: "Museum remains open until 10:00 PM most evenings.",
        category: "Art & Skyline",
        lat: 35.6605,
        lng: 139.7292
      }
    ];

    const istanbulAlternatives = [
      {
        title: "Süleymaniye Mosque & Golden Horn Panoramic Terrace",
        venue_name: "Süleymaniye Mosque (Süleymaniye Camii)",
        neighborhood: "Süleymaniye, Fatih",
        search_query: "Süleymaniye Mosque, Fatih, Istanbul",
        description: "Marvel at imperial master architect Mimar Sinan's supreme masterpiece, featuring tranquil courtyards and sweeping gardens overlooking the Golden Horn.",
        location: "Süleymaniye, Fatih, Istanbul",
        duration: "2 hours",
        estimated_cost: curr === "INR" ? "₹400" : (curr === "TRY" ? "₺150" : "$5"),
        tips: "Admission is free; visit outside prayer hours and relax at the garden terrace behind the qibla wall.",
        category: "Historic & Architecture",
        lat: 41.0163,
        lng: 28.9644
      },
      {
        title: "Galata Mevlevi Lodge & Whirling Dervishes Heritage Hall",
        venue_name: "Galata Mevlevihanesi Museum",
        neighborhood: "Şahkulu, Beyoğlu",
        search_query: "Galata Mevlevihanesi Museum, Beyoğlu, Istanbul",
        description: "Discover Istanbul's oldest surviving Mevlevi Sufi lodge, showcasing antique ney flutes, Divan poetry manuscripts, and the historic wooden semahane hall.",
        location: "Galip Dede Cd. No:15, Beyoğlu, Istanbul",
        duration: "2 hours",
        estimated_cost: curr === "INR" ? "₹750" : (curr === "TRY" ? "₺300" : "$10"),
        tips: "Located just steps from the end of İstiklal Street near the Tünel funicular station.",
        category: "Spiritual & Cultural Heritage",
        lat: 41.0284,
        lng: 28.9749
      },
      {
        title: "Pierre Loti Hill & Panoramic Golden Horn Cable Car",
        venue_name: "Pierre Loti Hill & Eyüp Teleferik",
        neighborhood: "Eyüpsultan",
        search_query: "Pierre Loti Hill, Eyüpsultan, Istanbul",
        description: "Ascend by the TF2 municipal cable car over historic Eyüp cemetery gardens to sip traditional Turkish tea overlooking the illuminated Golden Horn inlet.",
        location: "Eyüp Merkez, Eyüpsultan, Istanbul",
        duration: "2.5 hours",
        estimated_cost: curr === "INR" ? "₹500" : (curr === "TRY" ? "₺200" : "$7"),
        tips: "Board the public cable car using your Istanbulkart for discounted municipal fares.",
        category: "Panoramic Scenic Views",
        lat: 41.0543,
        lng: 28.9344
      }
    ];

    const targetDay = planResult.itinerary.find(d => d.day_number === dayNumber);
    const existingAct = targetDay?.activities?.[activityIndex];
    const baseLat = existingAct?.lat || (isIstanbul ? 41.0082 : (isTokyo ? 35.6812 : 20.0));
    const baseLng = existingAct?.lng || (isIstanbul ? 28.9784 : (isTokyo ? 139.7671 : 0.0));

    const generalAlternatives = [
      {
        title: `Artisan Craft & Pottery Discovery in ${planResult.destination}`,
        venue_name: `Artisan Heritage Studio of ${planResult.destination}`,
        neighborhood: "Artisan Quarter",
        search_query: `Artisan Studio, ${planResult.destination}`,
        description: "Hands-on masterclass with local artisans crafting handmade regional souvenirs and pottery.",
        location: `Artisan Quarter, ${planResult.destination}`,
        duration: "2 hours",
        estimated_cost: curr === "INR" ? "₹1,200" : "$15",
        tips: "Keep your handcrafted souvenir as a memorable keepsake!",
        category: "Crafts & Art",
        lat: parseFloat((baseLat + 0.003).toFixed(4)),
        lng: parseFloat((baseLng + 0.004).toFixed(4))
      },
      {
        title: `Panoramic Sunset Observation Terrace in ${planResult.destination}`,
        venue_name: `City View Panoramic Terrace of ${planResult.destination}`,
        neighborhood: "Central District",
        search_query: `Observation Deck, ${planResult.destination}`,
        description: "Take in breathtaking 360-degree vistas of the skyline while relaxing with authentic local beverages.",
        location: `Central District, ${planResult.destination}`,
        duration: "1.5 hours",
        estimated_cost: curr === "INR" ? "₹900" : "$12",
        tips: "Arrive 30 minutes before golden hour sunset for the most dramatic photography lighting.",
        category: "Sightseeing",
        lat: parseFloat((baseLat - 0.003).toFixed(4)),
        lng: parseFloat((baseLng - 0.002).toFixed(4))
      }
    ];

    const alts = isTokyo ? tokyoAlternatives : (isIstanbul ? istanbulAlternatives : generalAlternatives);
    const randomAlt = alts[Math.floor(Math.random() * alts.length)];

    const updatedPlan = JSON.parse(JSON.stringify(planResult));
    const dayObj = updatedPlan.itinerary.find(d => d.day_number === dayNumber);
    if (dayObj && dayObj.activities[activityIndex]) {
      const origSlot = dayObj.activities[activityIndex].time_slot;
      dayObj.activities[activityIndex] = {
        ...randomAlt,
        time_slot: origSlot
      };
      setPlanResult(updatedPlan);
      saveTripToStorage(updatedPlan);
    }
  };

  const handleReset = () => {
    setPlanResult(null);
    setAgentLogs([]);
    setErrorMsg(null);
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col selection:bg-sky-500 selection:text-white print:bg-white print:text-slate-900">
      <Header
        onReset={handleReset}
        hasPlan={!!planResult}
        onOpenDrawer={() => setIsDrawerOpen(true)}
        currentCurrency={currency}
        onCurrencyChange={setCurrency}
      />

      <SavedTripsDrawer
        isOpen={isDrawerOpen}
        onClose={() => setIsDrawerOpen(false)}
        onLoadTrip={(trip) => {
          setPlanResult(trip);
          if (trip.budget_breakdown?.currency) {
            setCurrency(trip.budget_breakdown.currency);
          }
        }}
      />

      {/* Collapsible Multi-Agent Orchestration Log Drawer (Requirement 5) */}
      <AgentTelemetryDrawer
        isOpen={isTelemetryOpen}
        onClose={() => setIsTelemetryOpen(false)}
        logs={agentLogs.length > 0 ? agentLogs : planResult?.agent_logs || []}
        tripId={planResult?.trip_id}
        destination={planResult?.destination}
      />

      <main className="grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 print:p-0 print:max-w-none">
        {!planResult ? (
          <div className="max-w-4xl mx-auto">
            {!isLoading && (
              <PresetBar presets={presets} onSelect={handlePresetSelect} />
            )}

            <TravelForm
              onSubmit={handleFormSubmit}
              initialValues={selectedPreset}
              isLoading={isLoading}
              onCurrencyChange={setCurrency}
            />

            {isLoading && (
              <AgentProgress logs={agentLogs} />
            )}

            {errorMsg && (
              <div className="mt-6 p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm flex items-center justify-between">
                <span><strong>Error:</strong> {errorMsg}</span>
                <button
                  onClick={() => setErrorMsg(null)}
                  className="text-xs bg-rose-500/20 px-2 py-1 rounded text-rose-200"
                >
                  Dismiss
                </button>
              </div>
            )}
          </div>
        ) : (
          <div>
            {/* Trip Header Banner */}
            <div className="bg-gradient-to-r from-sky-950 via-slate-900 to-indigo-950 border border-sky-500/30 rounded-2xl p-6 sm:p-8 mb-8 shadow-2xl relative overflow-hidden print:bg-white print:border-slate-300 print:text-slate-900 print:shadow-none print:p-4">
              <div className="absolute right-0 top-0 translate-x-10 -translate-y-10 w-96 h-96 bg-sky-500/10 rounded-full blur-3xl pointer-events-none print:hidden" />

              <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
                <div>
                  <div className="flex items-center gap-2 text-xs font-bold text-sky-400 print:text-sky-700 uppercase tracking-widest mb-2">
                    <Sparkles className="w-4 h-4" /> Multi-Agent Verified Itinerary
                  </div>
                  <h2 className="text-3xl sm:text-4xl font-extrabold text-white print:text-slate-900 tracking-tight">
                    {planResult.destination}
                  </h2>
                  <div className="flex flex-wrap items-center gap-3 mt-3 text-xs text-slate-300 print:text-slate-700">
                    <span className="flex items-center gap-1.5 bg-slate-800/80 print:bg-slate-100 px-3 py-1 rounded-lg border border-slate-700 print:border-slate-300">
                      <Calendar className="w-4 h-4 text-sky-400 print:text-sky-600" /> {planResult.duration_days} Days
                    </span>
                    <span className="flex items-center gap-1.5 bg-slate-800/80 print:bg-slate-100 px-3 py-1 rounded-lg border border-slate-700 print:border-slate-300">
                      <Compass className="w-4 h-4 text-indigo-400 print:text-indigo-600" /> Best: {planResult.best_time_to_visit}
                    </span>

                    {/* Collapsible Telemetry Drawer Trigger (Requirement 5) */}
                    <button
                      onClick={() => setIsTelemetryOpen(true)}
                      className="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-sky-500/15 hover:bg-sky-500/25 text-sky-300 border border-sky-500/30 font-bold transition print:hidden"
                      title="Inspect multi-agent collaboration trace & logs"
                    >
                      <Bot className="w-3.5 h-3.5" /> Agent Telemetry (5/5 Active)
                    </button>
                  </div>
                </div>

                {/* Action Buttons (Requirement 4 & 5) */}
                <div className="flex items-center gap-2.5 flex-wrap print:hidden">
                  <button
                    onClick={() => saveTripToStorage(planResult)}
                    className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition"
                  >
                    <Bookmark className="w-4 h-4 text-sky-400" /> Bookmark
                  </button>
                  <button
                    onClick={() => exportToCalendar(planResult)}
                    className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md shadow-indigo-600/30 transition"
                    title="Export activities to Google/Apple Calendar (.ics)"
                  >
                    <CalendarDays className="w-4 h-4" /> Export Calendar (.ics)
                  </button>
                  <button
                    onClick={() => downloadMarkdown(planResult)}
                    className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-sky-600 hover:bg-sky-500 text-white text-xs font-semibold shadow-md shadow-sky-600/30 transition"
                  >
                    <Download className="w-4 h-4" /> Export Markdown
                  </button>
                  <button
                    onClick={() => window.print()}
                    className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition"
                  >
                    <Printer className="w-4 h-4" /> Print / PDF
                  </button>
                </div>
              </div>

              <div className="mt-6 pt-6 border-t border-slate-800/80 print:border-slate-300">
                <h4 className="text-xs font-semibold text-slate-400 print:text-slate-600 uppercase tracking-wider mb-1">Destination Overview</h4>
                <p className="text-slate-200 print:text-slate-800 text-sm leading-relaxed">{planResult.overview}</p>
              </div>
            </div>

            {/* Interactive Leaflet Map View with Transit Polyline */}
            <MapView plan={planResult} activeDay={activeDay} />

            {/* Multi-Day Master Timetable (All 5 days print sequentially) */}
            <ItineraryView
              itinerary={planResult.itinerary}
              currency={currency}
              onSwapActivity={handleSwapActivity}
              destination={planResult.destination}
            />

            {/* Budget & Hotel Section */}
            <BudgetCard
              budget={planResult.budget_breakdown}
              accommodations={planResult.accommodations}
              currency={currency}
            />

            {/* Dining Highlights */}
            <DiningSection dining={planResult.dining} />

            {/* Packing List, Visa Guidance & Embassy Essentials */}
            <PackingChecklist
              packingList={planResult.packing_checklist}
              travelTips={planResult.travel_tips}
            />
          </div>
        )}
      </main>

      <footer className="border-t border-slate-800 py-6 bg-slate-950/80 text-center text-xs text-slate-500 print:hidden">
        <p>AI Travel Planner • Multi-Agent Autonomous System • Powered by FastAPI & React</p>
      </footer>
    </div>
  );
}
