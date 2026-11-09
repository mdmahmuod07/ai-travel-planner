import React from 'react';
import { Bookmark, Trash2, Calendar, MapPin, ExternalLink, X } from 'lucide-react';

export function saveTripToStorage(plan) {
  if (!plan || !plan.trip_id) return;
  const saved = JSON.parse(localStorage.getItem('ai_travel_saved_trips') || '[]');
  const exists = saved.some(t => t.trip_id === plan.trip_id);
  if (!exists) {
    saved.unshift({
      ...plan,
      saved_at: new Date().toLocaleDateString()
    });
    localStorage.setItem('ai_travel_saved_trips', JSON.stringify(saved.slice(0, 10)));
  }
}

export function getSavedTrips() {
  return JSON.parse(localStorage.getItem('ai_travel_saved_trips') || '[]');
}

export function deleteSavedTrip(tripId) {
  const saved = getSavedTrips().filter(t => t.trip_id !== tripId);
  localStorage.setItem('ai_travel_saved_trips', JSON.stringify(saved));
  return saved;
}

export default function SavedTripsDrawer({ isOpen, onClose, onLoadTrip }) {
  const [trips, setTrips] = React.useState(getSavedTrips());

  React.useEffect(() => {
    if (isOpen) {
      setTrips(getSavedTrips());
    }
  }, [isOpen]);

  const handleDelete = (e, tripId) => {
    e.stopPropagation();
    const updated = deleteSavedTrip(tripId);
    setTrips(updated);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-sm flex justify-end transition-opacity">
      <div className="w-full max-w-md bg-slate-900 border-l border-slate-800 h-full p-6 overflow-y-auto flex flex-col justify-between shadow-2xl">
        <div>
          <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
            <div className="flex items-center gap-2">
              <Bookmark className="w-5 h-5 text-sky-400" />
              <h3 className="text-lg font-bold text-white">Saved Itineraries</h3>
            </div>
            <button
              onClick={onClose}
              className="p-1 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {trips.length === 0 ? (
            <div className="text-center py-12 text-slate-500 text-sm">
              <p>No saved trips yet.</p>
              <p className="text-xs mt-1">Generate a plan and bookmark it to access it anytime!</p>
            </div>
          ) : (
            <div className="space-y-3">
              {trips.map(t => (
                <div
                  key={t.trip_id}
                  onClick={() => {
                    onLoadTrip(t);
                    onClose();
                  }}
                  className="p-4 rounded-xl bg-slate-800/80 border border-slate-700/80 hover:border-sky-500/50 cursor-pointer transition group flex justify-between items-start"
                >
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xs font-bold text-sky-400 uppercase tracking-wider">{t.destination}</span>
                      <span className="text-[10px] px-2 py-0.5 rounded bg-slate-700 text-slate-300">
                        {t.duration_days} Days
                      </span>
                    </div>
                    <p className="text-xs text-slate-300 line-clamp-1">{t.overview}</p>
                    <span className="text-[10px] text-slate-500 block mt-2">Saved on {t.saved_at || 'Recently'}</span>
                  </div>

                  <button
                    onClick={(e) => handleDelete(e, t.trip_id)}
                    className="p-1.5 text-slate-500 hover:text-rose-400 hover:bg-slate-700 rounded-lg transition"
                    title="Delete saved trip"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        <button
          onClick={onClose}
          className="w-full py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-semibold mt-6 transition"
        >
          Close Drawer
        </button>
      </div>
    </div>
  );
}
