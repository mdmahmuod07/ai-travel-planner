import React, { useEffect, useRef } from 'react';
import { Navigation, Clock, MapPin, ExternalLink } from 'lucide-react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

export default function MapView({ plan, activeDay = 1 }) {
  const mapContainerRef = useRef(null);
  const mapInstanceRef = useRef(null);

  if (!plan || !plan.itinerary || plan.itinerary.length === 0) return null;

  const currentDay = plan.itinerary.find(d => d.day_number === activeDay) || plan.itinerary[0];
  const activities = currentDay?.activities || [];

  const cleanVenue = (act) => {
    if (act.search_query) return act.search_query;
    const name = act.venue_name || act.title;
    return act.location ? `${name}, ${act.location}` : `${name}, ${plan.destination}`;
  };

  const getDirectionsUrl = () => {
    if (activities.length === 0) {
      return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(plan.destination)}`;
    }

    if (activities.length === 1) {
      return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(cleanVenue(activities[0]))}`;
    }

    const origin = encodeURIComponent(cleanVenue(activities[0]));
    const destination = encodeURIComponent(cleanVenue(activities[activities.length - 1]));
    const middleActivities = activities.slice(1, -1);
    const waypointsParam = middleActivities.length > 0
      ? `&waypoints=${middleActivities.map(a => encodeURIComponent(cleanVenue(a))).join('%7C')}`
      : '';

    return `https://www.google.com/maps/dir/?api=1&origin=${origin}&destination=${destination}${waypointsParam}&travelmode=transit`;
  };

  const directionsUrl = getDirectionsUrl();

  // Initialize and update interactive Leaflet Map
  useEffect(() => {
    if (!mapContainerRef.current) return;

    // Remove existing map instance if it exists
    if (mapInstanceRef.current) {
      mapInstanceRef.current.remove();
      mapInstanceRef.current = null;
    }

    const validActs = activities.filter(
      act => typeof act.lat === 'number' && typeof act.lng === 'number' && !isNaN(act.lat) && !isNaN(act.lng)
    );

    const defaultLat = validActs.length > 0 ? validActs[0].lat : 35.6762;
    const defaultLng = validActs.length > 0 ? validActs[0].lng : 139.6503;

    const map = L.map(mapContainerRef.current, {
      center: [defaultLat, defaultLng],
      zoom: 13,
      scrollWheelZoom: false
    });

    mapInstanceRef.current = map;

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    const markers = [];

    validActs.forEach((act, idx) => {
      const stopNumber = idx + 1;
      const customPin = L.divIcon({
        className: 'custom-map-marker',
        html: `
          <div style="
            background: linear-gradient(135deg, #0284c7, #0369a1);
            color: #ffffff;
            width: 32px;
            height: 32px;
            border-radius: 50% 50% 50% 0;
            transform: rotate(-45deg);
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid #ffffff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.35);
            cursor: pointer;
          ">
            <span style="
              transform: rotate(45deg);
              font-weight: 800;
              font-size: 12px;
              font-family: 'Plus Jakarta Sans', sans-serif;
            ">${stopNumber}</span>
          </div>
        `,
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
      });

      const venueQuery = encodeURIComponent(cleanVenue(act));
      const gmapsLink = `https://www.google.com/maps/search/?api=1&query=${venueQuery}`;

      const popupContent = `
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; min-width: 190px; padding: 4px;">
          <div style="display: inline-block; background: #e0f2fe; color: #0369a1; font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 4px; text-transform: uppercase; margin-bottom: 4px;">
            Stop #${stopNumber} • ${act.time_slot}
          </div>
          <div style="font-size: 13px; font-weight: 700; color: #0f172a; margin-bottom: 2px; line-height: 1.3;">
            ${act.venue_name || act.title}
          </div>
          <div style="font-size: 11px; color: #64748b; margin-bottom: 6px;">
            ${act.neighborhood || act.location || ''}
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #e2e8f0; padding-top: 6px; font-size: 11px;">
            <span style="color: #047857; font-weight: 700;">${act.estimated_cost || ''}</span>
            <a href="${gmapsLink}" target="_blank" rel="noopener noreferrer" style="color: #0284c7; font-weight: 700; text-decoration: underline; display: inline-flex; align-items: center; gap: 2px;">
              Open in Maps ↗
            </a>
          </div>
        </div>
      `;

      const marker = L.marker([act.lat, act.lng], { icon: customPin })
        .bindPopup(popupContent)
        .addTo(map);

      markers.push(marker);
    });

    // Draw transit polyline between sequential stops
    if (validActs.length > 1) {
      const coords = validActs.map(a => [a.lat, a.lng]);
      L.polyline(coords, {
        color: '#0284c7',
        weight: 4,
        opacity: 0.85,
        dashArray: '8, 8'
      }).addTo(map);

      const bounds = L.latLngBounds(coords);
      map.fitBounds(bounds, { padding: [40, 40], maxZoom: 15 });
    }

    // Force map size refresh after container settles
    const timer = setTimeout(() => {
      map.invalidateSize();
    }, 250);

    return () => {
      clearTimeout(timer);
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, [activeDay, currentDay, activities, plan.destination]);

  return (
    <div className="bg-slate-800/60 border border-slate-700 rounded-2xl p-5 sm:p-6 shadow-xl mb-8 print:bg-white print:border-slate-300 print:p-4 print:break-inside-avoid">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-4 gap-3">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-sky-500/15 border border-sky-500/30 print:bg-slate-100 print:border-slate-300">
            <Navigation className="w-5 h-5 text-sky-400 print:text-sky-600" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white print:text-slate-900">
              Transit & Route Flow • Day {activeDay}: {currentDay?.theme || 'Daily Itinerary'}
            </h3>
            <p className="text-xs text-slate-400 print:text-slate-600">
              Interactive Leaflet routing with sequential stops and Google Maps directions.
            </p>
          </div>
        </div>

        {/* Single Primary Google Maps Transit Button (Requirement 2) */}
        <div className="shrink-0 print:hidden">
          <a
            href={directionsUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-4 sm:px-5 py-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs shadow-lg shadow-sky-600/30 transition transform hover:-translate-y-0.5 active:translate-y-0"
            title="Open complete multi-stop transit route in Google Maps"
          >
            <span className="text-sm">🗺️</span>
            <span>Open Day Route in Google Maps</span>
            <ExternalLink className="w-3.5 h-3.5 ml-0.5 text-sky-200" />
          </a>
        </div>
      </div>

      {/* Embedded Leaflet Map Container */}
      <div className="relative mb-4">
        <div
          ref={mapContainerRef}
          className="w-full h-[320px] rounded-xl overflow-hidden border border-slate-700 shadow-inner z-0 print:border-slate-300 print:h-[260px]"
        />
      </div>

      {/* Sequential Stop Chips Flow */}
      {activities.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {activities.map((act, i) => {
            const venueSearch = cleanVenue(act);
            const mapsQueryUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(venueSearch)}`;

            return (
              <div
                key={i}
                className="bg-slate-900/80 border border-slate-700/70 rounded-xl p-3.5 print:bg-slate-50 print:border-slate-200 flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between gap-1 mb-1.5">
                    <span className="px-2 py-0.5 rounded-md bg-sky-500/20 text-sky-300 print:bg-sky-100 print:text-sky-800 text-[10px] font-bold uppercase tracking-wider">
                      Stop #{i + 1} • {act.time_slot}
                    </span>
                    <span className="text-[11px] text-slate-400 print:text-slate-500 flex items-center gap-1">
                      <Clock className="w-3 h-3" /> {act.duration}
                    </span>
                  </div>
                  <h4 className="text-xs font-bold text-slate-100 print:text-slate-900 line-clamp-1 mb-1">
                    <a
                      href={mapsQueryUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="hover:text-sky-400 hover:underline transition"
                      title={`Open ${act.venue_name || act.title} in Google Maps`}
                    >
                      {act.venue_name || act.title}
                    </a>
                  </h4>
                  <p className="text-[11px] text-slate-400 print:text-slate-600 flex items-center gap-1 truncate mb-2">
                    <MapPin className="w-3 h-3 text-sky-400 shrink-0" />
                    <span className="truncate">{act.neighborhood || act.location}</span>
                  </p>
                </div>

                <div className="pt-2 border-t border-slate-800 print:border-slate-200 flex items-center justify-between text-[11px]">
                  <span className="text-emerald-400 print:text-emerald-700 font-semibold">{act.estimated_cost}</span>
                  <a
                    href={mapsQueryUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sky-400 hover:text-sky-300 print:hidden font-medium inline-flex items-center gap-0.5 underline"
                  >
                    Locate ↗
                  </a>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <p className="text-xs text-slate-400">No scheduled activities for this day.</p>
      )}
    </div>
  );
}
