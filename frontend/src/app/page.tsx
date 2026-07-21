'use client';

import React, { useState, useEffect } from 'react';
import { 
  Cpu, Shield, Database, Network, MessageSquare, Terminal, 
  Upload, Search, CheckCircle2, AlertTriangle, Activity, Zap, 
  Layers, Lock, Server, Sparkles, FileText, Send, RefreshCw 
} from 'lucide-react';

export default function KalkiDashboard() {
  const [activeTab, setActiveTab] = useState<'agent' | 'topology' | 'rag' | 'security'>('agent');
  const [inputQuery, setInputQuery] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionResult, setExecutionResult] = useState<any>(null);
  
  // RAG Search State
  const [ragQuery, setRagQuery] = useState('KALKI AI latency specs');
  const [ragResults, setRagResults] = useState<any[]>([]);

  // Default Agent Execution Simulation
  const handleExecuteTask = async () => {
    if (!inputQuery.trim()) return;
    setIsExecuting(true);
    setExecutionResult(null);

    // Simulate backend call to http://localhost:8000/api/v1/chat/completions
    setTimeout(() => {
      setExecutionResult({
        trace_id: "tr-" + Math.random().toString(36).substring(2, 10),
        status: "SUCCESS",
        latency_ms: 412,
        response: `### KALKI AI IOS Execution Result\n\nQuery processed: **"${inputQuery}"**\n\n- **Security Agent**: Audit passed with zero risk violations (Risk score: 0.02).\n- **Planner Agent**: Decomposed into 3 sub-tasks via ReAct DAG planner.\n- **Research Agent**: Queried vector store (Cosine similarity 0.94).\n- **Memory Agent**: Injected short-term conversational context & long-term user preferences.\n- **Executor Agent**: Executed MCP tool \`kalki_vector_search\` and synthesized answer.\n- **Validator Agent**: Hallucination score 0.01 (Factually Grounded).`,
        execution_trace: [
          { agent: "SecurityAgent", status: "PASSED", risk_score: 0.02, latency: "12ms" },
          { agent: "PlannerAgent", status: "DECOMPOSED", subtasks: 3, latency: "38ms" },
          { agent: "ResearchAgent", status: "RETRIEVED", chunks: 2, latency: "145ms" },
          { agent: "MemoryAgent", status: "CONTEXT_INJECTED", mode: "Hierarchical", latency: "25ms" },
          { agent: "ExecutorAgent", status: "SYNTHESIZED", bytes: 480, latency: "162ms" },
          { agent: "ValidatorAgent", status: "VERIFIED", grounding: "99.2%", latency: "30ms" }
        ],
        citations: [
          { doc_id: "doc-kalki-arch-2026", title: "KALKI System Architecture Blueprint", score: 0.94 }
        ]
      });
      setIsExecuting(false);
    }, 1200);
  };

  const handleRagSearch = () => {
    setRagResults([
      {
        id: "doc-001",
        title: "KALKI AI Architectural Manifesto",
        content: "KALKI AI stands for Krishna Artificial Lattice Keystone Intelligence, designed as an Intelligence Operating System operating under 500ms latency budget.",
        score: 0.942,
        dense: 0.95,
        bm25: 0.93
      },
      {
        id: "doc-002",
        title: "Multi-Agent MCP & A2A Protocol Standard",
        content: "Model Context Protocol binds tools dynamically while A2A IPC router coordinates asynchronous inter-agent messages between Planner and Executor.",
        score: 0.884,
        dense: 0.89,
        bm25: 0.87
      }
    ]);
  };

  useEffect(() => {
    handleRagSearch();
  }, []);

  return (
    <div className="min-h-screen bg-[#07090E] text-gray-100 flex flex-col font-sans">
      
      {/* 1. TOP HEADER & METRICS BAR */}
      <header className="border-b border-white/10 bg-[#0B0F19]/80 backdrop-blur-md px-6 py-4 sticky top-0 z-50 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 via-indigo-500 to-purple-600 p-[2px] flex items-center justify-center shadow-lg shadow-cyan-500/20">
            <div className="w-full h-full bg-[#07090E] rounded-[10px] flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-cyan-400 animate-pulse" />
            </div>
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-xl font-bold tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-indigo-300 to-purple-400">
                KALKI AI
              </h1>
              <span className="px-2 py-0.5 text-[10px] font-mono font-semibold bg-cyan-950 text-cyan-400 border border-cyan-800/60 rounded-full">
                IOS v1.5.0
              </span>
            </div>
            <p className="text-xs text-gray-400">Krishna Artificial Lattice Keystone Intelligence</p>
          </div>
        </div>

        {/* Live System Metrics Badges */}
        <div className="hidden md:flex items-center space-x-6 text-xs font-mono">
          <div className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-white/5 border border-white/10">
            <Zap className="w-4 h-4 text-cyan-400" />
            <span className="text-gray-400">Latency SLA:</span>
            <span className="text-cyan-400 font-bold">&lt; 500ms</span>
          </div>

          <div className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-white/5 border border-white/10">
            <Cpu className="w-4 h-4 text-indigo-400" />
            <span className="text-gray-400">MoE Router:</span>
            <span className="text-indigo-300 font-semibold">Llama-3 70B / Phi-3 INT4</span>
          </div>

          <div className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-white/5 border border-white/10">
            <Shield className="w-4 h-4 text-emerald-400" />
            <span className="text-gray-400">Security Guard:</span>
            <span className="text-emerald-400 font-semibold">ACTIVE</span>
          </div>
        </div>
      </header>

      {/* 2. NAVIGATION TABS */}
      <div className="border-b border-white/10 bg-[#0B0F19]/50 px-6 py-2 flex space-x-2">
        <button
          onClick={() => setActiveTab('agent')}
          className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            activeTab === 'agent'
              ? 'bg-gradient-to-r from-cyan-500/20 to-purple-500/20 text-cyan-300 border border-cyan-500/40'
              : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'
          }`}
        >
          <MessageSquare className="w-4 h-4" />
          <span>Multimodal Agent Studio</span>
        </button>

        <button
          onClick={() => setActiveTab('topology')}
          className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            activeTab === 'topology'
              ? 'bg-gradient-to-r from-cyan-500/20 to-purple-500/20 text-cyan-300 border border-cyan-500/40'
              : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'
          }`}
        >
          <Network className="w-4 h-4" />
          <span>Agent Topology &amp; MCP</span>
        </button>

        <button
          onClick={() => setActiveTab('rag')}
          className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            activeTab === 'rag'
              ? 'bg-gradient-to-r from-cyan-500/20 to-purple-500/20 text-cyan-300 border border-cyan-500/40'
              : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'
          }`}
        >
          <Database className="w-4 h-4" />
          <span>Hybrid RAG Knowledge</span>
        </button>

        <button
          onClick={() => setActiveTab('security')}
          className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            activeTab === 'security'
              ? 'bg-gradient-to-r from-cyan-500/20 to-purple-500/20 text-cyan-300 border border-cyan-500/40'
              : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'
          }`}
        >
          <Shield className="w-4 h-4" />
          <span>Defensive Security Studio</span>
        </button>
      </div>

      {/* 3. MAIN DASHBOARD CONTENT */}
      <main className="flex-1 p-6 max-w-7xl w-full mx-auto space-y-6">
        
        {/* TAB 1: MULTIMODAL AGENT STUDIO */}
        {activeTab === 'agent' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* Left Column: Input Prompt & Dropzone */}
            <div className="lg:col-span-2 space-y-6">
              <div className="glass-panel rounded-2xl p-6 space-y-4">
                <div className="flex items-center justify-between">
                  <h2 className="text-lg font-semibold flex items-center space-x-2">
                    <Terminal className="w-5 h-5 text-cyan-400" />
                    <span>Agent Command Studio</span>
                  </h2>
                  <span className="text-xs font-mono text-gray-400">MCP Protocol v1.0</span>
                </div>

                <div className="relative">
                  <textarea
                    value={inputQuery}
                    onChange={(e) => setInputQuery(e.target.value)}
                    placeholder="Enter complex multimodal prompt (e.g. 'Analyze KALKI AI multi-agent orchestrator and verify security guardrails')..."
                    className="w-full h-36 bg-[#07090E]/80 border border-white/10 rounded-xl p-4 text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-cyan-500/60 focus:ring-1 focus:ring-cyan-500/60 resize-none"
                  />
                  <div className="absolute bottom-3 right-3 flex items-center space-x-2">
                    <button 
                      onClick={() => setInputQuery("Execute defensive security audit and RAG knowledge search on KALKI architecture.")}
                      className="text-xs px-2.5 py-1 rounded-md bg-white/5 hover:bg-white/10 text-gray-400 transition"
                    >
                      Preset Query
                    </button>
                    <button
                      onClick={handleExecuteTask}
                      disabled={isExecuting || !inputQuery.trim()}
                      className="px-5 py-2 rounded-lg bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-400 hover:to-purple-500 text-white font-medium text-sm flex items-center space-x-2 shadow-lg shadow-cyan-500/20 disabled:opacity-50 transition"
                    >
                      {isExecuting ? (
                        <>
                          <RefreshCw className="w-4 h-4 animate-spin" />
                          <span>Executing Agents...</span>
                        </>
                      ) : (
                        <>
                          <Send className="w-4 h-4" />
                          <span>Dispatch Task</span>
                        </>
                      )}
                    </button>
                  </div>
                </div>

                {/* Multimodal Attachment Zone */}
                <div className="border border-dashed border-white/10 rounded-xl p-4 text-center hover:border-cyan-500/40 transition cursor-pointer flex items-center justify-center space-x-3 bg-white/[0.01]">
                  <Upload className="w-5 h-5 text-gray-400" />
                  <span className="text-xs text-gray-400">
                    Drop PDF, Code files, Images, Audio streams, or IoT Sensor JSON payloads for Multimodal Ingestion
                  </span>
                </div>
              </div>

              {/* Execution Result Box */}
              {executionResult && (
                <div className="glass-panel rounded-2xl p-6 space-y-4 border-cyan-500/30">
                  <div className="flex items-center justify-between border-b border-white/10 pb-3">
                    <div className="flex items-center space-x-3">
                      <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                      <h3 className="font-semibold text-gray-200">Execution Completed</h3>
                    </div>
                    <div className="text-xs font-mono px-3 py-1 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800">
                      Latency: {executionResult.latency_ms}ms
                    </div>
                  </div>

                  <div className="text-sm text-gray-300 leading-relaxed whitespace-pre-line font-sans bg-[#07090E]/60 p-4 rounded-xl border border-white/5">
                    {executionResult.response}
                  </div>

                  {/* Grounded Citation */}
                  {executionResult.citations && (
                    <div className="pt-2">
                      <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Grounding Citations</h4>
                      {executionResult.citations.map((c: any, idx: number) => (
                        <div key={idx} className="flex items-center justify-between text-xs bg-white/5 p-2.5 rounded-lg border border-white/10">
                          <span className="text-cyan-300 font-medium">{c.title}</span>
                          <span className="font-mono text-gray-400">Confidence: {c.score}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Right Column: Live Agent Execution Trace */}
            <div className="space-y-6">
              <div className="glass-panel rounded-2xl p-6 space-y-4">
                <h3 className="text-sm font-semibold flex items-center space-x-2 text-gray-300">
                  <Activity className="w-4 h-4 text-cyan-400" />
                  <span>Agent Execution Trace Feed</span>
                </h3>

                <div className="space-y-3 font-mono text-xs">
                  {executionResult ? (
                    executionResult.execution_trace.map((item: any, idx: number) => (
                      <div key={idx} className="p-3 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between">
                        <div>
                          <div className="text-cyan-300 font-bold">{item.agent}</div>
                          <div className="text-gray-400 text-[11px]">Action: {item.status}</div>
                        </div>
                        <div className="text-right">
                          <span className="text-emerald-400 text-[10px]">{item.latency}</span>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-12 text-gray-500 text-xs">
                      No active task execution trace.<br />Submit a prompt to view real-time multi-agent IPC handoffs.
                    </div>
                  )}
                </div>
              </div>
            </div>

          </div>
        )}

        {/* TAB 2: AGENT TOPOLOGY & MCP PROTOCOL */}
        {activeTab === 'topology' && (
          <div className="space-y-6">
            <div className="glass-panel rounded-2xl p-6">
              <h2 className="text-lg font-semibold mb-4 flex items-center space-x-2">
                <Network className="w-5 h-5 text-cyan-400" />
                <span>6-Agent Orchestration Architecture (MCP &amp; A2A IPC)</span>
              </h2>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {[
                  { name: "Security Agent", role: "Perimeter & Prompt Guardrails", status: "ACTIVE", desc: "Audits prompt injections & enforces NIST/RBAC controls." },
                  { name: "Planner Agent", role: "ReAct DAG Task Decomposer", status: "ACTIVE", desc: "Breaks high-level goals into parallel sub-task execution graphs." },
                  { name: "Research Agent", role: "RAG & Vector Search Retriever", status: "ACTIVE", desc: "Queries Qdrant dense vector store & BM25 keyword index." },
                  { name: "Memory Agent", role: "Hierarchical Context Ingestion", status: "ACTIVE", desc: "Manages short-term, long-term, semantic & episodic memory." },
                  { name: "Executor Agent", role: "MCP Tool Runtime Execution", status: "ACTIVE", desc: "Runs sandboxed code execution, web search & external APIs." },
                  { name: "Validator Agent", role: "Fact & Hallucination Verifier", status: "ACTIVE", desc: "Validates output factual grounding before returning to user." }
                ].map((agent, i) => (
                  <div key={i} className="p-4 rounded-xl bg-white/5 border border-white/10 space-y-2 hover:border-cyan-500/40 transition">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-cyan-300 text-sm">{agent.name}</span>
                      <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800">
                        {agent.status}
                      </span>
                    </div>
                    <div className="text-xs font-semibold text-gray-400">{agent.role}</div>
                    <p className="text-xs text-gray-400 leading-relaxed">{agent.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* TAB 3: HYBRID RAG KNOWLEDGE ENGINE */}
        {activeTab === 'rag' && (
          <div className="space-y-6">
            <div className="glass-panel rounded-2xl p-6 space-y-4">
              <h2 className="text-lg font-semibold flex items-center space-x-2">
                <Database className="w-5 h-5 text-cyan-400" />
                <span>Reciprocal Rank Fusion (RRF) Hybrid Search Inspector</span>
              </h2>

              <div className="flex space-x-3">
                <input
                  type="text"
                  value={ragQuery}
                  onChange={(e) => setRagQuery(e.target.value)}
                  className="flex-1 bg-[#07090E] border border-white/10 rounded-xl px-4 py-2 text-sm text-gray-100 focus:outline-none focus:border-cyan-500"
                />
                <button
                  onClick={handleRagSearch}
                  className="px-5 py-2 rounded-xl bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 font-medium text-sm flex items-center space-x-2 border border-cyan-500/40"
                >
                  <Search className="w-4 h-4" />
                  <span>Execute Search</span>
                </button>
              </div>

              {/* RAG Results List */}
              <div className="space-y-3 pt-2">
                {ragResults.map((item, idx) => (
                  <div key={idx} className="p-4 rounded-xl bg-white/5 border border-white/10 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-gray-200 text-sm">{item.title}</span>
                      <div className="flex space-x-2 text-[10px] font-mono">
                        <span className="px-2 py-0.5 bg-cyan-950 text-cyan-400 rounded">RRF Score: {item.score}</span>
                        <span className="px-2 py-0.5 bg-indigo-950 text-indigo-300 rounded">Dense: {item.dense}</span>
                        <span className="px-2 py-0.5 bg-purple-950 text-purple-300 rounded">BM25: {item.bm25}</span>
                      </div>
                    </div>
                    <p className="text-xs text-gray-400">{item.content}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* TAB 4: DEFENSIVE SECURITY & GOVERNANCE */}
        {activeTab === 'security' && (
          <div className="space-y-6">
            <div className="glass-panel rounded-2xl p-6 space-y-4">
              <h2 className="text-lg font-semibold flex items-center space-x-2 text-emerald-400">
                <Shield className="w-5 h-5" />
                <span>Defensive Cybersecurity &amp; Safety Audit Panel</span>
              </h2>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs">
                <div className="p-4 rounded-xl bg-white/5 border border-white/10 space-y-1">
                  <div className="text-gray-400">Threat Monitoring Status</div>
                  <div className="text-emerald-400 text-lg font-bold">0 Active Threats</div>
                  <div className="text-[10px] text-gray-500">NIST SP 800-53 Compliant</div>
                </div>

                <div className="p-4 rounded-xl bg-white/5 border border-white/10 space-y-1">
                  <div className="text-gray-400">Encryption Level</div>
                  <div className="text-cyan-400 text-lg font-bold">TLS 1.3 / AES-256</div>
                  <div className="text-[10px] text-gray-500">End-to-End Encrypted</div>
                </div>

                <div className="p-4 rounded-xl bg-white/5 border border-white/10 space-y-1">
                  <div className="text-gray-400">Human-in-the-Loop (HITL)</div>
                  <div className="text-indigo-400 text-lg font-bold">ENABLED</div>
                  <div className="text-[10px] text-gray-500">High-Impact Actions Require Approval</div>
                </div>
              </div>
            </div>
          </div>
        )}

      </main>

      {/* FOOTER */}
      <footer className="border-t border-white/10 py-4 px-6 text-center text-xs text-gray-500 font-mono">
        KALKI AI — Krishna Artificial Lattice Keystone Intelligence © 2026. All rights reserved.
      </footer>
    </div>
  );
}
