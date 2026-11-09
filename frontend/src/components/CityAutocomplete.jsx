import React, { useState, useEffect, useRef } from 'react';
import { MapPin, Loader2, X, Check } from 'lucide-react';

// Built-in offline fallback database of top global destinations
const POPULAR_DESTINATIONS = [
  { city: 'Tokyo', country: 'Japan', display: 'Tokyo, Japan' },
  { city: 'Istanbul', country: 'Turkey', display: 'Istanbul, Turkey' },
  { city: 'Paris', country: 'France', display: 'Paris, France' },
  { city: 'London', country: 'United Kingdom', display: 'London, United Kingdom' },
  { city: 'New York', country: 'United States', display: 'New York, United States' },
  { city: 'Bangalore', country: 'India', display: 'Bangalore, India' },
  { city: 'Delhi', country: 'India', display: 'Delhi, India' },
  { city: 'Mumbai', country: 'India', display: 'Mumbai, India' },
  { city: 'Rome', country: 'Italy', display: 'Rome, Italy' },
  { city: 'Dubai', country: 'United Arab Emirates', display: 'Dubai, United Arab Emirates' },
  { city: 'Bangkok', country: 'Thailand', display: 'Bangkok, Thailand' },
  { city: 'Singapore', country: 'Singapore', display: 'Singapore, Singapore' },
  { city: 'Amsterdam', country: 'Netherlands', display: 'Amsterdam, Netherlands' },
  { city: 'Barcelona', country: 'Spain', display: 'Barcelona, Spain' },
  { city: 'Kyoto', country: 'Japan', display: 'Kyoto, Japan' },
  { city: 'Bali', country: 'Indonesia', display: 'Bali, Indonesia' },
  { city: 'Berlin', country: 'Germany', display: 'Berlin, Germany' },
  { city: 'Sydney', country: 'Australia', display: 'Sydney, Australia' },
  { city: 'Toronto', country: 'Canada', display: 'Toronto, Canada' },
  { city: 'Seoul', country: 'South Korea', display: 'Seoul, South Korea' },
  { city: 'Cairo', country: 'Egypt', display: 'Cairo, Egypt' },
  { city: 'Vienna', country: 'Austria', display: 'Vienna, Austria' },
  { city: 'Prague', country: 'Czech Republic', display: 'Prague, Czech Republic' },
  { city: 'Athens', country: 'Greece', display: 'Athens, Greece' },
  { city: 'Lisbon', country: 'Portugal', display: 'Lisbon, Portugal' },
  { city: 'Ankara', country: 'Turkey', display: 'Ankara, Turkey' },
  { city: 'Antalya', country: 'Turkey', display: 'Antalya, Turkey' },
  { city: 'Osaka', country: 'Japan', display: 'Osaka, Japan' }
];

export default function CityAutocomplete({
  value,
  onChange,
  placeholder = 'e.g. Istanbul, Turkey',
  required = false,
  icon: Icon = MapPin,
  iconColor = 'text-sky-400'
}) {
  const [inputValue, setInputValue] = useState(value || '');
  const [suggestions, setSuggestions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(-1);
  const containerRef = useRef(null);

  useEffect(() => {
    setInputValue(value || '');
  }, [value]);

  // Click outside listener to dismiss popup
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // 300ms Debounced Nominatim Fetch with Offline Fallback
  useEffect(() => {
    const trimmed = inputValue.trim();
    if (trimmed.length < 2) {
      setSuggestions([]);
      setIsOpen(false);
      return;
    }

    const timer = setTimeout(async () => {
      setIsLoading(true);
      try {
        // First query OpenStreetMap Nominatim
        const endpoint = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(
          trimmed
        )}&addressdetails=1&limit=6&featuretype=city`;
        
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 2500); // 2.5s network timeout

        const response = await fetch(endpoint, {
          signal: controller.signal,
          headers: {
            'Accept-Language': 'en',
            'User-Agent': 'AITravelPlanner/2.0'
          }
        });
        clearTimeout(timeoutId);

        if (response.ok) {
          const data = await response.json();
          if (Array.isArray(data) && data.length > 0) {
            const parsed = data.map((item) => {
              const addr = item.address || {};
              const cityName = addr.city || addr.town || addr.municipality || addr.state || item.name;
              const countryName = addr.country || '';
              const fullLabel = countryName ? `${cityName}, ${countryName}` : item.display_name.split(',').slice(0, 2).join(',').trim();
              return {
                id: item.place_id || item.osm_id || fullLabel,
                primary: fullLabel,
                secondary: item.display_name,
                lat: parseFloat(item.lat),
                lng: parseFloat(item.lon)
              };
            });
            setSuggestions(parsed);
            setIsOpen(true);
            setIsLoading(false);
            return;
          }
        }
      } catch (err) {
        // Network or CORS or rate-limit or abort: fall through to offline database
      }

      // Offline instant fallback search
      const qLower = trimmed.toLowerCase();
      const matched = POPULAR_DESTINATIONS.filter(
        (p) =>
          p.city.toLowerCase().includes(qLower) ||
          p.country.toLowerCase().includes(qLower) ||
          p.display.toLowerCase().includes(qLower)
      ).slice(0, 5).map((p) => ({
        id: p.display,
        primary: p.display,
        secondary: `${p.city}, ${p.country}`
      }));

      setSuggestions(matched);
      setIsOpen(matched.length > 0);
      setIsLoading(false);
    }, 300);

    return () => clearTimeout(timer);
  }, [inputValue]);

  const handleSelect = (item) => {
    const selectedText = item.primary;
    setInputValue(selectedText);
    onChange(selectedText);
    setIsOpen(false);
    setSuggestions([]);
  };

  const handleInputChange = (e) => {
    const val = e.target.value;
    setInputValue(val);
    onChange(val);
    setIsOpen(true);
  };

  const handleKeyDown = (e) => {
    if (!isOpen || suggestions.length === 0) return;

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setHighlightedIndex((prev) => (prev < suggestions.length - 1 ? prev + 1 : 0));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setHighlightedIndex((prev) => (prev > 0 ? prev - 1 : suggestions.length - 1));
    } else if (e.key === 'Enter') {
      if (highlightedIndex >= 0 && highlightedIndex < suggestions.length) {
        e.preventDefault();
        handleSelect(suggestions[highlightedIndex]);
      }
    } else if (e.key === 'Escape') {
      setIsOpen(false);
    }
  };

  const handleClear = () => {
    setInputValue('');
    onChange('');
    setSuggestions([]);
    setIsOpen(false);
  };

  return (
    <div ref={containerRef} className="relative w-full">
      <div className="relative">
        <Icon className={`w-5 h-5 ${iconColor} absolute left-3 top-3 pointer-events-none`} />
        
        <input
          type="text"
          required={required}
          value={inputValue}
          onChange={handleInputChange}
          onFocus={() => {
            if (suggestions.length > 0) setIsOpen(true);
          }}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          autoComplete="off"
          className="w-full bg-slate-900 border border-slate-700 rounded-xl py-2.5 pl-10 pr-9 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-sky-500 transition text-sm shadow-inner"
        />

        <div className="absolute right-2.5 top-2.5 flex items-center space-x-1">
          {isLoading && <Loader2 className="w-4 h-4 text-sky-400 animate-spin" />}
          {inputValue && !isLoading && (
            <button
              type="button"
              onClick={handleClear}
              className="text-slate-500 hover:text-slate-300 p-0.5 rounded transition"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>

      {/* Dropdown Suggestions */}
      {isOpen && suggestions.length > 0 && (
        <ul className="absolute z-50 left-0 right-0 mt-1.5 bg-slate-900 border border-slate-700 rounded-xl shadow-2xl max-h-60 overflow-y-auto divide-y divide-slate-800 text-sm">
          {suggestions.map((item, idx) => {
            const isHighlighted = idx === highlightedIndex;
            const isSelected = item.primary.toLowerCase() === inputValue.toLowerCase();
            return (
              <li
                key={item.id || idx}
                onMouseDown={(e) => {
                  e.preventDefault(); // prevents blur before click
                  handleSelect(item);
                }}
                onMouseEnter={() => setHighlightedIndex(idx)}
                className={`px-3.5 py-2.5 cursor-pointer flex items-center justify-between transition ${
                  isHighlighted ? 'bg-sky-950/70 text-sky-200' : 'text-slate-200 hover:bg-slate-800/80'
                }`}
              >
                <div className="flex items-center space-x-2.5 overflow-hidden">
                  <MapPin className={`w-4 h-4 shrink-0 ${isHighlighted ? 'text-sky-400' : 'text-slate-500'}`} />
                  <div className="truncate">
                    <span className="font-semibold text-slate-100">{item.primary}</span>
                    {item.secondary && item.secondary !== item.primary && (
                      <span className="block text-[11px] text-slate-400 truncate mt-0.5">{item.secondary}</span>
                    )}
                  </div>
                </div>
                {isSelected && <Check className="w-4 h-4 text-emerald-400 shrink-0 ml-2" />}
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
