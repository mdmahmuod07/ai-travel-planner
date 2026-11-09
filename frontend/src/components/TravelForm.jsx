import React, { useState, useEffect } from 'react';
import { MapPin, Calendar, DollarSign, Users, Compass, Utensils, Send, Sparkles, Coins, Navigation } from 'lucide-react';
import { CURRENCY_RATES, formatCurrencyValue } from './CurrencySelector';
import CityAutocomplete from './CityAutocomplete';

const BUDGET_PRESET_CHIPS = [
  { label: '₹30,000', value: 30000, tier: 'Budget' },
  { label: '₹50,000', value: 50000, tier: 'Budget' },
  { label: '₹1,00,000', value: 100000, tier: 'Moderate' },
  { label: '₹2,00,000', value: 200000, tier: 'Luxury' },
  { label: 'Custom', value: null, tier: null }
];

export default function TravelForm({ onSubmit, initialValues, isLoading, onCurrencyChange }) {
  const [formData, setFormData] = useState({
    destination: 'Tokyo, Japan',
    origin: 'Bangalore, India',
    duration_days: 5,
    target_budget: 50000,
    currency: 'INR',
    travel_style: 'Budget',
    budget: 'Budget',
    companions: 'Couple',
    dietary_restrictions: ['Vegetarian'],
    interests: ['Food', 'History', 'Nature'],
    special_requests: ''
  });

  const [activeChip, setActiveChip] = useState('₹50,000');

  useEffect(() => {
    if (initialValues) {
      setFormData(prev => ({
        ...prev,
        ...initialValues,
        target_budget: initialValues.target_budget !== undefined ? initialValues.target_budget : prev.target_budget,
        currency: initialValues.currency || prev.currency || 'INR',
        travel_style: initialValues.travel_style || initialValues.budget || prev.travel_style
      }));

      // Match preset chip
      if (initialValues.target_budget) {
        const found = BUDGET_PRESET_CHIPS.find(c => c.value === initialValues.target_budget);
        setActiveChip(found ? found.label : 'Custom');
      }
    }
  }, [initialValues]);

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (field === 'currency' && onCurrencyChange) {
      onCurrencyChange(value);
    }
  };

  const handleChipSelect = (chip) => {
    setActiveChip(chip.label);
    if (chip.value !== null) {
      setFormData(prev => ({
        ...prev,
        target_budget: chip.value,
        travel_style: chip.tier || prev.travel_style,
        budget: chip.tier || prev.budget
      }));
    } else {
      // Custom mode: Keep current or set focus
    }
  };

  const handleBudgetNumberChange = (valStr) => {
    const num = valStr === '' ? '' : parseFloat(valStr);
    setFormData(prev => ({
      ...prev,
      target_budget: num
    }));
    const found = BUDGET_PRESET_CHIPS.find(c => c.value === num);
    setActiveChip(found ? found.label : 'Custom');
  };

  const toggleDietary = (item) => {
    setFormData(prev => {
      const exists = prev.dietary_restrictions.includes(item);
      const updated = exists
        ? prev.dietary_restrictions.filter(d => d !== item)
        : [...prev.dietary_restrictions, item];
      return { ...prev, dietary_restrictions: updated };
    });
  };

  const toggleInterest = (item) => {
    setFormData(prev => {
      const exists = prev.interests.includes(item);
      const updated = exists
        ? prev.interests.filter(i => i !== item)
        : [...prev.interests, item];
      return { ...prev, interests: updated };
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.destination.trim()) return;
    const finalData = {
      ...formData,
      target_budget: formData.target_budget ? Number(formData.target_budget) : null,
      budget: formData.travel_style
    };
    onSubmit(finalData);
  };

  const dietaryOptions = ['Vegetarian', 'Vegan', 'Halal', 'Kosher', 'Gluten-Free', 'Dairy-Free', 'Nut Allergy'];
  const interestOptions = ['Food', 'History', 'Art', 'Nature', 'Shopping', 'Nightlife', 'Relaxation', 'Anime & Tech'];

  return (
    <div className="bg-slate-800/60 border border-slate-700/80 rounded-2xl p-6 sm:p-8 backdrop-blur-md shadow-xl print:hidden">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          <Compass className="w-6 h-6 text-sky-400" /> Plan Your Next Journey
        </h2>
        <p className="text-slate-400 text-sm mt-1">
          Customize your budget and preferences; our 5 specialized AI agents will orchestrate a verified, authentic itinerary.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Destination & Origin Typeahead Autocomplete */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Destination City / Country *
            </label>
            <CityAutocomplete
              value={formData.destination}
              onChange={(val) => handleChange('destination', val)}
              placeholder="e.g. Istanbul, Turkey or Tokyo, Japan"
              required={true}
              icon={MapPin}
              iconColor="text-sky-400"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Departing From (Origin)
            </label>
            <CityAutocomplete
              value={formData.origin}
              onChange={(val) => handleChange('origin', val)}
              placeholder="e.g. Bangalore, India"
              required={false}
              icon={Navigation}
              iconColor="text-emerald-400"
            />
          </div>
        </div>

        {/* Total Budget & Currency Section (Requirement 1) */}
        <div className="bg-slate-900/90 border border-slate-700/90 rounded-xl p-4 sm:p-5">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-3">
            <div>
              <label className="block text-xs font-bold text-emerald-400 uppercase tracking-wider">
                Total Trip Budget & Currency *
              </label>
              <p className="text-[11px] text-slate-400">Strict ceiling enforced across lodging, dining, transit & sightseeing.</p>
            </div>
            
            {/* Currency Dropdown */}
            <div className="flex items-center gap-2 bg-slate-800 border border-slate-700 px-3 py-1.5 rounded-lg shrink-0">
              <Coins className="w-4 h-4 text-emerald-400" />
              <span className="text-xs text-slate-400 font-semibold">Currency:</span>
              <select
                value={formData.currency}
                onChange={(e) => handleChange('currency', e.target.value)}
                className="bg-transparent text-xs font-bold text-emerald-300 focus:outline-none cursor-pointer"
              >
                {Object.keys(CURRENCY_RATES).map(code => (
                  <option key={code} value={code} className="bg-slate-900 text-slate-100">
                    {CURRENCY_RATES[code].label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Quick Preset Chips */}
          <div className="flex flex-wrap items-center gap-2 mb-3">
            <span className="text-xs text-slate-400 font-medium">Quick Select:</span>
            {BUDGET_PRESET_CHIPS.map(chip => (
              <button
                type="button"
                key={chip.label}
                onClick={() => handleChipSelect(chip)}
                className={`px-3 py-1 rounded-lg text-xs font-semibold border transition ${
                  activeChip === chip.label
                    ? 'bg-emerald-500 text-slate-950 border-emerald-400 shadow-sm shadow-emerald-500/20 font-bold'
                    : 'bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-600'
                }`}
              >
                {chip.label}
              </button>
            ))}
          </div>

          {/* Numerical Input Field */}
          <div className="relative">
            <span className="absolute left-3.5 top-2.5 text-base font-bold text-emerald-400">
              {CURRENCY_RATES[formData.currency]?.symbol || '₹'}
            </span>
            <input
              type="number"
              min="5000"
              step="1000"
              required
              value={formData.target_budget !== null && formData.target_budget !== undefined ? formData.target_budget : ''}
              onChange={(e) => handleBudgetNumberChange(e.target.value)}
              placeholder="e.g. 50000"
              className="w-full bg-slate-950 border border-slate-700 focus:border-emerald-500 rounded-xl py-2.5 pl-9 pr-24 text-slate-100 font-mono text-base font-bold placeholder-slate-600 focus:outline-none transition"
            />
            <span className="absolute right-3.5 top-3 text-xs text-slate-400 font-semibold uppercase">
              {formData.currency} Ceiling
            </span>
          </div>

          {formData.target_budget && (
            <div className="mt-2 text-xs text-slate-400 flex items-center justify-between">
              <span>
                Daily Allocation: ~{formatCurrencyValue(Math.round(formData.target_budget / formData.duration_days), formData.currency)} / day
              </span>
              <span className="text-emerald-400 font-medium">
                {formData.target_budget <= 60000 && formData.currency === 'INR'
                  ? 'Capsule hotels, hostels & budget business inns recommended'
                  : formData.target_budget <= 150000 && formData.currency === 'INR'
                  ? '3-4 Star comfort & boutique hotels recommended'
                  : 'Luxury boutique hotels & premier stays recommended'}
              </span>
            </div>
          )}
        </div>

        {/* Duration, Travel Style & Companions */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
                Duration
              </label>
              <span className="text-xs font-bold text-sky-400">{formData.duration_days} Days</span>
            </div>
            <input
              type="range"
              min="1"
              max="21"
              value={formData.duration_days}
              onChange={(e) => handleChange('duration_days', parseInt(e.target.value, 10))}
              className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-sky-500 mt-2"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Travel Style / Tier
            </label>
            <div className="grid grid-cols-3 gap-1 bg-slate-900 p-1 rounded-xl border border-slate-700">
              {['Budget', 'Moderate', 'Luxury'].map((style) => (
                <button
                  type="button"
                  key={style}
                  onClick={() => {
                    handleChange('travel_style', style);
                    handleChange('budget', style);
                  }}
                  className={`py-1.5 text-xs font-semibold rounded-lg transition ${
                    formData.travel_style === style
                      ? 'bg-sky-600 text-white shadow-md'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {style}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Companions
            </label>
            <select
              value={formData.companions}
              onChange={(e) => handleChange('companions', e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl py-2.5 px-3 text-slate-100 focus:outline-none focus:border-sky-500 text-sm"
            >
              <option value="Solo">Solo Traveler</option>
              <option value="Couple">Couple / Partners</option>
              <option value="Family">Family with Kids</option>
              <option value="Friends">Group of Friends</option>
            </select>
          </div>
        </div>

        {/* Interests Selection */}
        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
            Trip Interests & Highlights
          </label>
          <div className="flex flex-wrap gap-2">
            {interestOptions.map(interest => {
              const active = formData.interests.includes(interest);
              return (
                <button
                  type="button"
                  key={interest}
                  onClick={() => toggleInterest(interest)}
                  className={`px-3 py-1.5 text-xs font-medium rounded-lg border transition ${
                    active
                      ? 'bg-sky-500/20 border-sky-500/50 text-sky-300'
                      : 'bg-slate-900/60 border-slate-700/60 text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {interest}
                </button>
              );
            })}
          </div>
        </div>

        {/* Dietary Preferences */}
        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
            Dietary Preferences
          </label>
          <div className="flex flex-wrap gap-2">
            {dietaryOptions.map(diet => {
              const active = formData.dietary_restrictions.includes(diet);
              return (
                <button
                  type="button"
                  key={diet}
                  onClick={() => toggleDietary(diet)}
                  className={`px-3 py-1.5 text-xs font-medium rounded-lg border transition ${
                    active
                      ? 'bg-emerald-500/20 border-emerald-500/50 text-emerald-300'
                      : 'bg-slate-900/60 border-slate-700/60 text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {diet}
                </button>
              );
            })}
          </div>
        </div>

        {/* Special Requests */}
        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
            Special Requests / Notes (Optional)
          </label>
          <textarea
            rows="2"
            value={formData.special_requests}
            onChange={(e) => handleChange('special_requests', e.target.value)}
            placeholder="e.g. Prefer Japanese bullet trains (Shinkansen), quiet boutique stays, want slow-paced mornings..."
            className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-sky-500 transition text-sm"
          />
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full py-3.5 px-6 rounded-xl bg-gradient-to-r from-emerald-500 via-sky-600 to-indigo-600 hover:from-emerald-400 hover:to-indigo-500 text-white font-bold text-base shadow-lg shadow-sky-500/25 flex items-center justify-center gap-2 transition disabled:opacity-50"
        >
          {isLoading ? (
            <>
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              Agents Orchestrating Itinerary...
            </>
          ) : (
            <>
              <Send className="w-5 h-5" /> Generate Multi-Agent Travel Plan
            </>
          )}
        </button>
      </form>
    </div>
  );
}
