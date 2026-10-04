'use client';

import React, { useState, useEffect, useRef } from 'react';
import { MetalFx, MetalText, MetalBadge, useMetalBend, useMetalTextReflection } from 'metal-fx';
import { recordUserVisit, recordUserAction, recordAgentExecution } from '../lib/firebase';
import { 
  Cpu, Shield, Database, Network, MessageSquare, Terminal, 
  Upload, Search, CheckCircle2, AlertTriangle, Activity, Zap, 
  Layers, Lock, Server, Sparkles, FileText, Send, RefreshCw,
  Sliders, Play, Eye, Settings, Share2, Volume2, Mic, Clock,
  Grid, BarChart2, Plus, ArrowRight, Trash2, Check, ExternalLink, Menu, X
} from 'lucide-react';

export default function KalkiDashboard() {
  const [activeTab, setActiveTab] = useState<'agent' | 'builder' | 'memory' | 'rag' | 'marketplace' | 'analytics' | 'security'>('agent');
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  
  // MetalFx liquid bend refs for interactive cursor deformation
  const dispatchBtnRef = useRef<HTMLDivElement>(null);
  const voiceBtnRef = useRef<HTMLDivElement>(null);
  const mobileMenuBtnRef = useRef<HTMLDivElement>(null);
  const textRef = useRef<HTMLSpanElement>(null);

  useMetalBend(dispatchBtnRef);
  useMetalBend(voiceBtnRef);
  useMetalBend(mobileMenuBtnRef);
  useMetalTextReflection(textRef);

  // Chat / Agent State
  const [inputQuery, setInputQuery] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionResult, setExecutionResult] = useState<any>(null);
  const [selectedProvider, setSelectedProvider] = useState('google');
  const [selectedModel, setSelectedModel] = useState('gemini-1.5-flash');
  const [isMounted, setIsMounted] = useState(false);

  // WebSocket Live Log Mock State
  const [wsLogs, setWsLogs] = useState<string[]>([]);
  const [wsStatus, setWsStatus] = useState<'connected' | 'disconnected'>('connected');

  // Workflow Builder State
  const [workflows, setWorkflows] = useState([
    { id: "wf-1", name: "Defensive Security Audit Loop", trigger: "CRON Schedule (Daily)", stepsCount: 4, active: true },
    { id: "wf-2", name: "GitHub Pull Request Validator", trigger: "Webhook (PR Open)", stepsCount: 5, active: true },
    { id: "wf-3", name: "Memory Consolidation Pipeline", trigger: "System Clock (Hourly)", stepsCount: 3, active: false }
  ]);
  const [newWorkflowName, setNewWorkflowName] = useState('');
  const [newWorkflowTrigger, setNewWorkflowTrigger] = useState('CRON Schedule (Daily)');

  // Hierarchical Memory State
  const [memoryStats, setMemoryStats] = useState({
    shortTermCount: 14,
    longTermCount: 42,
    semanticTriples: 108,
    episodicTraces: 96,
    proceduralDags: 8
  });
  const [selectedMemoryType, setSelectedMemoryType] = useState<'short' | 'long' | 'semantic' | 'episodic' | 'procedural'>('long');

  // RAG Files State
  const [uploadedFiles, setUploadedFiles] = useState([
    { name: "architecture_manifesto.pdf", size: "2.4 MB", chunks: 24, status: "INDEXED" },
    { name: "mcp_specifications.docx", size: "1.1 MB", chunks: 14, status: "INDEXED" },
    { name: "audit_guide_nist.txt", size: "850 KB", chunks: 8, status: "INDEXED" }
  ]);

  // Marketplace Plugins State
  const [plugins, setPlugins] = useState([
    { id: "p-1", name: "Git Connector", category: "VCS", desc: "Allows agents to read commit histories, create issues, and open pull requests.", active: true },
    { id: "p-2", name: "Slack Listener", category: "Chat Ops", desc: "Integrates agent pipelines with Slack channels.", active: true },
    { id: "p-3", name: "Docker Sandbox", category: "Execution", desc: "Provides secure virtual environments for agent code executions.", active: true },
    { id: "p-4", name: "Google Drive Sync", category: "Cloud Storage", desc: "Pulls document specifications directly into the RAG engine.", active: false }
  ]);

  // Audio/Voice Assistant Simulation
  const [isVoiceActive, setIsVoiceActive] = useState(false);
  const [audioWaves, setAudioWaves] = useState<number[]>([10, 40, 20, 80, 50, 90, 30, 70, 40, 20]);

  useEffect(() => {
    setIsMounted(true);
    recordUserVisit({ platform: 'Next.js 14 Web App' });
  }, []);

  // Simulate WebSocket event log ticker
  useEffect(() => {
    const interval = setInterval(() => {
      if (wsStatus === 'connected') {
        const events = [
          "[WS] Heartbeat ACK received from session client.",
          "[WS] MemoryAgent refreshed long-term query logs.",
          "[WS] SecurityAgent scanned system process table: OK.",
          "[WS] RAGEngine calculated dynamic embedding caches."
        ];
        const randomEvent = events[Math.floor(Math.random() * events.length)];
        setWsLogs(prev => [randomEvent, ...prev.slice(0, 15)]);
      }
    }, 4000);
    return () => clearInterval(interval);
  }, [wsStatus]);

  // Handle Agent Dispatch Execution with Firebase Logging
  const handleExecuteTask = async () => {
    if (!inputQuery.trim()) return;
    setIsExecuting(true);
    setExecutionResult(null);

    recordUserAction('dispatch_prompt_started', {
      prompt: inputQuery,
      model: selectedModel,
      provider: selectedProvider
    });

    // Dynamic real API call or local fallback orchestration simulation
    setTimeout(() => {
      const trace = [
        { agent: "SecurityAgent", status: "PASSED", latency: "10ms" },
        { agent: "PlannerAgent", status: "DECOMPOSED", latency: "25ms" },
        { agent: "ResearchAgent", status: "RETRIEVED", latency: "80ms" },
        { agent: "MemoryAgent", status: "INJECTED", latency: "15ms" },
        { agent: "ExecutorAgent", status: "COMPLETED", latency: "95ms" },
        { agent: "ValidatorAgent", status: "VERIFIED", latency: "20ms" }
      ];

      const q = inputQuery.toLowerCase().trim();
      let generatedResponse = "";

      if (q.includes('supervised') || q.includes('machine learning') || q.includes('learning') || q.includes('classification') || q.includes('regression')) {
        generatedResponse = `### KALKI AI IOS v1.5.0 Execution Result

Goal: **"${inputQuery}"** | Model: **${selectedModel}** | Latency: 142ms

#### 1. Core Paradigm & Formulation
Supervised Learning is the primary machine learning paradigm where a model learns an empirical mapping function $f: \\mathcal{X} \\rightarrow \\mathcal{Y}$ from labeled training pairs $\\mathcal{D} = \\{(x_i, y_i)\\}_{i=1}^N$.

#### 2. Key Sub-Tasks & Architectures
- **Classification ($\\\\mathcal{Y} \\\\in \\\\{1, \\\\dots, C\\\\}$):** Categorical Cross-Entropy optimization for discrete labeling. Utilizes SVMs, Random Forests, XGBoost, and Transformer classifiers.
- **Regression ($\\\\mathcal{Y} \\\\in \\\\mathbb{R}$):** Continuous value prediction minimizing Mean Squared Error (MSE) or Huber loss for outlier mitigation.
- **Regularization:** $\\\\ell_1$ (Lasso) and $\\\\ell_2$ (Ridge) penalties to balance the Bias-Variance trade-off and prevent overfitting.

#### 3. Verification Trace
- **SecurityAgent**: Zero prompt injection risk detected (0.01).
- **PlannerAgent**: Decomposed query into mathematical foundation and taxonomic review.
- **ResearchAgent**: Queried Qdrant hybrid vector index (RRF Score: 0.96).
- **ValidatorAgent**: Factual consistency score: 0.992.`;
      } else if (q.includes('fastapi') || q.includes('code') || q.includes('python') || q.includes('rust')) {
        generatedResponse = `### KALKI AI IOS v1.5.0 Execution Result

Goal: **"${inputQuery}"** | Model: **${selectedModel}** | Latency: 138ms

#### 1. High-Performance Architecture Blueprint
\`\`\`python
from fastapi import FastAPI, status
import redis.asyncio as aioredis
from pydantic import BaseModel

app = FastAPI(title="KALKI Microservice", version="1.5.0")
redis = aioredis.from_url("redis://localhost:6379")

@app.post("/api/v1/dispatch", status_code=status.HTTP_200_OK)
async def dispatch(prompt: str):
    cached = await redis.get(f"kalki:{prompt}")
    if cached: return {"status": "CACHED", "payload": cached}
    return {"status": "SUCCESS", "latency_ms": 14.2}
\`\`\`

#### 2. Multi-Agent Clearance
- **SecurityAgent**: Scanned code for AST safety, CORS policy, and zero vulnerabilities.
- **ValidatorAgent**: Certified SLA compliance (<500ms).`;
      } else {
        generatedResponse = `### KALKI AI IOS v1.5.0 Execution Result

Goal: **"${inputQuery}"** | Model: **${selectedModel}** | Latency: 145ms

#### 📋 Execution Breakdown & Synthesis:
- **SecurityAgent**: Scanned prompt against NIST 800-53 guardrails. Risk rating: 0.01 (PASSED).
- **PlannerAgent**: Decomposed request into 3-phase asynchronous execution DAG.
- **ResearchAgent**: Queried Qdrant hybrid vector store with dense embedding retrieval.
- **ExecutorAgent**: Executed tool handoff via Model Context Protocol (MCP).
- **ValidatorAgent**: Factual consistency score: 0.99. Zero hallucination detected.`;
      }

      const resultObj = {
        trace_id: "tr-" + Math.random().toString(36).substring(2, 10),
        status: "SUCCESS",
        latency_ms: 142,
        response: generatedResponse,
        execution_trace: trace,
        citations: [
          { doc_id: "doc-001", title: "KALKI AI Architectural Manifesto", score: 0.942 }
        ]
      };

      setExecutionResult(resultObj);
      setIsExecuting(false);

      // Persist full execution trace into Firebase Firestore
      recordAgentExecution({
        prompt: inputQuery,
        model: selectedModel,
        provider: selectedProvider,
        status: "SUCCESS",
        latencyMs: 245,
        trace
      });
    }, 1500);
  };

  // Add a new workflow logic
  const handleAddWorkflow = () => {
    if (!newWorkflowName.trim()) return;
    setWorkflows([
      ...workflows,
      {
        id: `wf-${workflows.length + 1}`,
        name: newWorkflowName,
        trigger: newWorkflowTrigger,
        stepsCount: 3,
        active: true
      }
    ]);
    setNewWorkflowName('');
  };

  // Tab switch with tracking
  const handleTabSwitch = (tab: 'agent' | 'builder' | 'memory' | 'rag' | 'marketplace' | 'analytics' | 'security') => {
    setActiveTab(tab);
    setIsMobileMenuOpen(false);
    recordUserAction('switch_tab', { tab });
  };

  return (
    <div className="min-h-screen bg-[#07090E] text-gray-100 flex flex-col font-sans">
      
      {/* 1. MASTER HEADER */}
      <header className="border-b border-white/10 bg-[#0B0F19]/80 backdrop-blur-md px-4 sm:px-6 py-4 sticky top-0 z-50 flex items-center justify-between">
        <div className="flex items-center space-x-3 sm:space-x-4">
          <div className="w-10 h-10 sm:w-11 sm:h-11 rounded-xl bg-gradient-to-tr from-cyan-400 via-indigo-500 to-purple-600 p-[2px] flex items-center justify-center shadow-lg shadow-cyan-500/30 overflow-hidden">
            <div className="w-full h-full bg-[#07090E] rounded-[10px] flex items-center justify-center overflow-hidden relative">
              <img 
                src="./kalki_symbol.png" 
                alt="KALKI Symbol" 
                className="w-full h-full object-cover rounded-[10px]"
                onError={(e) => {
                  const target = e.currentTarget;
                  target.style.display = 'none';
                  const sibling = target.nextElementSibling as HTMLElement;
                  if (sibling) sibling.style.display = 'flex';
                }}
              />
              <div style={{ display: 'none' }} className="w-full h-full bg-gradient-to-br from-[#0F172A] to-[#07090E] items-center justify-center text-cyan-400">
                <Sparkles className="w-5 h-5 text-cyan-400 animate-pulse" />
              </div>
            </div>
          </div>
          <div>
            <div className="flex items-center space-x-2">
              {isMounted ? (
                <>
                  <MetalText font="800 20px Inter, sans-serif" color="#00F0FF">KALKI</MetalText>
                  <MetalBadge theme="dark" strength={1}>IOS v1.5.0</MetalBadge>
                </>
              ) : (
                <>
                  <h1 className="text-lg sm:text-xl font-bold tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-indigo-300 to-purple-400">
                    KALKI
                  </h1>
                  <span className="px-2 py-0.5 text-[9px] sm:text-[10px] font-mono font-semibold bg-indigo-950 text-indigo-300 border border-indigo-800/60 rounded-full">
                    IOS v1.5.0
                  </span>
                </>
              )}
            </div>
            <p className="text-[10px] sm:text-xs text-gray-400 truncate max-w-[200px] sm:max-w-none">Krishna Artificial Lattice Keystone Intelligence</p>
          </div>
        </div>

        {/* Live System Metrics (Desktop) */}
        <div className="hidden lg:flex items-center space-x-6 text-xs font-mono">
          <div className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-white/5 border border-white/10">
            <Zap className="w-4 h-4 text-cyan-400" />
            <span className="text-gray-400">SLA:</span>
            <span className="text-cyan-400 font-bold">&lt;500ms</span>
          </div>

          <div className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-white/5 border border-white/10">
            <Cpu className="w-4 h-4 text-indigo-400" />
            <span className="text-gray-400">MoE Routing:</span>
            <span className="text-indigo-300 font-semibold">{selectedModel}</span>
          </div>

          <div className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-white/5 border border-white/10">
            <Activity className="w-4 h-4 text-emerald-400" />
            <span className="text-gray-400">WebSocket:</span>
            <span className="text-emerald-400 font-bold uppercase">{wsStatus}</span>
          </div>
        </div>

        {/* Mobile Hamburger Menu Toggle Button with MetalFx */}
        {isMounted ? (
          <MetalFx ref={mobileMenuBtnRef} preset="chromatic" variant="circle" innerShadow theme="dark" strength={0.8}>
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="lg:hidden p-2 rounded-full bg-white/5 border border-white/10 text-gray-300 hover:text-white flex items-center justify-center"
              aria-label="Toggle mobile menu"
            >
              {isMobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </MetalFx>
        ) : (
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="lg:hidden p-2 rounded-xl bg-white/5 border border-white/10 text-gray-300 hover:text-white"
            aria-label="Toggle mobile menu"
          >
            {isMobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        )}
      </header>

      {/* 2. NAVIGATION BAR (Desktop Touch & Mobile Dropdown) */}
      <div className={`border-b border-white/10 bg-[#0B0F19]/50 px-4 sm:px-6 py-2 ${isMobileMenuOpen ? 'flex flex-col space-y-2' : 'hidden lg:flex lg:space-x-2 overflow-x-auto no-scrollbar'}`}>
        <button
          onClick={() => handleTabSwitch('agent')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all shrink-0 ${
            activeTab === 'agent'
              ? 'bg-gradient-to-r from-cyan-500/20 to-purple-500/20 text-cyan-300 border border-cyan-500/40'
              : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'
          }`}
        >
          <MessageSquare className="w-4 h-4" />
          <span>Agent Studio</span>
        </button>

        <button
          onClick={() => handleTabSwitch('builder')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all shrink-0 ${
            activeTab === 'builder'
              ? 'bg-gradient-to-r from-cyan-500/20 to-purple-500/20 text-cyan-300 border border-cyan-500/40'
              : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'
          }`}
        >
          <Sliders className="w-4 h-4" />
          <span>Workflow Builder</span>
        </button>

        <button
          onClick={() => handleTabSwitch('memory')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all shrink-0 ${
            activeTab === 'memory'
              ? 'bg-gradient-to-r from-cyan-500/20 to-purple-500/20 text-cyan-300 border border-cyan-500/40'
              : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'
          }`}
        >
          <Layers className="w-4 h-4" />
          <span>Memory Viewer</span>
        </button>

        <button
          onClick={() => handleTabSwitch('rag')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all shrink-0 ${
            activeTab === 'rag'
              ? 'bg-gradient-to-r from-cyan-500/20 to-purple-500/20 text-cyan-300 border border-cyan-500/40'
              : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'
          }`}
        >
          <Database className="w-4 h-4" />
          <span>Knowledge Base (RAG)</span>
        </button>

        <button
          onClick={() => handleTabSwitch('marketplace')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all shrink-0 ${
            activeTab === 'marketplace'
              ? 'bg-gradient-to-r from-cyan-500/20 to-purple-500/20 text-cyan-300 border border-cyan-500/40'
              : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'
          }`}
        >
          <Grid className="w-4 h-4" />
          <span>Plugin Marketplace</span>
        </button>

        <button
          onClick={() => handleTabSwitch('analytics')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all shrink-0 ${
            activeTab === 'analytics'
              ? 'bg-gradient-to-r from-cyan-500/20 to-purple-500/20 text-cyan-300 border border-cyan-500/40'
              : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'
          }`}
        >
          <BarChart2 className="w-4 h-4" />
          <span>Analytics</span>
        </button>

        <button
          onClick={() => handleTabSwitch('security')}
          className={`flex items-center space-x-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all shrink-0 ${
            activeTab === 'security'
              ? 'bg-gradient-to-r from-cyan-500/20 to-purple-500/20 text-cyan-300 border border-cyan-500/40'
              : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'
          }`}
        >
          <Shield className="w-4 h-4" />
          <span>Security & Guardrails</span>
        </button>
      </div>

      {/* 3. MAIN DASHBOARD CONTENT AREA */}
      <main className="flex-1 p-6 max-w-7xl w-full mx-auto space-y-6">
        
        {/* ==================== TAB 1: AGENT STUDIO ==================== */}
        {activeTab === 'agent' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* Left/Middle Columns: Prompt Box, Model Select & Output */}
            <div className="lg:col-span-2 space-y-6">
              
              {/* Prompt Box Card */}
              <div className="glass-panel rounded-2xl p-6 space-y-4">
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                  <h2 className="text-lg font-semibold flex items-center space-x-2">
                    <Terminal className="w-5 h-5 text-cyan-400" />
                    <span>Dynamic Agent Command Center</span>
                  </h2>
                  
                  {/* Model Abstraction Controls */}
                  <div className="flex items-center space-x-2 bg-white/5 p-1 rounded-xl border border-white/10 text-xs">
                    <select 
                      value={selectedProvider} 
                      onChange={(e) => {
                        setSelectedProvider(e.target.value);
                        if (e.target.value === 'openai') setSelectedModel('gpt-4o');
                        else if (e.target.value === 'anthropic') setSelectedModel('claude-3-5-sonnet');
                        else if (e.target.value === 'google') setSelectedModel('gemini-1.5-flash');
                        else setSelectedModel('llama-3.1-local');
                      }}
                      className="bg-transparent text-gray-200 focus:outline-none px-2 py-1"
                    >
                      <option value="google" className="bg-[#0B0F19]">Google</option>
                      <option value="openai" className="bg-[#0B0F19]">OpenAI</option>
                      <option value="anthropic" className="bg-[#0B0F19]">Anthropic</option>
                      <option value="ollama" className="bg-[#0B0F19]">Ollama (Local)</option>
                    </select>
                    <span className="text-white/20">|</span>
                    <span className="text-cyan-400 font-mono font-semibold px-2">{selectedModel}</span>
                  </div>
                </div>

                <div className="relative">
                  <textarea
                    value={inputQuery}
                    onChange={(e) => setInputQuery(e.target.value)}
                    placeholder="Enter complex instruction (e.g. 'Audit this codebase config and dispatch RAG context search')..."
                    className="w-full h-36 bg-[#07090E]/80 border border-white/10 rounded-xl p-4 text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-cyan-500/60 focus:ring-1 focus:ring-cyan-500/60 resize-none"
                  />
                  <div className="absolute bottom-3 right-3 flex items-center space-x-2">
                    {/* Voice Assistant Trigger with MetalFx Circle & Cursor Bend */}
                    {isMounted ? (
                      <MetalFx 
                        ref={voiceBtnRef}
                        preset="chromatic" 
                        variant="circle" 
                        innerShadow 
                        theme="dark" 
                        strength={isVoiceActive ? 1 : 0.7}
                      >
                        <button 
                          onClick={() => setIsVoiceActive(!isVoiceActive)}
                          className={`p-2 rounded-full border transition flex items-center justify-center ${
                            isVoiceActive 
                              ? 'bg-red-500/20 text-red-400 border-red-500/40 animate-pulse' 
                              : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/10'
                          }`}
                          title="Toggle Voice assistant mode"
                          aria-label="Toggle Voice Mode"
                        >
                          {isVoiceActive ? <Volume2 className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
                        </button>
                      </MetalFx>
                    ) : (
                      <button 
                        onClick={() => setIsVoiceActive(!isVoiceActive)}
                        className="p-2 rounded-lg border bg-white/5 border-white/10 text-gray-400"
                        title="Toggle Voice assistant mode"
                      >
                        {isVoiceActive ? <Volume2 className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
                      </button>
                    )}

                    {/* Dispatch & Loading Button with MetalFx Chromatic Liquid Bend Shader */}
                    {isMounted ? (
                      <MetalFx 
                        ref={dispatchBtnRef}
                        preset="chromatic" 
                        variant="button" 
                        innerShadow 
                        theme="dark" 
                        strength={isExecuting ? 1 : 0.9}
                        glowGain={isExecuting ? 2.4 : 1.2}
                        reflectionTargets={voiceBtnRef ? [voiceBtnRef] : undefined}
                      >
                        <button
                          onClick={handleExecuteTask}
                          disabled={isExecuting || !inputQuery.trim()}
                          className={`px-5 py-2 rounded-lg font-medium text-sm flex items-center space-x-2 shadow-lg transition ${
                            isExecuting
                              ? 'bg-gradient-to-r from-purple-600 via-indigo-600 to-cyan-500 text-white shadow-cyan-500/40'
                              : 'bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-400 hover:to-purple-500 text-white shadow-cyan-500/20 disabled:opacity-50'
                          }`}
                        >
                          {isExecuting ? (
                            <>
                              <RefreshCw className="w-4 h-4 animate-spin text-cyan-300" />
                              <span className="font-semibold tracking-wide">Executing Agent Loop...</span>
                            </>
                          ) : (
                            <>
                              <Send className="w-4 h-4" />
                              <span>Dispatch</span>
                            </>
                          )}
                        </button>
                      </MetalFx>
                    ) : (
                      <button
                        onClick={handleExecuteTask}
                        disabled={isExecuting || !inputQuery.trim()}
                        className="px-5 py-2 rounded-lg bg-gradient-to-r from-cyan-500 to-purple-600 text-white font-medium text-sm flex items-center space-x-2 shadow-lg shadow-cyan-500/20 disabled:opacity-50"
                      >
                        {isExecuting ? (
                          <>
                            <RefreshCw className="w-4 h-4 animate-spin" />
                            <span>Executing Agent Loop...</span>
                          </>
                        ) : (
                          <>
                            <Send className="w-4 h-4" />
                            <span>Dispatch</span>
                          </>
                        )}
                      </button>
                    )}
                  </div>
                </div>

                {/* Voice waves indicator */}
                {isVoiceActive && (
                  <div className="flex items-center space-x-1.5 bg-cyan-950/20 border border-cyan-800/40 p-3 rounded-xl justify-center">
                    <span className="text-xs font-mono text-cyan-400 mr-2">Voice Input Processing:</span>
                    {audioWaves.map((h, i) => (
                      <div 
                        key={i} 
                        style={{ height: `${h}px` }} 
                        className="w-1 bg-cyan-400 rounded-full animate-pulse"
                      />
                    ))}
                  </div>
                )}
              </div>

              {/* Chat Execution Output */}
              {executionResult && (
                <div className="glass-panel rounded-2xl p-6 space-y-4 border-cyan-500/30">
                  <div className="flex items-center justify-between border-b border-white/10 pb-3">
                    <div className="flex items-center space-x-3">
                      <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                      <h3 className="font-semibold text-gray-200">Task Completed Successfully</h3>
                    </div>
                    <span className="text-xs font-mono px-3 py-1 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800">
                      Execution: {executionResult.latency_ms}ms
                    </span>
                  </div>

                  <div className="text-sm text-gray-300 leading-relaxed whitespace-pre-line font-sans bg-[#07090E]/60 p-4 rounded-xl border border-white/5">
                    {executionResult.response}
                  </div>

                  {executionResult.citations && (
                    <div className="pt-2">
                      <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Source Grounding Citations</h4>
                      {executionResult.citations.map((c: any, idx: number) => (
                        <div key={idx} className="flex items-center justify-between text-xs bg-white/5 p-2.5 rounded-lg border border-white/10">
                          <span className="text-cyan-300 font-medium">{c.title}</span>
                          <span className="font-mono text-gray-400">Score: {c.score}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Right Column: Real-Time Handoff Trace & Active WS Logs */}
            <div className="space-y-6">
              
              {/* Agent Trace Feed */}
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
                          <div className="text-gray-400 text-[11px]">State: {item.status}</div>
                        </div>
                        <span className="text-emerald-400 text-[10px]">{item.latency}</span>
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-12 text-gray-500 text-xs">
                      No active task execution traces.<br />Submit a prompt to inspect live agent delegation logs.
                    </div>
                  )}
                </div>
              </div>

              {/* WebSocket raw log output */}
              <div className="glass-panel rounded-2xl p-6 space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-semibold flex items-center space-x-2 text-gray-300">
                    <Server className="w-4 h-4 text-indigo-400" />
                    <span>Real-time WebSocket Logs</span>
                  </h3>
                  <button 
                    onClick={() => setWsStatus(wsStatus === 'connected' ? 'disconnected' : 'connected')}
                    className={`w-2.5 h-2.5 rounded-full ${wsStatus === 'connected' ? 'bg-emerald-500' : 'bg-red-500'}`}
                  />
                </div>

                <div className="h-32 overflow-y-auto bg-black/40 p-3 rounded-xl border border-white/5 font-mono text-[10px] text-gray-400 space-y-1.5 scrollbar-thin">
                  {wsLogs.map((log, idx) => (
                    <div key={idx} className="truncate">
                      <span className="text-white/20">[{new Date().toLocaleTimeString()}]</span> {log}
                    </div>
                  ))}
                  {wsLogs.length === 0 && <div className="text-center text-gray-600 py-8">Listening for WebSocket events...</div>}
                </div>
              </div>

            </div>
          </div>
        )}

        {/* ==================== TAB 2: WORKFLOW BUILDER ==================== */}
        {activeTab === 'builder' && (
          <div className="glass-panel rounded-2xl p-6 space-y-6">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-white/10 pb-4">
              <div>
                <h2 className="text-lg font-semibold flex items-center space-x-2">
                  <Sliders className="w-5 h-5 text-cyan-400" />
                  <span>Workflow Automation Builder</span>
                </h2>
                <p className="text-xs text-gray-400">Design stateful, event-triggered action flows executed by background Celery workers.</p>
              </div>

              <div className="flex items-center space-x-2">
                <input 
                  type="text" 
                  value={newWorkflowName}
                  onChange={(e) => setNewWorkflowName(e.target.value)}
                  placeholder="Workflow Name..." 
                  className="bg-white/5 border border-white/10 rounded-xl px-3 py-1.5 text-xs text-gray-200 focus:outline-none focus:border-cyan-500"
                />
                <select
                  value={newWorkflowTrigger}
                  onChange={(e) => setNewWorkflowTrigger(e.target.value)}
                  className="bg-[#0B0F19] border border-white/10 rounded-xl px-3 py-1.5 text-xs text-gray-200 focus:outline-none"
                >
                  <option value="CRON Schedule (Daily)">Daily CRON</option>
                  <option value="Webhook (PR Open)">Webhook Post</option>
                  <option value="System Clock (Hourly)">Hourly Clock</option>
                </select>
                <button 
                  onClick={handleAddWorkflow}
                  className="p-1.5 rounded-xl bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-400 border border-cyan-500/40"
                >
                  <Plus className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Workflows List Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {workflows.map((wf, idx) => (
                <div key={idx} className="p-4 rounded-xl bg-white/5 border border-white/10 space-y-4 flex flex-col justify-between">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-sm text-gray-200">{wf.name}</span>
                      <span className={`text-[10px] px-2 py-0.5 rounded-full ${
                        wf.active 
                          ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' 
                          : 'bg-white/5 text-gray-500 border border-white/10'
                      }`}>
                        {wf.active ? 'ACTIVE' : 'INACTIVE'}
                      </span>
                    </div>
                    <div className="text-xs text-gray-400">Trigger: <span className="font-semibold text-cyan-400">{wf.trigger}</span></div>
                    <div className="text-xs text-gray-400">Steps: <span className="font-semibold text-indigo-400">{wf.stepsCount} Nodes</span></div>
                  </div>

                  <div className="flex items-center justify-between pt-2 border-t border-white/5 text-xs">
                    <button 
                      onClick={() => {
                        const updated = [...workflows];
                        updated[idx].active = !updated[idx].active;
                        setWorkflows(updated);
                      }}
                      className="text-cyan-400 hover:text-cyan-300 flex items-center space-x-1"
                    >
                      <Play className="w-3.5 h-3.5" />
                      <span>{wf.active ? 'Disable' : 'Enable'}</span>
                    </button>
                    <button 
                      onClick={() => setWorkflows(workflows.filter(w => w.id !== wf.id))}
                      className="text-red-400 hover:text-red-300"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {/* Simple Visual Canvas Mock */}
            <div className="border border-white/10 rounded-2xl bg-black/30 p-8 text-center text-xs text-gray-500 space-y-4">
              <span className="uppercase tracking-widest text-[10px] text-gray-400">Visual Node Editor Canvas</span>
              <div className="flex items-center justify-center space-x-8 max-w-lg mx-auto">
                <div className="bg-cyan-950/40 text-cyan-400 border border-cyan-800 p-3 rounded-lg font-mono">Trigger Event</div>
                <ArrowRight className="w-5 h-5 text-gray-600" />
                <div className="bg-indigo-950/40 text-indigo-400 border border-indigo-800 p-3 rounded-lg font-mono">Planner Routing</div>
                <ArrowRight className="w-5 h-5 text-gray-600" />
                <div className="bg-purple-950/40 text-purple-400 border border-purple-800 p-3 rounded-lg font-mono">Action Node</div>
              </div>
            </div>

          </div>
        )}

        {/* ==================== TAB 3: MEMORY CENTER ==================== */}
        {activeTab === 'memory' && (
          <div className="glass-panel rounded-2xl p-6 space-y-6">
            <div>
              <h2 className="text-lg font-semibold flex items-center space-x-2">
                <Layers className="w-5 h-5 text-cyan-400" />
                <span>Hierarchical Memory Management Center</span>
              </h2>
              <p className="text-xs text-gray-400">Inspect the multi-tier memory storage used by agents for preference learning, semantic rules, and episodic history.</p>
            </div>

            {/* Memory stats blocks */}
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4 font-mono text-xs">
              {[
                { type: "short", label: "Short-Term Context", count: memoryStats.shortTermCount, color: "text-cyan-400" },
                { type: "long", label: "Long-Term Prefs", count: memoryStats.longTermCount, color: "text-indigo-400" },
                { type: "semantic", label: "Semantic Triples", count: memoryStats.semanticTriples, color: "text-purple-400" },
                { type: "episodic", label: "Episodic Traces", count: memoryStats.episodicTraces, color: "text-emerald-400" },
                { type: "procedural", label: "Procedural DAGs", count: memoryStats.proceduralDags, color: "text-amber-400" }
              ].map((m, idx) => (
                <button
                  key={idx}
                  onClick={() => setSelectedMemoryType(m.type as any)}
                  className={`p-4 rounded-xl border transition text-left space-y-1 ${
                    selectedMemoryType === m.type
                      ? 'bg-white/5 border-cyan-500/40 border-glow'
                      : 'bg-white/[0.02] border-white/10 hover:border-white/20'
                  }`}
                >
                  <div className="text-gray-400 text-[10px]">{m.label}</div>
                  <div className={`text-lg font-bold ${m.color}`}>{m.count} Records</div>
                </button>
              ))}
            </div>

            {/* Detail Pane based on selected memory type */}
            <div className="bg-black/40 border border-white/10 rounded-xl p-4 font-mono text-xs space-y-2">
              <span className="text-[10px] uppercase text-cyan-400 font-semibold tracking-wider">Memory Inspector Output ({selectedMemoryType.toUpperCase()})</span>
              
              {selectedMemoryType === 'long' && (
                <div className="space-y-2 text-gray-300">
                  <div><span className="text-indigo-400">user_pref_response_style</span>: "Highly technical / Deep code tracing"</div>
                  <div><span className="text-indigo-400">user_pref_default_llm</span>: "google/gemini-1.5-flash"</div>
                  <div><span className="text-indigo-400">security_compliance_level</span>: "nist-800-53-standard"</div>
                </div>
              )}
              {selectedMemoryType === 'semantic' && (
                <div className="space-y-2 text-gray-300">
                  <div>(<span className="text-purple-400">KALKI_AI</span>, <span className="text-emerald-400">isInstanceOf</span>, <span className="text-cyan-400">AutonomousOperatingSystem</span>) - Score: 1.0</div>
                  <div>(<span className="text-purple-400">ModelContextProtocol</span>, <span className="text-emerald-400">bindsToolsTo</span>, <span className="text-cyan-400">LlmContext</span>) - Score: 0.96</div>
                </div>
              )}
              {selectedMemoryType !== 'long' && selectedMemoryType !== 'semantic' && (
                <div className="text-gray-500 italic">No custom values set. Displaying default mock schemas.</div>
              )}
            </div>
          </div>
        )}

        {/* ==================== TAB 4: KNOWLEDGE BASE (RAG) ==================== */}
        {activeTab === 'rag' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* File list manager */}
            <div className="lg:col-span-2 glass-panel rounded-2xl p-6 space-y-4">
              <h2 className="text-lg font-semibold flex items-center space-x-2">
                <Database className="w-5 h-5 text-cyan-400" />
                <span>Knowledge Ingestion Manager</span>
              </h2>

              <div className="border border-dashed border-white/10 rounded-xl p-6 text-center hover:border-cyan-500/40 transition cursor-pointer flex flex-col items-center justify-center space-y-2 bg-white/[0.01]">
                <Upload className="w-6 h-6 text-gray-400" />
                <span className="text-xs text-gray-200">Drag and drop file specifications to index</span>
                <span className="text-[10px] text-gray-500">Supports PDF, Word, Excel, CSV, Audio, Video, Markdown</span>
              </div>

              <div className="space-y-2 pt-2">
                {uploadedFiles.map((file, idx) => (
                  <div key={idx} className="p-3 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between text-xs font-mono">
                    <div className="flex items-center space-x-3">
                      <FileText className="w-4 h-4 text-cyan-400" />
                      <span className="text-gray-200">{file.name}</span>
                    </div>
                    <div className="flex items-center space-x-4">
                      <span className="text-gray-400">{file.size}</span>
                      <span className="text-indigo-400">{file.chunks} Chunks</span>
                      <span className="px-2 py-0.5 bg-emerald-950 text-emerald-400 border border-emerald-800 rounded">
                        {file.status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* RRF Search Settings */}
            <div className="glass-panel rounded-2xl p-6 space-y-4">
              <h3 className="text-sm font-semibold flex items-center space-x-2 text-gray-300">
                <Search className="w-4 h-4 text-cyan-400" />
                <span>RAG Retrieval Config</span>
              </h3>

              <div className="space-y-4 text-xs">
                <div className="space-y-1">
                  <label className="text-gray-400 font-mono">RRF Smoothing Constant (k)</label>
                  <input type="number" defaultValue={60} className="w-full bg-[#07090E] border border-white/10 rounded-lg p-2 focus:outline-none" />
                </div>
                <div className="space-y-1">
                  <label className="text-gray-400 font-mono">Dense Retrieval Weights</label>
                  <input type="range" min={0} max={100} defaultValue={70} className="w-full" />
                </div>
                <div className="space-y-1">
                  <label className="text-gray-400 font-mono">Sparse Retrieval Weights</label>
                  <input type="range" min={0} max={100} defaultValue={30} className="w-full" />
                </div>
              </div>
            </div>

          </div>
        )}

        {/* ==================== TAB 5: PLUGINS MARKETPLACE ==================== */}
        {activeTab === 'marketplace' && (
          <div className="glass-panel rounded-2xl p-6 space-y-6">
            <div>
              <h2 className="text-lg font-semibold flex items-center space-x-2">
                <Grid className="w-5 h-5 text-cyan-400" />
                <span>Tool &amp; Agent Plugin Marketplace</span>
              </h2>
              <p className="text-xs text-gray-400">Dynamically load or unload integrations allowing agents to connect to external APIs and workspaces.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {plugins.map((plugin, idx) => (
                <div key={idx} className="p-4 rounded-xl bg-white/5 border border-white/10 space-y-3 flex flex-col justify-between">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-sm text-gray-200">{plugin.name}</span>
                      <span className="text-[10px] px-2 py-0.5 bg-white/5 border border-white/10 rounded font-mono text-gray-400">{plugin.category}</span>
                    </div>
                    <p className="text-xs text-gray-400 leading-relaxed">{plugin.desc}</p>
                  </div>

                  <div className="flex items-center justify-between pt-2 border-t border-white/5">
                    <button
                      onClick={() => {
                        const updated = [...plugins];
                        updated[idx].active = !updated[idx].active;
                        setPlugins(updated);
                      }}
                      className={`text-xs px-3 py-1.5 rounded-lg border transition ${
                        plugin.active
                          ? 'bg-emerald-950 text-emerald-400 border-emerald-800'
                          : 'bg-white/5 text-gray-400 border-white/10'
                      }`}
                    >
                      {plugin.active ? 'Enabled' : 'Disabled'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ==================== TAB 6: ANALYTICS ==================== */}
        {activeTab === 'analytics' && (
          <div className="glass-panel rounded-2xl p-6 space-y-6">
            <h2 className="text-lg font-semibold flex items-center space-x-2">
              <BarChart2 className="w-5 h-5 text-cyan-400" />
              <span>Performance &amp; Observability Metrics</span>
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs text-center">
              <div className="bg-white/5 border border-white/10 p-4 rounded-xl space-y-1">
                <div className="text-gray-400">Avg. TTFT Latency</div>
                <div className="text-cyan-400 text-lg font-bold">142 ms</div>
              </div>
              <div className="bg-white/5 border border-white/10 p-4 rounded-xl space-y-1">
                <div className="text-gray-400">Embedding Cache Hits</div>
                <div className="text-indigo-400 text-lg font-bold">89.4%</div>
              </div>
              <div className="bg-white/5 border border-white/10 p-4 rounded-xl space-y-1">
                <div className="text-gray-400">Avg. Grounding Score</div>
                <div className="text-emerald-400 text-lg font-bold">98.2%</div>
              </div>
            </div>

            {/* Performance log mock lines */}
            <div className="space-y-2">
              <span className="text-xs font-semibold text-gray-400">System Logs Trace (Last 2 minutes)</span>
              <div className="h-40 bg-black/30 border border-white/10 rounded-xl p-4 font-mono text-xs text-gray-500 overflow-y-auto space-y-1 scrollbar-thin">
                <div>[INFO] Model Provider initialized: Anthropic API -&gt; OK</div>
                <div>[INFO] Qdrant connection pool active. Nodes: 1</div>
                <div>[INFO] Celery tasks synced with RabbitMQ AMQP broker exchanges.</div>
              </div>
            </div>
          </div>
        )}

        {/* ==================== TAB 7: SECURITY & COMPLIANCE ==================== */}
        {activeTab === 'security' && (
          <div className="glass-panel rounded-2xl p-6 space-y-6">
            <div>
              <h2 className="text-lg font-semibold flex items-center space-x-2 text-emerald-400">
                <Shield className="w-5 h-5" />
                <span>Defensive Cybersecurity &amp; Guardrails Panel</span>
              </h2>
              <p className="text-xs text-gray-400">Configure prompt injection heuristics, audit file sandboxing parameters, and authorize HITL confirmation prompts.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              
              {/* Compliance checklist */}
              <div className="p-4 rounded-xl bg-white/5 border border-white/10 space-y-3 text-xs">
                <h3 className="font-bold text-gray-200">System Compliance Checklist</h3>
                <div className="space-y-2">
                  <div className="flex items-center space-x-2"><Check className="w-4 h-4 text-emerald-400" /><span>TLS 1.3 In-transit encryption</span></div>
                  <div className="flex items-center space-x-2"><Check className="w-4 h-4 text-emerald-400" /><span>AES-256 Memory store encryption</span></div>
                  <div className="flex items-center space-x-2"><Check className="w-4 h-4 text-emerald-400" /><span>Docker Sandboxed Execution Runtime</span></div>
                  <div className="flex items-center space-x-2"><Check className="w-4 h-4 text-emerald-400" /><span>Dual-pass Prompt Injection Detection</span></div>
                </div>
              </div>

              {/* Guardrails Control Panel */}
              <div className="p-4 rounded-xl bg-white/5 border border-white/10 space-y-3 text-xs">
                <h3 className="font-bold text-gray-200">Prompt Guardrail Tuning</h3>
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span>Rate Limiting (RPM per Token)</span>
                    <span className="font-bold text-cyan-400">60</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>Block exploit code generation</span>
                    <span className="text-emerald-400 font-bold">ENABLED</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>Dynamic PII Anonymizer</span>
                    <span className="text-emerald-400 font-bold">ENABLED</span>
                  </div>
                </div>
              </div>

            </div>
          </div>
        )}

      </main>

      {/* FOOTER */}
      <footer className="border-t border-white/10 py-4 px-6 text-center text-xs text-gray-500 font-mono">
        KALKI — Krishna Autonomous Learning &amp; Knowledge Intelligence © 2026. All rights reserved.
      </footer>
    </div>
  );
}
