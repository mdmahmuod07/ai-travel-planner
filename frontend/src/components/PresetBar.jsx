import React from 'react';
import { Sparkles, Calendar, Tag } from 'lucide-react';
import { formatCurrencyValue } from './CurrencySelector';

export default function PresetBar({ presets, onSelect }) {
  if (!presets || presets.length === 0) return null;

  return (
    <div className="mb-8 print:hidden">
      <div className="flex items-center gap-2 mb-3">
        <Sparkles className="w-4 h-4 text-sky-400" />
        <h3 className="text-sm font-semibold text-slate-300">Quick Start Presets</h3>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {presets.map((preset, idx) => (
          <button
            key={idx}
            onClick={() => onSelect(preset)}
            className="p-3.5 rounded-xl bg-slate-800/60 hover:bg-slate-800 border border-slate-700/60 hover:border-sky-500/50 text-left transition group shadow-sm flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-1.5 flex-wrap gap-1">
                <span className="text-[11px] font-semibold px-2 py-0.5 rounded bg-sky-500/10 text-sky-400 border border-sky-500/20">
                  {preset.travel_style || preset.budget}
                </span>
                <span className="text-xs text-slate-400 flex items-center gap-1">
                  <Calendar className="w-3 h-3" /> {preset.duration_days} Days
                </span>
              </div>
              <h4 className="font-semibold text-slate-100 group-hover:text-sky-400 transition text-sm">
                {preset.title}
              </h4>
            </div>
            <div className="mt-2 pt-2 border-t border-slate-700/50 flex items-center justify-between text-xs">
              <span className="text-slate-400 text-[11px] truncate">{preset.companions}</span>
              {preset.target_budget && (
                <span className="text-emerald-400 font-bold text-xs">
                  {formatCurrencyValue(preset.target_budget, preset.currency || 'INR')}
                </span>
              )}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
