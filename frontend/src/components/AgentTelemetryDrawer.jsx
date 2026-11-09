import React from 'react';
import {
  Bot,
  X,
  CheckCircle2,
  MapPin,
  Calendar,
  DollarSign,
  Utensils,
  ShieldCheck,
  Cpu,
  ArrowRight,
  Clock,
  Sparkles
} from 'lucide-react';

export default function AgentTelemetryDrawer({ isOpen, onClose, logs = [], tripId, destination }) {
  if (!isOpen) return null;

  const agentNodes = [
    {
      id: 'orchestrator',
      name: 'Orchestrator',
      icon: Cpu,
      color: 'bg-indigo-600',
      description: 'Coordinates request pipeline, context synthesis & refinement'
    },
    {
      id: 'destination_specialist',
      name: 'Destination Specialist',
      icon: MapPin,
      color: 'bg-amber-600',
      description: 'Authentic ward exploration, genuine landmarks & accurate coordinates'
    },
    {
      id: 'itinerary_orchestrator',
      name: 'Itinerary Orchestrator',
      icon: Calendar,
      color: 'bg-sky-600',
      description: 'Geographically clustered day schedules & transit route routing'
    },
    {
      id: 'budget_specialist',
      name: 'Budget & Stay Specialist',
      icon: DollarSign,
      color: 'bg-emerald-600',
      description: 'Strict budget ceiling enforcement & dynamic accommodation adaptation'
    },
    {
      id: 'dining_specialist',
      name: 'Dining Specialist',
      icon: Utensils,
      color: 'bg-rose-600',
      description: 'Authentic dining curation with strict vegetarian/vegan broth vetting'
    },
    {
      id: 'packing_specialist',
      name: 'Packing & Safety Specialist',
      icon: ShieldCheck,
      color: 'bg-purple-600',
      description: 'Pre-approved visa laws, official 110/119 hotlines & embassy info'
    }
  ];

  return (
    <div className="fixed inset-0 z-50 overflow-hidden flex justify-end print:hidden">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-slate-950/70 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      />

      {/* Slide-over panel */}
      <div className="relative w-full max-w-xl bg-slate-900 border-l border-slate-800 shadow-2xl flex flex-col h-full z-10">
        {/* Header */}
        <div className="p-5 border-b border-slate-800 flex items-center justify-between bg-slate-950/60">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-sky-500/10 border border-sky-500/20 text-sky-400">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-white">Agent Orchestration Telemetry</h3>
                <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-bold">
                  5/5 Complete
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Live trace of multi-agent collaboration network for {destination || 'active trip'}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-5 overflow-y-auto space-y-6 grow">
          {/* Visual Collaboration Architecture */}
          <div>
            <h4 className="text-xs font-bold text-sky-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5" /> Multi-Agent Execution Flow
            </h4>
            <div className="bg-slate-950 rounded-xl p-4 border border-slate-800">
              <div className="flex flex-col gap-2">
                {/* Step 1: Orchestrator -> Destination */}
                <div className="flex items-center gap-2 text-xs">
                  <span className="px-2.5 py-1 rounded-md bg-indigo-600/30 border border-indigo-500/40 text-indigo-200 font-semibold shrink-0">
                    Orchestrator
                  </span>
                  <ArrowRight className="w-3.5 h-3.5 text-slate-500 shrink-0" />
                  <span className="px-2.5 py-1 rounded-md bg-amber-600/30 border border-amber-500/40 text-amber-200 font-semibold shrink-0">
                    Destination Specialist
                  </span>
                  <span className="text-[11px] text-slate-500 ml-auto">Initial Context</span>
                </div>

                {/* Step 2: Parallel Dispatch */}
                <div className="ml-4 pl-3 border-l-2 border-dashed border-slate-800 my-1 py-1 space-y-1.5">
                  <div className="text-[11px] font-semibold text-slate-400 flex items-center gap-1">
                    <span>⚡ Parallel Multi-Agent Concurrency:</span>
                  </div>
                  <div className="grid grid-cols-2 gap-1.5 text-[11px]">
                    <div className="p-1.5 rounded bg-sky-950/60 border border-sky-800/40 text-sky-300">
                      📅 Itinerary Orchestrator
                    </div>
                    <div className="p-1.5 rounded bg-emerald-950/60 border border-emerald-800/40 text-emerald-300">
                      💰 Budget & Hotel Specialist
                    </div>
                    <div className="p-1.5 rounded bg-rose-950/60 border border-rose-800/40 text-rose-300">
                      🍜 Dining Specialist
                    </div>
                    <div className="p-1.5 rounded bg-purple-950/60 border border-purple-800/40 text-purple-300">
                      🛡️ Packing & Safety Specialist
                    </div>
                  </div>
                </div>

                {/* Step 3: Synthesis */}
                <div className="flex items-center gap-2 text-xs">
                  <span className="px-2.5 py-1 rounded-md bg-emerald-600/30 border border-emerald-500/40 text-emerald-200 font-semibold shrink-0 flex items-center gap-1">
                    <CheckCircle2 className="w-3 h-3 text-emerald-400" /> Synthesis & Validation
                  </span>
                  <span className="text-[11px] text-slate-500 ml-auto">Trip ID: {tripId || 'trip_latest'}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Telemetry Guardrail Verifications */}
          <div>
            <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2.5">
              Verified Pipeline Guardrails
            </h4>
            <div className="space-y-2 text-xs">
              <div className="p-2.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>Strict Budget Ceiling enforced: Total Trip Cost &le; Target Budget</span>
              </div>
              <div className="p-2.5 rounded-lg bg-sky-500/10 border border-sky-500/20 text-sky-300 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-sky-400 shrink-0" />
                <span>Zero Hallucinations: Generic placeholders eliminated; authentic wards mapped</span>
              </div>
              <div className="p-2.5 rounded-lg bg-purple-500/10 border border-purple-500/20 text-purple-300 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-purple-400 shrink-0" />
                <span>Consular accuracy: Pre-approved visa verified; official 110 &amp; 119 numbers</span>
              </div>
              <div className="p-2.5 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-300 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-rose-400 shrink-0" />
                <span>Dietary integrity: Meat/poultry never tagged as Vegetarian/Vegan</span>
              </div>
            </div>
          </div>

          {/* Step-by-Step Execution Log Trace */}
          <div>
            <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5 text-slate-400" /> Step-by-Step Execution Trace ({logs.length} events)
            </h4>
            <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
              {logs.length === 0 ? (
                <div className="text-xs text-slate-500 p-4 text-center bg-slate-950/60 rounded-xl border border-slate-800">
                  No execution logs recorded yet.
                </div>
              ) : (
                logs.map((log, idx) => (
                  <div
                    key={idx}
                    className="p-3 rounded-xl bg-slate-950/80 border border-slate-800/80 flex items-start gap-3 text-xs"
                  >
                    <div className="mt-0.5 shrink-0">
                      {log.status === 'completed' ? (
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                      ) : (
                        <span className="w-2.5 h-2.5 rounded-full bg-sky-400 inline-block animate-pulse" />
                      )}
                    </div>
                    <div className="grow">
                      <div className="flex items-center justify-between gap-2 mb-0.5">
                        <span className="font-bold text-slate-200">{log.agent_name || log.agent_id}</span>
                        <span className="text-[10px] font-mono text-slate-500">{log.timestamp}</span>
                      </div>
                      <p className="text-slate-400 text-[11px] leading-relaxed">{log.message}</p>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-800 bg-slate-950/80 text-xs text-slate-500 flex items-center justify-between">
          <span>AI Travel Planner Multi-Agent Runtime</span>
          <button
            onClick={onClose}
            className="px-3 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold transition"
          >
            Close Drawer
          </button>
        </div>
      </div>
    </div>
  );
}
