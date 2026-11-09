import React from 'react';
import { Hotel, Star, MapPin, CheckCircle, ShieldCheck, Wallet } from 'lucide-react';
import { convertAmount } from './CurrencySelector';

export default function BudgetCard({ budget, accommodations, currency = 'INR' }) {
  if (!budget && (!accommodations || accommodations.length === 0)) return null;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8 print:break-inside-avoid">
      {/* Budget Breakdown Summary */}
      {budget && (
        <div className="bg-slate-800/60 border border-slate-700 rounded-2xl p-6 shadow-xl flex flex-col justify-between print:bg-white print:border-slate-300 print:text-slate-900">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-white print:text-slate-900 flex items-center gap-2">
                <Wallet className="w-5 h-5 text-emerald-400 print:text-emerald-600" /> Estimated Budget
              </h3>
              <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 print:text-emerald-700 border border-emerald-500/20 print:border-emerald-300">
                {currency} Projection
              </span>
            </div>

            <div className="space-y-3 text-xs mb-6">
              <div className="flex justify-between py-1.5 border-b border-slate-700/60 print:border-slate-200">
                <span className="text-slate-400 print:text-slate-600">Lodging & Accommodation</span>
                <span className="font-semibold text-slate-200 print:text-slate-900">{convertAmount(budget.accommodation, currency)}</span>
              </div>
              <div className="flex justify-between py-1.5 border-b border-slate-700/60 print:border-slate-200">
                <span className="text-slate-400 print:text-slate-600">Food & Local Dining</span>
                <span className="font-semibold text-slate-200 print:text-slate-900">{convertAmount(budget.dining, currency)}</span>
              </div>
              <div className="flex justify-between py-1.5 border-b border-slate-700/60 print:border-slate-200">
                <span className="text-slate-400 print:text-slate-600">Activities & Attractions</span>
                <span className="font-semibold text-slate-200 print:text-slate-900">{convertAmount(budget.activities_and_tours, currency)}</span>
              </div>
              <div className="flex justify-between py-1.5 border-b border-slate-700/60 print:border-slate-200">
                <span className="text-slate-400 print:text-slate-600">Local Transit & Metro</span>
                <span className="font-semibold text-slate-200 print:text-slate-900">{convertAmount(budget.local_transport, currency)}</span>
              </div>
              <div className="flex justify-between py-1.5 border-b border-slate-700/60 print:border-slate-200">
                <span className="text-slate-400 print:text-slate-600">Emergency & Shopping</span>
                <span className="font-semibold text-slate-200 print:text-slate-900">{convertAmount(budget.miscellaneous, currency)}</span>
              </div>
            </div>
          </div>

          <div>
            <div className="bg-slate-900 p-4 rounded-xl border border-slate-700/80 print:bg-slate-100 print:border-slate-300 mb-3">
              <div className="flex justify-between items-center">
                <span className="text-xs font-bold text-slate-400 print:text-slate-600 uppercase tracking-wider">Total Estimated Trip Cost</span>
                <span className="text-xl font-extrabold text-emerald-400 print:text-emerald-700">{convertAmount(budget.total_estimated, currency)}</span>
              </div>
            </div>

            {budget.saving_tips && budget.saving_tips.length > 0 && (
              <div className="text-[11px] text-slate-400 print:text-slate-600 space-y-1">
                <span className="font-semibold text-slate-300 print:text-slate-700 flex items-center gap-1">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-400 print:text-emerald-600" /> Budget Optimization:
                </span>
                <p className="line-clamp-2">{budget.saving_tips[0]}</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Accommodations List */}
      {accommodations && accommodations.length > 0 && (
        <div className="lg:col-span-2 bg-slate-800/60 border border-slate-700 rounded-2xl p-6 shadow-xl print:bg-white print:border-slate-300">
          <h3 className="text-lg font-bold text-white print:text-slate-900 flex items-center gap-2 mb-4">
            <Hotel className="w-5 h-5 text-sky-400 print:text-sky-600" /> Recommended Stay Options
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {accommodations.map((hotel, idx) => (
              <div
                key={idx}
                className="p-4 rounded-xl bg-slate-900/80 border border-slate-700/70 hover:border-sky-500/40 transition flex flex-col justify-between print:bg-slate-50 print:border-slate-200"
              >
                <div>
                  <div className="flex items-start justify-between gap-2 mb-1">
                    <h4 className="text-sm font-bold text-white print:text-slate-900 leading-snug">{hotel.name}</h4>
                    <span className="text-xs font-semibold px-2 py-0.5 rounded bg-amber-500/10 text-amber-300 print:text-amber-800 border border-amber-500/20 print:border-amber-300 flex items-center gap-1 shrink-0">
                      <Star className="w-3 h-3 fill-amber-400 text-amber-400" /> {hotel.rating}
                    </span>
                  </div>
                  <p className="text-xs text-sky-400 print:text-sky-600 font-medium flex items-center gap-1 mb-2">
                    <MapPin className="w-3 h-3" /> {hotel.neighborhood} • <span className="text-slate-400 print:text-slate-600">{hotel.type}</span>
                  </p>
                  <p className="text-xs text-slate-300 print:text-slate-700 mb-3">{hotel.why_recommended}</p>
                </div>

                <div className="pt-2 border-t border-slate-800 print:border-slate-200 flex items-center justify-between">
                  <span className="text-xs text-slate-400 print:text-slate-600">Est. Price:</span>
                  <span className="text-xs font-bold text-emerald-400 print:text-emerald-700">{convertAmount(hotel.price_per_night, currency)}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
