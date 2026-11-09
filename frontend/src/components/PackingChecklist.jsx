import React, { useState } from 'react';
import { Luggage, ShieldAlert, CloudSun, CheckSquare, Square, CreditCard, Info, Landmark, Zap, Train } from 'lucide-react';

const CATEGORY_LABEL_MAP = {
  essential_documents: 'Essential Documents & Travel Funds',
  clothing: 'Clothing & Climate-Appropriate Apparel',
  electronics: 'Electronics, Power & Navigation',
  health: 'Health, Medications & Personal Care'
};

const DEFAULT_CATEGORY_FALLBACKS = {
  essential_documents: [
    'Original Passport (valid for 6+ months) & 2 printed photocopies',
    'Official Visa / Travel Authorization documentation & confirmation',
    'Return flight e-tickets and confirmed hotel vouchers',
    'International credit/debit card & modest local cash funds',
    'Comprehensive travel & health insurance policy certificate'
  ],
  clothing: [
    'Comfortable, broken-in walking shoes for cobblestones & monuments',
    'Versatile breathable daytime layers & evening jacket',
    'Modest attire covering shoulders & knees for sacred monuments',
    'Lightweight rain shell or compact travel umbrella'
  ],
  electronics: [
    'Destination-compatible power plug adapter & dual-voltage charger',
    '10,000mAh+ portable power bank for all-day navigation',
    'USB-C / Lightning multi-charging cables',
    'eSIM QR profile activated or local SIM card'
  ],
  health: [
    'Prescription medications in original containers with doctor note',
    'Compact travel first-aid kit (pain relief, antacids, blister bandages)',
    'Broad-spectrum sunscreen (SPF 30+) & moisturizing lip balm',
    'Reusable insulated water bottle'
  ]
};

function normalizeCategories(packingData) {
  if (!packingData) return [];

  let result = [];

  // Case 1: packingData is an Object: { essential_documents: [...], clothing: [...], ... }
  if (!Array.isArray(packingData) && typeof packingData === 'object') {
    result = Object.entries(packingData).map(([key, val]) => {
      const catKey = key.toLowerCase();
      const catName = CATEGORY_LABEL_MAP[catKey] || key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
      const rawItems = Array.isArray(val) ? val : (val ? [val] : []);
      let items = rawItems.map(item => {
        if (typeof item === 'string') return item.trim();
        if (typeof item === 'object' && item !== null) {
          return (item.item || item.name || item.text || item.title || '').trim();
        }
        return String(item).trim();
      }).filter(Boolean);

      if (items.length === 0 && DEFAULT_CATEGORY_FALLBACKS[catKey]) {
        items = DEFAULT_CATEGORY_FALLBACKS[catKey];
      }

      return { category_name: catName, items };
    });
  } else if (Array.isArray(packingData)) {
    // Case 2: packingData is an Array
    result = packingData.map((cat, idx) => {
      if (typeof cat !== 'object' || cat === null) {
        return { category_name: `Category ${idx + 1}`, items: [String(cat)] };
      }

      // Check if cat has any dedicated category key
      for (const [key, label] of Object.entries(CATEGORY_LABEL_MAP)) {
        if (cat[key] && Array.isArray(cat[key]) && cat[key].length > 0) {
          const items = cat[key].map(i => (typeof i === 'object' ? (i?.item || i?.name || String(i)) : String(i)));
          return { category_name: cat.category_name || label, items };
        }
      }

      const catName =
        cat.category_name ||
        cat.name ||
        cat.title ||
        cat.category ||
        (cat.essential_documents && CATEGORY_LABEL_MAP.essential_documents) ||
        (cat.clothing && CATEGORY_LABEL_MAP.clothing) ||
        (cat.electronics && CATEGORY_LABEL_MAP.electronics) ||
        (cat.health && CATEGORY_LABEL_MAP.health) ||
        `Category ${idx + 1}`;

      const rawItems =
        cat.items ||
        cat.checklist ||
        cat.list ||
        cat.essential_documents ||
        cat.clothing ||
        cat.electronics ||
        cat.health ||
        [];

      const itemsList = Array.isArray(rawItems) ? rawItems : [rawItems];
      let items = itemsList
        .map(item => {
          if (typeof item === 'string') return item.trim();
          if (typeof item === 'object' && item !== null) {
            return (item.item || item.name || item.text || item.title || '').trim();
          }
          return String(item || '').trim();
        })
        .filter(Boolean);

      // Match key for default fallback if items are empty
      const matchedKey = Object.keys(DEFAULT_CATEGORY_FALLBACKS).find(k =>
        catName.toLowerCase().includes(k.replace('_', ' ')) || catName.toLowerCase().includes(k)
      );
      if (items.length === 0 && matchedKey) {
        items = DEFAULT_CATEGORY_FALLBACKS[matchedKey];
      }

      return { category_name: catName, items };
    });
  }

  // Ensure items are non-empty
  return result.filter(c => c && c.items && c.items.length > 0);
}

export default function PackingChecklist({ packingList, travelTips }) {
  const [checkedItems, setCheckedItems] = useState({});

  const toggleItem = (itemKey) => {
    setCheckedItems(prev => ({
      ...prev,
      [itemKey]: !prev[itemKey]
    }));
  };

  const categories = normalizeCategories(packingList);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8 print:break-inside-avoid">
      {/* Packing Checklist */}
      {categories.length > 0 && (
        <div className="bg-slate-800/60 border border-slate-700 rounded-2xl p-6 shadow-xl print:bg-white print:border-slate-300 print:text-slate-900">
          <h3 className="text-lg font-bold text-white print:text-slate-900 flex items-center gap-2 mb-4">
            <Luggage className="w-5 h-5 text-indigo-400 print:text-indigo-600" /> Climate & Destination-Aware Packing Checklist
          </h3>

          <div className="space-y-4">
            {categories.map((cat, catIdx) => (
              <div key={catIdx} className="bg-slate-900/80 rounded-xl p-4 border border-slate-700/60 print:bg-slate-50 print:border-slate-200">
                <h4 className="text-xs font-bold text-sky-400 print:text-sky-700 uppercase tracking-wider mb-2.5">
                  {cat.category_name}
                </h4>
                <div className="space-y-2">
                  {cat.items.map((item, itemIdx) => {
                    const key = `${catIdx}-${itemIdx}`;
                    const isChecked = !!checkedItems[key];
                    return (
                      <div
                        role="checkbox"
                        aria-checked={isChecked}
                        tabIndex={0}
                        key={itemIdx}
                        onClick={() => toggleItem(key)}
                        onKeyDown={(e) => {
                          if (e.key === ' ' || e.key === 'Enter') {
                            e.preventDefault();
                            toggleItem(key);
                          }
                        }}
                        className="w-full flex items-start gap-2.5 text-left py-1 text-xs group cursor-pointer select-none print:text-slate-900 focus:outline-none"
                      >
                        {isChecked ? (
                          <CheckSquare className="w-4 h-4 text-emerald-400 print:text-emerald-700 shrink-0 mt-0.5" />
                        ) : (
                          <Square className="w-4 h-4 text-slate-500 print:text-slate-500 group-hover:text-slate-300 shrink-0 mt-0.5" />
                        )}
                        <span className={`transition leading-relaxed ${isChecked ? 'line-through text-slate-500 print:text-slate-400' : 'text-slate-200 print:text-slate-900'}`}>
                          {item}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Travel Safety, Legal & Infrastructure Guide */}
      {travelTips && (
        <div className="bg-slate-800/60 border border-slate-700 rounded-2xl p-6 shadow-xl flex flex-col justify-between print:bg-white print:border-slate-300 print:text-slate-900">
          <div>
            <h3 className="text-lg font-bold text-white print:text-slate-900 flex items-center gap-2 mb-4">
              <ShieldAlert className="w-5 h-5 text-purple-400 print:text-purple-600" /> Travel Safety, Legal & Infrastructure Guide
            </h3>

            <div className="space-y-3.5 text-xs">
              {/* Weather */}
              {travelTips.weather_summary && (
                <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-700/60 print:bg-slate-50 print:border-slate-200">
                  <div className="flex items-center gap-2 font-semibold text-slate-200 print:text-slate-900 mb-1">
                    <CloudSun className="w-4 h-4 text-amber-400 print:text-amber-600" /> Weather Expectations
                  </div>
                  <p className="text-slate-400 print:text-slate-700 leading-relaxed">{travelTips.weather_summary}</p>
                </div>
              )}

              {/* Bilateral Visa & Entry Guidance */}
              {travelTips.visa_and_entry && (
                <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-700/60 print:bg-slate-50 print:border-slate-200">
                  <div className="flex items-center gap-2 font-semibold text-slate-200 print:text-slate-900 mb-1">
                    <Info className="w-4 h-4 text-sky-400 print:text-sky-600" /> Bilateral Visa & Entry Evaluation
                  </div>
                  <p className="text-slate-300 print:text-slate-800 leading-relaxed">{travelTips.visa_and_entry}</p>
                </div>
              )}

              {/* Electrical Standards */}
              {travelTips.electrical_specs && (
                <div className="p-3.5 rounded-xl bg-amber-950/30 border border-amber-500/30 print:bg-amber-50 print:border-amber-200">
                  <div className="flex items-center gap-2 font-semibold text-amber-300 print:text-amber-900 mb-1">
                    <Zap className="w-4 h-4 text-amber-400 print:text-amber-600" /> Electrical Standards & Power Plugs
                  </div>
                  <p className="text-amber-200/90 print:text-amber-900 leading-relaxed font-mono text-[11px]">
                    {travelTips.electrical_specs}
                  </p>
                </div>
              )}

              {/* Transit Infrastructure */}
              {travelTips.transit_tips && (
                <div className="p-3.5 rounded-xl bg-emerald-950/30 border border-emerald-500/30 print:bg-emerald-50 print:border-emerald-200">
                  <div className="flex items-center gap-2 font-semibold text-emerald-300 print:text-emerald-900 mb-1">
                    <Train className="w-4 h-4 text-emerald-400 print:text-emerald-600" /> Contactless Transit & Mobility Card
                  </div>
                  <p className="text-emerald-200/90 print:text-emerald-900 leading-relaxed">
                    {travelTips.transit_tips}
                  </p>
                </div>
              )}

              {/* Diplomatic Mission Assistance */}
              {travelTips.embassy_info && (
                <div className="p-3.5 rounded-xl bg-sky-950/40 border border-sky-500/30 print:bg-sky-50 print:border-sky-300">
                  <div className="flex items-center gap-2 font-bold text-sky-300 print:text-sky-800 mb-1">
                    <Landmark className="w-4 h-4 text-sky-400 print:text-sky-600" /> Consular & Diplomatic Mission Assistance
                  </div>
                  <p className="text-slate-300 print:text-slate-800 leading-relaxed text-[11px] whitespace-pre-line font-mono">
                    {travelTips.embassy_info}
                  </p>
                </div>
              )}

              {/* Payment & Currency */}
              {travelTips.currency_and_payment_tips && (
                <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-700/60 print:bg-slate-50 print:border-slate-200">
                  <div className="flex items-center gap-2 font-semibold text-slate-200 print:text-slate-900 mb-1">
                    <CreditCard className="w-4 h-4 text-emerald-400 print:text-emerald-600" /> Currency & Payment Practices
                  </div>
                  <p className="text-slate-400 print:text-slate-700 leading-relaxed">{travelTips.currency_and_payment_tips}</p>
                </div>
              )}

              {/* Local Customs & Etiquette */}
              {travelTips.local_customs && travelTips.local_customs.length > 0 && (
                <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-700/60 print:bg-slate-50 print:border-slate-200">
                  <span className="font-semibold text-slate-200 print:text-slate-900 block mb-1">Local Etiquette & Customs</span>
                  <ul className="list-disc list-inside space-y-1 text-slate-400 print:text-slate-700 leading-relaxed">
                    {travelTips.local_customs.map((c, idx) => (
                      <li key={idx}>{c}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
