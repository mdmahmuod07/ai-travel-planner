/**
 * Generates and triggers download of an RFC 5545 compliant .ics calendar file
 * for Google Calendar, Apple Calendar, and Microsoft Outlook.
 */
export function exportToCalendar(plan) {
  if (!plan || !plan.itinerary) return;

  const pad = (n) => (n < 10 ? `0${n}` : `${n}`);

  // Base start date: use tomorrow's date by default or today's date if not specified
  const baseDate = new Date();
  baseDate.setDate(baseDate.getDate() + 1);

  const formatICSDate = (dateObj, hours, minutes) => {
    const y = dateObj.getFullYear();
    const m = pad(dateObj.getMonth() + 1);
    const d = pad(dateObj.getDate());
    const hh = pad(hours);
    const mm = pad(minutes);
    return `${y}${m}${d}T${hh}${mm}00`;
  };

  const escapeICS = (str) => {
    if (!str) return '';
    return str
      .replace(/\\/g, '\\\\')
      .replace(/;/g, '\\;')
      .replace(/,/g, '\\,')
      .replace(/\n/g, '\\n');
  };

  const nowStamp = `${new Date().toISOString().replace(/[-:]/g, '').split('.')[0]}Z`;
  const lines = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//AI Travel Planner//Multi-Agent Autonomous System//EN',
    'CALSCALE:GREGORIAN',
    'METHOD:PUBLISH',
    `X-WR-CALNAME:Travel Itinerary: ${escapeICS(plan.destination)}`,
    'X-WR-TIMEZONE:Asia/Tokyo'
  ];

  plan.itinerary.forEach((day, dayIndex) => {
    const eventDate = new Date(baseDate);
    eventDate.setDate(baseDate.getDate() + dayIndex);

    (day.activities || []).forEach((act, actIdx) => {
      const slotLower = act.time_slot.toLowerCase();
      let startH = 9;
      let startM = 0;
      let endH = 12;
      let endM = 0;

      if (slotLower.includes('morning')) {
        startH = 9;
        startM = 0;
        endH = 12;
        endM = 0;
      } else if (slotLower.includes('afternoon')) {
        startH = 13;
        startM = 30;
        endH = 16;
        endM = 30;
      } else if (slotLower.includes('evening') || slotLower.includes('night')) {
        startH = 18;
        startM = 0;
        endH = 21;
        endM = 0;
      } else {
        startH = 10 + actIdx * 3;
        endH = startH + 2;
      }

      const dtStart = formatICSDate(eventDate, startH, startM);
      const dtEnd = formatICSDate(eventDate, endH, endM);
      const uid = `event-${plan.trip_id}-d${day.day_number}-a${actIdx}@aitravelplanner.ai`;

      let desc = act.description || '';
      if (act.tips) {
        desc += `\\n\\nInsider Tip: ${act.tips}`;
      }
      if (act.estimated_cost) {
        desc += `\\nEstimated Cost: ${act.estimated_cost}`;
      }
      desc += `\\nDay Theme: ${day.theme}`;

      lines.push('BEGIN:VEVENT');
      lines.push(`UID:${uid}`);
      lines.push(`DTSTAMP:${nowStamp}`);
      lines.push(`DTSTART:${dtStart}`);
      lines.push(`DTEND:${dtEnd}`);
      lines.push(`SUMMARY:[${escapeICS(act.time_slot)}] ${escapeICS(act.title)}`);
      lines.push(`DESCRIPTION:${escapeICS(desc)}`);
      lines.push(`LOCATION:${escapeICS(act.location ? `${act.location}, ${plan.destination}` : plan.destination)}`);
      if (act.lat && act.lng) {
        lines.push(`GEO:${act.lat};${act.lng}`);
      }
      lines.push('STATUS:CONFIRMED');
      lines.push('END:VEVENT');
    });
  });

  lines.push('END:VCALENDAR');

  const icsContent = lines.join('\r\n');
  const blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  const safeName = (plan.destination || 'trip').toLowerCase().replace(/[^a-z0-9]+/g, '_');
  a.download = `${safeName}_itinerary.ics`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
}
