import React from 'react';
import { Compass, Bot, RefreshCw, Bookmark } from 'lucide-react';
import CurrencySelector from './CurrencySelector';

export default function Header({ onReset, hasPlan, onOpenDrawer, currentCurrency, onCurrencyChange }) {
  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex items-center justify-between flex-wrap gap-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-sky-500/20">
            <Compass className="w-6 h-6 text-white animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold text-white tracking-tight">AI Travel Planner</h1>
              <span className="px-2 py-0.5 text-xs font-semibold rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/20 flex items-center gap-1">
                <Bot className="w-3 h-3" /> Multi-Agent 2.0
              </span>
            </div>
            <p className="text-xs text-slate-400">Autonomous Collaborative Trip Architect</p>
          </div>
        </div>

        <div className="flex items-center gap-3 flex-wrap">
          <CurrencySelector
            currentCurrency={currentCurrency}
            onCurrencyChange={onCurrencyChange}
          />

          <button
            onClick={onOpenDrawer}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition"
          >
            <Bookmark className="w-3.5 h-3.5 text-sky-400" />
            Saved Trips
          </button>

          {hasPlan && (
            <button
              onClick={onReset}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              New Trip
            </button>
          )}
        </div>
      </div>
    </header>
  );
}
