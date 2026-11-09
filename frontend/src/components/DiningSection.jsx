import React from 'react';
import { Utensils } from 'lucide-react';

export default function DiningSection({ dining }) {
  if (!dining || dining.length === 0) return null;

  return (
    <div className="bg-slate-800/60 border border-slate-700 rounded-2xl p-6 shadow-xl mb-8 print:bg-white print:border-slate-300 print:text-slate-900 print:break-inside-avoid">
      <div className="flex items-center justify-between mb-6 flex-wrap gap-2">
        <div>
          <h3 className="text-lg font-bold text-white print:text-slate-900 flex items-center gap-2">
            <Utensils className="w-5 h-5 text-rose-400 print:text-rose-600" /> Dining & Culinary Highlights
          </h3>
          <p className="text-xs text-slate-400 print:text-slate-600 mt-0.5">
            Authentic ward-based eateries with verified dietary tags.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {dining.map((item, idx) => (
          <div
            key={idx}
            className="p-4 rounded-xl bg-slate-900/80 border border-slate-700/70 hover:border-rose-500/30 transition flex flex-col justify-between print:bg-slate-50 print:border-slate-200"
          >
            <div>
              <div className="flex items-start justify-between gap-2 mb-1">
                <h4 className="text-sm font-bold text-white print:text-slate-900">{item.name}</h4>
                <span className="text-xs font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 shrink-0 print:bg-white print:border-slate-300 print:text-slate-800">
                  {item.price_range}
                </span>
              </div>
              <p className="text-xs text-rose-400 print:text-rose-600 font-medium mb-2">
                {item.cuisine} • <span className="text-slate-400 print:text-slate-600">{item.neighborhood}</span>
              </p>

              <div className="p-2.5 rounded-lg bg-slate-800/80 border border-slate-700/60 mb-3 print:bg-white print:border-slate-200">
                <span className="text-[11px] uppercase tracking-wider text-slate-400 print:text-slate-500 font-semibold block mb-0.5">Must-Try Specialty</span>
                <span className="text-xs text-slate-200 print:text-slate-800 font-medium">{item.must_try_dish}</span>
              </div>
            </div>

            <div className="flex items-center justify-between pt-2 border-t border-slate-800 print:border-slate-200 text-xs">
              <span className="text-slate-400 print:text-slate-600">Meal: <strong className="text-slate-200 print:text-slate-800">{item.meal_type}</strong></span>
              {item.dietary_friendly && item.dietary_friendly.length > 0 && (
                <div className="flex flex-wrap gap-1">
                  {item.dietary_friendly.map((d, i) => {
                    const isMeat = ['non-vegetarian', 'meat'].includes(d.toLowerCase());
                    return (
                      <span
                        key={i}
                        className={`px-1.5 py-0.5 text-[10px] font-semibold rounded border ${
                          isMeat
                            ? 'bg-rose-500/10 text-rose-300 border-rose-500/20 print:bg-rose-50 print:text-rose-800'
                            : 'bg-emerald-500/10 text-emerald-300 border-emerald-500/20 print:bg-emerald-50 print:text-emerald-800'
                        }`}
                      >
                        {d}
                      </span>
                    );
                  })}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
