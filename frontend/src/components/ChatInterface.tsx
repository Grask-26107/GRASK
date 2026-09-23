import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  Send,
  Sparkles,
  Copy,
  Check,
  ThumbsUp,
  ThumbsDown,
  BookOpen,
  Volume2,
  VolumeX,
  Mic,
  MicOff,
  RotateCcw,
  ShieldCheck,
  AlertTriangle,
  FileSpreadsheet,
  ChevronDown,
  ChevronUp,
  HelpCircle,
  Globe,
  Loader2,
  Menu,
  Camera,
  Search,
  FileCheck2,
  ArrowUp
} from 'lucide-react';
import { ChatMode, ChatMessage, Citation } from '../types';
import { chatApi, feedbackApi } from '../services/api';
import { SUPPORTED_LANGUAGES } from '../constants/languages';
export { SUPPORTED_LANGUAGES };

interface ChatInterfaceProps {
  currentMode: ChatMode;
  onModeChange: (mode: ChatMode) => void;
  onSelectCitation: (citation: Citation) => void;
  addToast: (type: 'success' | 'error' | 'info', message: string) => void;
  onToggleSidebar?: () => void;
  onOpenLicenseVerify?: () => void;
  onOpenComplianceAudit?: () => void;
  onOpenNutriScore?: () => void;
  selectedLanguage: string;
  onLanguageChange: (lang: string) => void;
  messages: ChatMessage[];
  setMessages: React.Dispatch<React.SetStateAction<ChatMessage[]>>;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  currentMode,
  onModeChange,
  onSelectCitation,
  addToast,
  onToggleSidebar,
  onOpenLicenseVerify,
  onOpenComplianceAudit,
  onOpenNutriScore,
  selectedLanguage,
  onLanguageChange,
  messages,
  setMessages,
}) => {
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedStandard, setSelectedStandard] = useState<string>('');
  const [samplePrompts, setSamplePrompts] = useState<any>(null);
  const [expandedCitations, setExpandedCitations] = useState<Record<string, boolean>>({});
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [isSpeaking, setIsSpeaking] = useState<string | null>(null);
  const [isListening, setIsListening] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load sample prompts
  useEffect(() => {
    const fetchPrompts = async () => {
      try {
        const data = await chatApi.getSamplePrompts();
        setSamplePrompts(data);
      } catch (err) {
        console.error('Failed to load sample prompts:', err);
      }
    };
    fetchPrompts();
  }, []);

  // Welcome message synchronized with currentMode
  useEffect(() => {
    if (messages.length === 0 || (messages.length === 1 && messages[0].id === 'welcome-01')) {
      const isConsumer = currentMode === 'consumer';
      const modeTitle = isConsumer ? 'CITIZEN & CONSUMER SAFETY MODE' : 'INDUSTRY & ENGINEERING MODE';
      const introText = isConsumer
        ? `I am your **Citizen & Consumer Safety Guide** for Indian Standards.\n\n` +
          `I explain product quality benchmarks in plain English, help you identify authentic **ISI Marks**, **CRS Registration (R-Numbers)**, **6-digit laser HUID Gold Hallmarks**, and guide you on verifying product licenses via the **BIS Care Mobile App**.`
        : `I am your **Technical Assistant & Certification Advisor** for Industry, Manufacturers, and Accredited Testing Labs.\n\n` +
          `I provide exact numerical tables, chemical bounds, tolerances, sampling protocols, and certification pathways across all 17 BIS Technical Departments (24,084 Standards).`;

      setMessages([
        {
          id: 'welcome-01',
          role: 'assistant',
          content:
            `### 🇮🇳 Welcome to GRASK AI (Bureau of Indian Standards — SIH26107)\n\n` +
            `${introText}\n\n` +
            `**Currently Operating in:** \`${modeTitle}\`\n\n` +
            `Ask about any Indian Standard, ISO Certification, Store Licensing or product specification (e.g. **IS 14543** Packaged Water, **IS 1786** TMT Steel, **ISO 9001 / ISO 27001**, **Opening a Medical Store / Grocery Shop**, **IS 2796** Petrol Bunks, **IS 1293** Plugs & Sockets, **IS 4151** Helmets).`,
          mode: currentMode,
          confidence_score: 1.0,
          timestamp: new Date().toLocaleTimeString(),
        },
      ]);
    }
  }, [currentMode]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSendMessage = async (textToSend?: string) => {
    const message = textToSend || inputMessage;
    if (!message.trim() || loading) return;

    const userMessageId = `usr-${Date.now()}`;
    const newMessages: ChatMessage[] = [
      ...messages,
      {
        id: userMessageId,
        role: 'user',
        content: message,
        timestamp: new Date().toLocaleTimeString(),
      },
    ];

    setMessages(newMessages);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await chatApi.sendMessage(
        message,
        currentMode,
        selectedStandard || undefined,
        newMessages,
        selectedLanguage
      );

      const assistantMsg: ChatMessage = {
        id: response?.id || `ast-${Date.now()}`,
        role: 'assistant',
        content: typeof response?.answer === 'string' ? response.answer : String(response?.answer || ''),
        mode: response?.mode || currentMode,
        citations: Array.isArray(response?.citations) ? response.citations : [],
        table_references: Array.isArray(response?.table_references) ? response.table_references : [],
        confidence_score: typeof response?.confidence_score === 'number' ? response.confidence_score : 0.95,
        refusal_triggered: Boolean(response?.refusal_triggered),
        needs_clarification: Boolean(response?.needs_clarification),
        disambiguation_options: Array.isArray(response?.disambiguation_options) ? response.disambiguation_options : [],
        suggested_followups: Array.isArray(response?.suggested_followups) ? response.suggested_followups : [],
        language: response?.language || selectedLanguage,
        timestamp: new Date().toLocaleTimeString(),
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      addToast('error', err.response?.data?.detail || 'Failed to reach BIS RAG Engine.');
      setMessages((prev) => [
        ...prev,
        {
          id: `err-${Date.now()}`,
          role: 'assistant',
          content: '⚠️ **Error:** Unable to connect to the backend server. Please verify that the FastAPI backend is running on `http://127.0.0.1:8000`.',
          timestamp: new Date().toLocaleTimeString(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (messageId: string, rating: 'thumbs_up' | 'thumbs_down', queryText?: string, responseText?: string) => {
    try {
      await feedbackApi.submitFeedback(messageId, rating, queryText, responseText, currentMode);
      setMessages((prev) =>
        prev.map((m) => (m.id === messageId ? { ...m, feedbackGiven: rating } : m))
      );
      addToast('success', 'Thank you! Feedback logged for Government Accuracy Oversight.');
    } catch (err) {
      addToast('error', 'Failed to submit feedback.');
    }
  };

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    addToast('info', 'Copied to clipboard!');
    setTimeout(() => setCopiedId(null), 2000);
  };

  const toggleSpeech = (text: string, id: string, msgLanguage?: string) => {
    if (!('speechSynthesis' in window)) {
      addToast('error', 'Text-to-Speech is not supported in this browser.');
      return;
    }

    if (isSpeaking === id) {
      window.speechSynthesis.cancel();
      setIsSpeaking(null);
    } else {
      window.speechSynthesis.cancel();
      const cleanText = text.replace(/[#*`_\[\]]/g, '');
      const utterance = new SpeechSynthesisUtterance(cleanText);
      const activeLangObj = SUPPORTED_LANGUAGES.find(
        (l) => l.code === (msgLanguage || selectedLanguage)
      ) || SUPPORTED_LANGUAGES[0];
      utterance.lang = activeLangObj.voice;
      utterance.rate = 1.0;
      utterance.onend = () => setIsSpeaking(null);
      utterance.onerror = () => setIsSpeaking(null);
      window.speechSynthesis.speak(utterance);
      setIsSpeaking(id);
    }
  };

  const toggleSpeechRecognition = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      addToast('error', 'Speech-to-Text is not supported in this browser.');
      return;
    }

    if (isListening) {
      setIsListening(false);
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      const activeLangObj = SUPPORTED_LANGUAGES.find((l) => l.code === selectedLanguage) || SUPPORTED_LANGUAGES[0];
      recognition.lang = activeLangObj.voice;
      recognition.interimResults = false;

      recognition.onstart = () => {
        setIsListening(true);
        addToast('info', `🎤 Listening in ${activeLangObj.name} (${activeLangObj.native})... Speak your query.`);
      };

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        if (transcript) {
          setInputMessage((prev) => (prev ? `${prev} ${transcript}` : transcript));
          addToast('success', `Voice captured: "${transcript}". Click Send to query or continue speaking.`);
        }
        setIsListening(false);
      };

      recognition.onerror = () => {
        setIsListening(false);
        addToast('error', 'Speech recognition error.');
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognition.start();
    } catch (err) {
      setIsListening(false);
      addToast('error', 'Could not activate microphone.');
    }
  };

  const handleTranslateMessage = async (messageId: string, targetLanguage: string) => {
    const targetMsg = messages.find((m) => m.id === messageId);
    if (!targetMsg) return;

    if (targetLanguage === 'en' && targetMsg.original_content) {
      setMessages((prev) =>
        prev.map((m) =>
          m.id === messageId
            ? { ...m, content: m.original_content!, language: 'en' }
            : m
        )
      );
      addToast('info', 'Reverted message to English.');
      return;
    }

    setMessages((prev) =>
      prev.map((m) => (m.id === messageId ? { ...m, is_translating: true } : m))
    );

    try {
      const sourceText = targetMsg.original_content || targetMsg.content;
      const res = await chatApi.translateMessage(sourceText, targetLanguage);
      setMessages((prev) =>
        prev.map((m) =>
          m.id === messageId
            ? {
                ...m,
                content: res.translated_text,
                original_content: sourceText,
                language: targetLanguage,
                is_translating: false,
              }
            : m
        )
      );
      addToast('success', `Translated into ${res.language_name} (${res.native_name})! Click 🔊 to listen.`);
    } catch (err) {
      setMessages((prev) =>
        prev.map((m) => (m.id === messageId ? { ...m, is_translating: false } : m))
      );
      addToast('error', 'Translation failed. Please try again.');
    }
  };

  const clearChat = () => {
    setMessages([]);
    addToast('info', 'Chat history cleared.');
  };

  const toggleCitationDrawer = (msgId: string) => {
    setExpandedCitations((prev) => ({ ...prev, [msgId]: !prev[msgId] }));
  };

  const currentSamplePrompts = samplePrompts ? samplePrompts[currentMode] || [] : [];

  const quickTopicPills = [
    { id: 'water', label: '💧 Water (IS 14543)', query: 'What are the permissible limits for Lead, Arsenic, and TDS in Packaged Drinking Water under IS 14543?' },
    { id: 'steel', label: '🏗️ TMT Steel (IS 1786)', query: 'What are the yield strength, chemical limits, and bend test requirements for Fe 500D TMT bars under IS 1786?' },
    { id: 'gold', label: '👑 Gold Hallmark HUID', query: 'How does a consumer verify 6-digit HUID gold hallmarking on the BIS Care App?' },
    { id: 'helmets', label: '🪖 Two-Wheeler Helmet (IS 4151)', query: 'What impact attenuation and chin strap tests are required for helmets under IS 4151?' },
    { id: 'crs', label: '💻 Electronics CRS (IS 13252)', query: 'How to obtain BIS CRS registration (R-Number) for laptops and mobile phones under Scheme-II?' },
    { id: 'scheme-1', label: '🏷️ Scheme-I ISI Mark', query: 'What is the step-by-step application procedure for Scheme-I ISI Mark on BIS Manakonline?' }
  ];

  return (
    <div className="flex flex-col h-full w-full bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 relative">
      {/* Top ChatGPT-style Minimal Bar */}
      <div className="h-14 border-b border-slate-200 dark:border-slate-800 px-4 flex items-center justify-between bg-white/80 dark:bg-slate-900/80 backdrop-blur-md shrink-0 z-10">
        <div className="flex items-center space-x-3">
          {onToggleSidebar && (
            <button
              type="button"
              onClick={onToggleSidebar}
              className="p-1.5 rounded-lg text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer"
              title="Toggle Sidebar"
              aria-label="Toggle Sidebar"
            >
              <Menu className="w-5 h-5" />
            </button>
          )}

          {/* Mode Pill Toggle */}
          <div className="flex items-center bg-slate-100 dark:bg-slate-800 p-0.5 rounded-xl border border-slate-200 dark:border-slate-700/60 text-xs">
            <button
              onClick={() => {
                if (currentMode !== 'industry') {
                  setMessages([]);
                  onModeChange('industry');
                  addToast('info', 'Switched to Industry & Engineering Mode (Chat Cleared).');
                }
              }}
              className={`px-2.5 py-1 rounded-lg font-semibold flex items-center space-x-1 transition-all ${
                currentMode === 'industry'
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              <span>🏭 Industry</span>
            </button>
            <button
              onClick={() => {
                if (currentMode !== 'consumer') {
                  setMessages([]);
                  onModeChange('consumer');
                  addToast('info', 'Switched to Citizen & Consumer Mode (Chat Cleared).');
                }
              }}
              className={`px-2.5 py-1 rounded-lg font-semibold flex items-center space-x-1 transition-all ${
                currentMode === 'consumer'
                  ? 'bg-emerald-600 text-white shadow-sm'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              <span>👥 Citizen</span>
            </button>
          </div>

          {/* Quick Shortcuts */}
          {onOpenLicenseVerify && (
            <button
              onClick={onOpenLicenseVerify}
              className="hidden sm:inline-flex items-center space-x-1 px-2.5 py-1 rounded-lg text-xs font-semibold bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800/60 hover:bg-amber-100 transition-colors"
            >
              <Camera className="w-3.5 h-3.5" />
              <span>Verify Mark / HUID</span>
            </button>
          )}

          {onOpenComplianceAudit && (
            <button
              onClick={onOpenComplianceAudit}
              className="hidden md:inline-flex items-center space-x-1 px-2.5 py-1 rounded-lg text-xs font-semibold bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/60 hover:bg-emerald-100 transition-colors"
            >
              <FileCheck2 className="w-3.5 h-3.5" />
              <span>Audit Studio</span>
            </button>
          )}

          {onOpenNutriScore && (
            <button
              onClick={onOpenNutriScore}
              className="inline-flex items-center space-x-1 px-2.5 py-1 rounded-lg text-xs font-semibold bg-teal-50 dark:bg-teal-950/40 text-teal-700 dark:text-teal-300 border border-teal-200 dark:border-teal-800/60 hover:bg-teal-100 transition-colors"
            >
              <span>🥗</span>
              <span className="hidden sm:inline">Nutri-Score & Ingredients</span>
              <span className="sm:hidden">Nutri-Score</span>
            </button>
          )}

          {/* Single Official Translation Selector (Beside Nutri-Score) */}
          <div className="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold bg-blue-50 dark:bg-blue-950/40 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800/60 shadow-xs">
            <Globe className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400 shrink-0" />
            <select
              value={selectedLanguage}
              onChange={(e) => onLanguageChange(e.target.value)}
              className="bg-transparent text-xs font-semibold text-blue-800 dark:text-blue-200 focus:outline-none cursor-pointer pr-1"
              title="Select National Translation Language"
            >
              {SUPPORTED_LANGUAGES.map((l) => (
                <option key={l.code} value={l.code} className="bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100">
                  {l.flag} {l.name} ({l.native})
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Right side controls */}
        <div className="flex items-center space-x-2">
          {/* Clear Session */}
          <button
            onClick={clearChat}
            className="p-1.5 text-slate-400 hover:text-rose-500 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors text-xs flex items-center space-x-1"
            title="Reset Chat"
          >
            <RotateCcw className="w-4 h-4" />
            <span className="hidden sm:inline">Reset</span>
          </button>
        </div>
      </div>

      {/* Main Messages Stream Container (ChatGPT Layout) */}
      <div className="flex-1 overflow-y-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6 max-w-4xl mx-auto w-full">
        {/* Quick Topic Chips */}
        <div className="flex items-center gap-1.5 overflow-x-auto whitespace-nowrap pb-1 scrollbar-none">
          {quickTopicPills.map((pill) => (
            <button
              key={pill.id}
              onClick={() => handleSendMessage(pill.query)}
              className="flex-shrink-0 flex items-center space-x-1 px-2.5 py-1 rounded-xl text-xs font-medium bg-slate-100 dark:bg-slate-800/90 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-700/80 hover:border-blue-500 hover:text-blue-600 dark:hover:text-sky-300 shadow-sm transition-all"
            >
              <span>{pill.label}</span>
            </button>
          ))}
        </div>

        {/* Message Feed */}
        {messages.map((msg) => {
          const isAssistant = msg.role === 'assistant';
          const hasCitations = msg.citations && msg.citations.length > 0;
          const isRefusal = msg.refusal_triggered;

          return (
            <div
              key={msg.id}
              className={`flex flex-col ${isAssistant ? 'items-start' : 'items-end'} animate-in fade-in duration-200`}
            >
              {/* Message Bubble Container */}
              <div
                className={`max-w-[95%] sm:max-w-[88%] rounded-2xl p-4 sm:p-5 shadow-sm border transition-all ${
                  isAssistant
                    ? isRefusal
                      ? 'bg-rose-50/90 dark:bg-rose-950/30 border-rose-200 dark:border-rose-900/60 text-slate-900 dark:text-slate-100'
                      : 'bg-white dark:bg-slate-800/80 border-slate-200/90 dark:border-slate-700/80 text-slate-900 dark:text-slate-100'
                    : 'bg-gradient-to-r from-blue-700 to-blue-800 text-white border-blue-600 self-end shadow-md shadow-blue-900/10'
                }`}
              >
                {/* Assistant Message Header */}
                {isAssistant && (
                  <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-100 dark:border-slate-700/60 text-xs">
                    <div className="flex items-center space-x-2">
                      <div className="w-5 h-5 rounded-md bg-gradient-to-tr from-blue-800 to-indigo-600 flex items-center justify-center text-white text-[10px] font-black shadow-sm">
                        🇮🇳
                      </div>
                      <span className="font-extrabold text-slate-900 dark:text-white tracking-tight">
                        GRASK AI
                      </span>
                      <span
                        className={`text-[10px] px-2 py-0.5 rounded-full font-semibold ${
                          (msg.mode || currentMode) === 'consumer'
                            ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300'
                            : 'bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300'
                        }`}
                      >
                        {(msg.mode || currentMode) === 'consumer' ? 'Citizen Mode' : 'Industry Mode'}
                      </span>
                    </div>

                    {msg.confidence_score !== undefined && (
                      <div className="flex items-center space-x-1.5 font-mono text-[11px] text-slate-500 dark:text-slate-400">
                        <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />
                        <span>Confidence: {Math.round(msg.confidence_score * 100)}%</span>
                      </div>
                    )}
                  </div>
                )}

                {/* Markdown Content */}
                <div className="markdown-content text-sm leading-relaxed">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {typeof msg.content === 'string' ? msg.content : String(msg.content || '')}
                  </ReactMarkdown>
                </div>

                {/* Grounded Citations Accordion */}
                {isAssistant && hasCitations && (
                  <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-700/60">
                    <button
                      onClick={() => toggleCitationDrawer(msg.id)}
                      className="flex items-center justify-between w-full text-xs font-bold text-blue-700 dark:text-blue-400 hover:opacity-80 py-1"
                    >
                      <div className="flex items-center space-x-1.5">
                        <BookOpen className="w-3.5 h-3.5" />
                        <span>Authoritative BIS Citations ({msg.citations?.length})</span>
                      </div>
                      {expandedCitations[msg.id] ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                    </button>

                    {expandedCitations[msg.id] && (
                      <div className="mt-2 space-y-2 pt-2">
                        {msg.citations?.map((cit, idx) => (
                          <div
                            key={idx}
                            onClick={() => onSelectCitation(cit)}
                            className="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-700/60 hover:border-blue-500 cursor-pointer transition-all text-xs"
                          >
                            <div className="flex items-center justify-between">
                              <span className="font-bold text-blue-600 dark:text-blue-400 font-mono">
                                {cit.is_code}
                              </span>
                              <span className="text-[10px] text-slate-400">
                                Page {cit.page_number} • {cit.clause}
                              </span>
                            </div>
                            <p className="text-[11px] text-slate-600 dark:text-slate-300 mt-1 line-clamp-2">
                              {cit.snippet}
                            </p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {/* Google-style "Did you mean?" Disambiguation Options */}
                {isAssistant && msg.disambiguation_options && msg.disambiguation_options.length > 0 && (
                  <div className="mt-3.5 pt-3 border-t border-slate-200/80 dark:border-slate-700/80">
                    <div className="flex items-center space-x-1.5 text-xs font-semibold text-blue-600 dark:text-blue-400 mb-2">
                      <Search className="w-3.5 h-3.5" />
                      <span>{msg.needs_clarification ? 'Select intended standardization topic:' : 'Did you mean? (Quick topics):'}</span>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {msg.disambiguation_options.map((opt, optIdx) => (
                        <button
                          key={optIdx}
                          onClick={() => handleSendMessage(opt.query)}
                          className="text-left p-2.5 rounded-xl border border-blue-200 dark:border-blue-800/80 bg-blue-50/60 dark:bg-blue-950/30 hover:bg-blue-100/80 dark:hover:bg-blue-900/50 hover:border-blue-400 transition-all cursor-pointer group shadow-xs"
                        >
                          <div className="font-semibold text-xs text-blue-900 dark:text-blue-200 group-hover:text-blue-700 dark:group-hover:text-blue-100">
                            {opt.label}
                          </div>
                          {opt.description && (
                            <div className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5 line-clamp-1">
                              {opt.description}
                            </div>
                          )}
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* Action Toolbar on Assistant Messages */}
                {isAssistant && (
                  <div className="mt-3 pt-2.5 border-t border-slate-100 dark:border-slate-700/60 flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
                    <span className="text-[10px]">{msg.timestamp}</span>

                    <div className="flex items-center space-x-1.5">
                      {/* Copy */}
                      <button
                        onClick={() => handleCopy(msg.content, msg.id)}
                        className="p-1 rounded hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 transition-colors"
                        title="Copy answer"
                      >
                        {copiedId === msg.id ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
                      </button>

                      {/* Text to Speech */}
                      <button
                        onClick={() => toggleSpeech(msg.content, msg.id, msg.language)}
                        className={`p-1 rounded hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors ${
                          isSpeaking === msg.id ? 'text-blue-600 dark:text-blue-400 animate-pulse' : 'text-slate-400 hover:text-slate-700'
                        }`}
                        title={isSpeaking === msg.id ? 'Stop reading' : 'Read aloud in native language'}
                      >
                        {isSpeaking === msg.id ? <VolumeX className="w-3.5 h-3.5" /> : <Volume2 className="w-3.5 h-3.5" />}
                      </button>

                      {/* Thumbs Up */}
                      <button
                        onClick={() => handleFeedback(msg.id, 'thumbs_up', messages[messages.indexOf(msg) - 1]?.content, msg.content)}
                        disabled={msg.feedbackGiven !== undefined && msg.feedbackGiven !== null}
                        className={`p-1 rounded hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors ${
                          msg.feedbackGiven === 'thumbs_up'
                            ? 'text-emerald-600 dark:text-emerald-400'
                            : 'text-slate-400 hover:text-emerald-600'
                        }`}
                        title="Accurate Grounding"
                      >
                        <ThumbsUp className="w-3.5 h-3.5" />
                      </button>

                      {/* Thumbs Down */}
                      <button
                        onClick={() => handleFeedback(msg.id, 'thumbs_down', messages[messages.indexOf(msg) - 1]?.content, msg.content)}
                        disabled={msg.feedbackGiven !== undefined && msg.feedbackGiven !== null}
                        className={`p-1 rounded hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors ${
                          msg.feedbackGiven === 'thumbs_down'
                            ? 'text-rose-600 dark:text-rose-400'
                            : 'text-slate-400 hover:text-rose-600'
                        }`}
                        title="Report Discrepancy"
                      >
                        <ThumbsDown className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {/* Starter Prompts when only welcome message exists */}
        {messages.length <= 1 && currentSamplePrompts.length > 0 && (
          <div className="pt-4 pb-2">
            <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-3 flex items-center space-x-1.5">
              <Sparkles className="w-3.5 h-3.5 text-amber-500" />
              <span>Suggested prompts for {currentMode === 'industry' ? 'Industry & Engineers' : 'Citizens & Consumers'}:</span>
            </span>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              {currentSamplePrompts.map((item: any, idx: number) => (
                <button
                  key={idx}
                  onClick={() => handleSendMessage(item.prompt)}
                  className="text-left p-3.5 rounded-2xl bg-slate-50 dark:bg-slate-800/60 hover:bg-slate-100 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-700/60 hover:border-blue-500 text-xs cursor-pointer group transition-all"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-[10px] font-bold text-blue-600 dark:text-blue-400">
                      {item.standard}
                    </span>
                    <span className="text-[10px] opacity-0 group-hover:opacity-100 text-blue-500 transition-opacity">Ask →</span>
                  </div>
                  <span className="font-semibold text-slate-800 dark:text-slate-200 block mt-1">
                    {item.title}
                  </span>
                  <p className="text-[11px] text-slate-500 dark:text-slate-400 line-clamp-1 mt-0.5">{item.prompt}</p>
                </button>
              ))}
            </div>
          </div>
        )}

        {loading && (
          <div className="flex items-center space-x-2 text-slate-500 dark:text-slate-400 text-xs p-3">
            <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
            <span>Grounding response in Bureau of Indian Standards clauses & tables...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* ChatGPT-style Floating Centered Bottom Input Bar */}
      <div className="p-4 shrink-0 bg-gradient-to-t from-white via-white to-transparent dark:from-slate-900 dark:via-slate-900 dark:to-transparent">
        <div className="max-w-3xl mx-auto w-full">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="relative bg-white dark:bg-slate-800 rounded-2xl border border-slate-300 dark:border-slate-700 shadow-lg flex items-center p-2 transition-all focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-500/20"
          >
            {/* MANAK-Vision Camera / Attachment Trigger */}
            {onOpenLicenseVerify && (
              <button
                type="button"
                onClick={onOpenLicenseVerify}
                className="p-2 text-slate-400 hover:text-blue-600 dark:hover:text-blue-400 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-700/60 transition-colors"
                title="Verify CM/L License, HUID or Scan Mark (MANAK-Vision)"
              >
                <Camera className="w-5 h-5" />
              </button>
            )}

            {/* FSSAI Nutri-Score & Hidden Ingredient Decrypter */}
            {onOpenNutriScore && (
              <button
                type="button"
                onClick={onOpenNutriScore}
                className="p-2 text-slate-400 hover:text-emerald-600 dark:hover:text-emerald-400 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-700/60 transition-colors"
                title="FSSAI Nutri-Score & Hidden Ingredient Decrypter (Harmful vs Secure)"
              >
                <span className="text-base leading-none">🥗</span>
              </button>
            )}

            {/* Input Text Field */}
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder={
                currentMode === 'industry'
                  ? 'Ask about Indian Standards, chemical limits, test methods, or certification...'
                  : 'Ask how to verify genuine ISI mark, gold hallmark, or consumer rights...'
              }
              className="flex-1 bg-transparent px-3 py-2 text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none"
              disabled={loading}
            />

            {/* Microphone Voice Input */}
            <button
              type="button"
              onClick={toggleSpeechRecognition}
              className={`p-2 rounded-xl border transition-all mr-1 ${
                isListening
                  ? 'bg-rose-500 text-white border-rose-600 animate-pulse shadow-md shadow-rose-500/30'
                  : 'text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 border-transparent hover:bg-slate-100 dark:hover:bg-slate-700/60'
              }`}
              title={isListening ? 'Stop Listening' : 'Voice Input (Web Speech API)'}
            >
              {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
            </button>

            {/* Send Button */}
            <button
              type="submit"
              disabled={!inputMessage.trim() || loading}
              className="p-2 rounded-xl bg-blue-600 hover:bg-blue-700 disabled:bg-slate-200 dark:disabled:bg-slate-700 text-white disabled:text-slate-400 transition-all font-semibold shadow-sm"
              title="Send Query"
            >
              <ArrowUp className="w-4 h-4" />
            </button>
          </form>

          <p className="text-[10px] text-center text-slate-400 dark:text-slate-500 mt-2">
            GRASK AI provides official guidance grounded under the Bureau of Indian Standards Act, 2016. Verify real-time CM/L on the official BIS Care Mobile App.
          </p>
        </div>
      </div>
    </div>
  );
};
