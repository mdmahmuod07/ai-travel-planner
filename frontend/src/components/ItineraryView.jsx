import React, { useState } from 'react';
import { Calendar, Clock, MapPin, Lightbulb, Sun, Sunset, Moon, RefreshCw, CheckCircle2, ExternalLink } from 'lucide-react';
import { convertAmount } from './CurrencySelector';

export default function ItineraryView({ itinerary, currency, onSwapActivity, destination = '' }) {
  const [activeDay, setActiveDay] = useState(1);

  if (!itinerary || itinerary.length === 0) return null;

  const getTimeIcon = (slot) => {
    const s = slot.toLowerCase();
    if (s.includes('morning')) return <Sun className="w-4 h-4 text-amber-400 shrink-0" />;
    if (s.includes('afternoon')) return <Sunset className="w-4 h-4 text-orange-400 shrink-0" />;
    return <Moon className="w-4 h-4 text-indigo-400 shrink-0" />;
  };

  return (
    <div className="bg-slate-800/60 border border-slate-700 rounded-2xl p-6 shadow-xl mb-8 print:bg-white print:border-slate-300 print:shadow-none print:p-2">
      {/* Header & Tabs */}
      <div className="flex items-center justify-between mb-6 flex-wrap gap-3">
        <div>
          <h3 className="text-xl font-bold text-white print:text-slate-900 flex items-center gap-2">
            <Calendar className="w-5 h-5 text-sky-400 print:text-sky-600" /> Day-by-Day Master Schedule
          </h3>
          <p className="text-xs text-slate-400 print:text-slate-600 mt-0.5">
            Geographically clustered by authentic wards to eliminate transit fatigue.
          </p>
        </div>

        {/* Day Navigation Tabs (Hidden on Print) */}
        <div className="flex items-center gap-1 bg-slate-900 p-1.5 rounded-xl border border-slate-700 overflow-x-auto max-w-full print:hidden">
          {itinerary.map((day) => (
            <button
              key={day.day_number}
              onClick={() => setActiveDay(day.day_number)}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition ${
                activeDay === day.day_number
                  ? 'bg-sky-600 text-white shadow-md'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
              }`}
            >
              Day {day.day_number}
            </button>
          ))}
        </div>
      </div>

      {/* Sequential Multi-Day Renderer (Active day shown on screen; ALL days rendered on print) */}
      <div className="space-y-8 print:space-y-6">
        {itinerary.map((day) => {
          const isCurrentActive = activeDay === day.day_number;

          return (
            <div
              key={day.day_number}
              className={`${
                isCurrentActive ? 'block' : 'hidden'
              } print:!block print:mb-8 print:break-inside-avoid print:page-break-inside-avoid`}
            >
              {/* Day Banner */}
              <div className="bg-gradient-to-r from-sky-900/40 to-slate-900 border border-sky-500/20 rounded-xl p-4 mb-4 flex items-center justify-between flex-wrap gap-3 print:bg-slate-100 print:border-slate-300 print:text-slate-900">
                <div>
                  <div className="flex items-center gap-2 text-xs text-sky-400 print:text-sky-700 font-bold uppercase tracking-wider">
                    <span>Day {day.day_number}</span> • <span>{day.theme}</span>
                  </div>
                  <p className="text-sm text-slate-200 print:text-slate-700 mt-1">{day.summary}</p>
                </div>
                <div className="bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700 text-xs font-semibold text-slate-300 print:bg-white print:border-slate-300 print:text-slate-800">
                  Daily Budget: <span className="text-emerald-400 print:text-emerald-700 font-bold">{convertAmount(day.daily_estimated_cost, currency)}</span>
                </div>
              </div>

              {/* Activities List */}
              <div className="space-y-3.5">
                {day.activities.map((act, idx) => (
                  <div
                    key={idx}
                    className="p-4 rounded-xl bg-slate-900/80 border border-slate-700/70 hover:border-slate-600 transition flex flex-col sm:flex-row gap-4 print:bg-white print:border-slate-200 print:p-3"
                  >
                    {/* Time Slot & Duration */}
                    <div className="sm:w-36 shrink-0 flex sm:flex-col items-center sm:items-start justify-between sm:justify-start gap-2 border-b sm:border-b-0 sm:border-r border-slate-800 print:border-slate-200 pb-2 sm:pb-0 sm:pr-4">
                      <span className="px-2.5 py-1 rounded-md bg-slate-800 border border-slate-700 text-slate-200 text-xs font-semibold flex items-center gap-1.5 print:bg-slate-100 print:border-slate-300 print:text-slate-800">
                        {getTimeIcon(act.time_slot)}
                        {act.time_slot}
                      </span>
                      <span className="text-xs text-slate-400 print:text-slate-600 flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5" /> {act.duration}
                      </span>
                    </div>

                    {/* Activity Content */}
                    <div className="grow">
                      {(() => {
                        const venueSearch = act.search_query || `${act.venue_name || act.title}, ${destination || act.location || ''}`;
                        const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(venueSearch)}`;

                        return (
                          <>
                            <div className="flex items-start justify-between gap-2 mb-1">
                              <h4 className="text-base font-bold text-white print:text-slate-900 flex items-center gap-2 flex-wrap">
                                <a
                                  href={mapsUrl}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="hover:text-sky-400 hover:underline inline-flex items-center gap-1.5 transition"
                                  title={`Locate ${act.venue_name || act.title} on Google Maps`}
                                >
                                  <span>{act.title}</span>
                                  <ExternalLink className="w-3.5 h-3.5 text-sky-400 opacity-60 hover:opacity-100 print:hidden shrink-0" />
                                </a>
                                {act.category && (
                                  <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700 print:bg-slate-100 print:text-slate-600 print:border-slate-300">
                                    {act.category}
                                  </span>
                                )}
                              </h4>
                              <div className="flex items-center gap-2 shrink-0">
                                <span className="text-xs font-bold text-emerald-400 print:text-emerald-700 bg-emerald-500/10 px-2.5 py-0.5 rounded border border-emerald-500/20 print:border-emerald-300">
                                  {convertAmount(act.estimated_cost, currency)}
                                </span>
                                {onSwapActivity && (
                                  <button
                                    onClick={() => onSwapActivity(day.day_number, idx)}
                                    className="p-1 text-slate-400 hover:text-sky-400 hover:bg-slate-800 rounded transition print:hidden"
                                    title="Swap this activity with an authentic alternative"
                                  >
                                    <RefreshCw className="w-3.5 h-3.5" />
                                  </button>
                                )}
                              </div>
                            </div>

                            {act.venue_name && (
                              <div className="text-xs font-semibold text-sky-300 print:text-sky-800 mb-1 flex items-center gap-1.5">
                                <a
                                  href={mapsUrl}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="hover:text-sky-200 hover:underline transition"
                                  title={`Open ${act.venue_name} in Google Maps`}
                                >
                                  <span>🏛️ {act.venue_name}</span>
                                </a>
                                {act.neighborhood && (
                                  <span className="text-[11px] text-slate-400 print:text-slate-600 font-normal">
                                    • {act.neighborhood}
                                  </span>
                                )}
                              </div>
                            )}

                            <p className="text-xs text-slate-400 print:text-slate-600 flex items-center gap-1 mb-2">
                              <MapPin className="w-3.5 h-3.5 text-sky-400 print:text-sky-600 shrink-0" />
                              <span className="text-slate-300 print:text-slate-800 font-medium">{act.location}</span>
                            </p>

                            <p className="text-xs text-slate-300 print:text-slate-700 leading-relaxed">{act.description}</p>

                            {act.tips && (
                              <div className="mt-3 p-2.5 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-300 print:bg-amber-50 print:border-amber-300 print:text-amber-900 text-xs flex items-start gap-2">
                                <Lightbulb className="w-4 h-4 shrink-0 text-amber-400 print:text-amber-700 mt-0.5" />
                                <span><strong>Insider Tip:</strong> {act.tips}</span>
                              </div>
                            )}

                            {(act.search_query || act.location) && (
                              <div className="mt-2.5">
                                <a
                                  href={mapsUrl}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="inline-flex items-center gap-1 text-[11px] text-sky-400 hover:text-sky-300 print:hidden font-medium underline"
                                >
                                  <ExternalLink className="w-3 h-3" /> Open in Google Maps ↗
                                </a>
                              </div>
                            )}
                          </>
                        );
                      })()}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
