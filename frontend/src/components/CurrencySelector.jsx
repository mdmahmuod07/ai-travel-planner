import React from 'react';
import { Coins } from 'lucide-react';

export const CURRENCY_RATES = {
  INR: { symbol: '₹', rate: 1.0, baseToUsd: 1 / 84.0, label: 'INR (₹)' },
  USD: { symbol: '$', rate: 1 / 84.0, baseToUsd: 1.0, label: 'USD ($)' },
  EUR: { symbol: '€', rate: 0.92 / 84.0, baseToUsd: 0.92, label: 'EUR (€)' },
  GBP: { symbol: '£', rate: 0.78 / 84.0, baseToUsd: 0.78, label: 'GBP (£)' },
  JPY: { symbol: '¥', rate: 155.0 / 84.0, baseToUsd: 155.0, label: 'JPY (¥)' },
  AUD: { symbol: 'A$', rate: 1.52 / 84.0, baseToUsd: 1.52, label: 'AUD (A$)' },
  CAD: { symbol: 'C$', rate: 1.38 / 84.0, baseToUsd: 1.38, label: 'CAD (C$)' }
};

export function formatCurrencyValue(amount, currencyCode = 'INR') {
  if (amount === undefined || amount === null) return '';
  const num = typeof amount === 'number' ? amount : parseFloat(String(amount).replace(/[^0-9.-]+/g, ''));
  if (isNaN(num)) return String(amount);

  if (currencyCode === 'INR') {
    return '₹' + new Intl.NumberFormat('en-IN', { maximumFractionDigits: 0 }).format(Math.round(num));
  }
  const curr = CURRENCY_RATES[currencyCode] || CURRENCY_RATES.USD;
  return `${curr.symbol}${new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 }).format(Math.round(num))}`;
}

export function convertAmount(text, targetCurrency = 'INR') {
  if (!text || typeof text !== 'string') return text;
  const target = targetCurrency.toUpperCase();
  const targetConfig = CURRENCY_RATES[target] || CURRENCY_RATES.INR;

  // 1. If text has INR (₹) amounts: e.g. "₹50,000" or "₹2,500 - ₹4,500"
  if (text.includes('₹')) {
    if (target === 'INR') {
      // Re-format cleanly with Intl.NumberFormat('en-IN')
      return text.replace(/₹\s*([\d,]+)/g, (match, p1) => {
        const val = parseInt(p1.replace(/,/g, ''), 10);
        if (isNaN(val)) return match;
        return formatCurrencyValue(val, 'INR');
      });
    }
    // Convert from INR to target currency
    return text.replace(/₹\s*([\d,]+)/g, (match, p1) => {
      const valInInr = parseInt(p1.replace(/,/g, ''), 10);
      if (isNaN(valInInr)) return match;
      const converted = valInInr * targetConfig.rate;
      return formatCurrencyValue(converted, target);
    });
  }

  // 2. If text has USD ($) amounts: e.g. "$100" or "$50 - $100"
  if (text.includes('$')) {
    if (target === 'USD') {
      return text;
    }
    const inrMultiplier = 84.0;
    return text.replace(/\$\s*([\d,]+)/g, (match, p1) => {
      const valInUsd = parseInt(p1.replace(/,/g, ''), 10);
      if (isNaN(valInUsd)) return match;
      const valInInr = valInUsd * inrMultiplier;
      if (target === 'INR') {
        return formatCurrencyValue(valInInr, 'INR');
      }
      const converted = valInInr * targetConfig.rate;
      return formatCurrencyValue(converted, target);
    });
  }

  // 3. If text is a plain number string: e.g. "50000"
  const cleanNum = parseFloat(text.replace(/,/g, ''));
  if (!isNaN(cleanNum)) {
    return formatCurrencyValue(cleanNum, target);
  }

  return text;
}

export default function CurrencySelector({ currentCurrency = 'INR', onCurrencyChange }) {
  return (
    <div className="flex items-center gap-2 bg-slate-900 border border-slate-700/80 px-3 py-1.5 rounded-xl print:hidden">
      <Coins className="w-4 h-4 text-emerald-400" />
      <span className="text-xs font-semibold text-slate-400">Currency:</span>
      <select
        value={currentCurrency}
        onChange={(e) => onCurrencyChange(e.target.value)}
        className="bg-transparent text-xs font-bold text-emerald-400 focus:outline-none cursor-pointer"
      >
        {Object.keys(CURRENCY_RATES).map(code => (
          <option key={code} value={code} className="bg-slate-900 text-slate-200">
            {CURRENCY_RATES[code].label}
          </option>
        ))}
      </select>
    </div>
  );
}
