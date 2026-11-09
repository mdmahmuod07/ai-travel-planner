import React from 'react';
import { Bot, CheckCircle2, Loader2, Sparkles, MapPin, Calendar, DollarSign, Utensils, ShieldCheck } from 'lucide-react';

export default function AgentProgress({ logs }) {
  const agents = [
    {
      id: 'destination_specialist',
      name: 'Destination & Attraction Specialist',
      role: 'Researching highlights, landmark clusters & local customs',
      icon: MapPin,
      color: 'from-amber-500 to-orange-500'
    },
    {
      id: 'itinerary_orchestrator',
      name: 'Itinerary Orchestrator',
      role: 'Designing geographically optimized day-by-day timetable',
      icon: Calendar,
      color: 'from-sky-500 to-blue-600'
    },
    {
      id: 'budget_specialist',
      name: 'Budget & Accommodation Specialist',
      role: 'Calculating price breakdowns & vetting hotel options',
      icon: DollarSign,
      color: 'from-emerald-500 to-teal-600'
    },
    {
      id: 'dining_specialist',
      name: 'Dining & Culinary Specialist',
      role: 'Curating authentic dining & applying dietary filters',
      icon: Utensils,
      color: 'from-pink-500 to-rose-600'
    },
    {
      id: 'packing_specialist',
      name: 'Packing & Travel Safety Specialist',
      role: 'Formulating weather-aware packing & security checklist',
      icon: ShieldCheck,
      color: 'from-purple-500 to-indigo-600'
    }
  ];

  const getAgentStatus = (id) => {
    const agentLogs = logs.filter(l => l.agent_id === id);
    if (!agentLogs || agentLogs.length === 0) return { status: 'pending', lastMsg: 'Waiting to start...' };
    const lastLog = agentLogs[agentLogs.length - 1];
    return { status: lastLog.status, lastMsg: lastLog.message };
  };

  return (
    <div className="bg-slate-800/80 border border-slate-700 rounded-2xl p-6 shadow-xl my-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-xl bg-sky-500/10 border border-sky-500/20 text-sky-400">
          <Bot className="w-6 h-6 animate-pulse" />
        </div>
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            Multi-Agent Collaboration Network
            <span className="flex h-2.5 w-2.5 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-sky-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-sky-500"></span>
            </span>
          </h3>
          <p className="text-xs text-slate-400">5 specialized AI agents are processing your trip parameters concurrently...</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        {agents.map(agent => {
          const { status, lastMsg } = getAgentStatus(agent.id);
          const Icon = agent.icon;
          const isDone = status === 'completed';
          const isWorking = status === 'working';

          return (
            <div
              key={agent.id}
              className={`p-4 rounded-xl border transition-all duration-300 ${
                isDone
                  ? 'bg-slate-900/90 border-emerald-500/40 shadow-sm shadow-emerald-500/10'
                  : isWorking
                  ? 'bg-slate-900 border-sky-500/50 shadow-md shadow-sky-500/10 scale-[1.02]'
                  : 'bg-slate-900/40 border-slate-800 opacity-60'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <div className={`p-1.5 rounded-lg bg-gradient-to-tr ${agent.color} text-white`}>
                    <Icon className="w-4 h-4" />
                  </div>
                  <span className="text-xs font-semibold text-slate-200">{agent.name}</span>
                </div>
                {isDone ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                ) : isWorking ? (
                  <Loader2 className="w-4 h-4 text-sky-400 animate-spin shrink-0" />
                ) : (
                  <span className="w-2 h-2 rounded-full bg-slate-600 shrink-0" />
                )}
              </div>
              <p className="text-xs text-slate-400 line-clamp-2 mt-1">{lastMsg}</p>
            </div>
          );
        })}
      </div>

      {/* Live Stream Terminal Output */}
      <div className="bg-slate-950 rounded-xl p-3 border border-slate-800 font-mono text-xs max-h-36 overflow-y-auto">
        <div className="text-slate-500 border-b border-slate-800 pb-1 mb-2 flex items-center justify-between">
          <span>Agent Activity Console</span>
          <span className="text-[10px] text-sky-400 flex items-center gap-1">
            <Sparkles className="w-3 h-3" /> Live Feed
          </span>
        </div>
        {logs.slice(-6).map((log, i) => (
          <div key={i} className="py-0.5 text-slate-300 flex items-start gap-2">
            <span className="text-slate-500 shrink-0">[{log.timestamp}]</span>
            <span className="text-sky-400 font-semibold shrink-0">[{log.agent_name}]:</span>
            <span className="text-slate-200">{log.message}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
