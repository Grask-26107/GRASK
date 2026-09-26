import React from 'react';
import {
  Plus,
  MessageSquare,
  ShieldCheck,
  Award,
  GraduationCap,
  FlaskConical,
  Scale,
  Layers,
  BarChart3,
  Sun,
  Moon,
  Globe,
  CheckCircle2,
  FileCheck2,
  Sparkles,
  ChevronLeft,
  ChevronRight,
  ExternalLink,
  Search
} from 'lucide-react';
import { ChatMode } from '../types';
import { SUPPORTED_LANGUAGES } from '../constants/languages';

interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
  currentMode: ChatMode;
  onModeChange: (mode: ChatMode) => void;
  selectedLanguage: string;
  onLanguageChange: (lang: string) => void;
  darkMode: boolean;
  onToggleDarkMode: () => void;
  onNewChat: () => void;
  onOpenLicenseVerify: () => void;
  onOpenComplianceAudit: () => void;
  onOpenNutriScore?: () => void;
  onOpenApplyModal?: () => void;
  onOpenBisService: (section: 'standards_clubs' | 'nits_training' | 'lab_recognition' | 'consumer_protection' | 'departments') => void;
  onOpenTelemetry: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  isOpen,
  onToggle,
  currentMode,
  onModeChange,
  selectedLanguage,
  onLanguageChange,
  darkMode,
  onToggleDarkMode,
  onNewChat,
  onOpenLicenseVerify,
  onOpenComplianceAudit,
  onOpenNutriScore,
  onOpenApplyModal,
  onOpenBisService,
  onOpenTelemetry,
}) => {
  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-slate-900/60 backdrop-blur-sm lg:hidden"
          onClick={onToggle}
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={`fixed lg:static top-0 left-0 z-40 h-full flex flex-col bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 border-slate-200 dark:border-slate-800 transition-all duration-300 ease-in-out shrink-0 select-none overflow-hidden ${
          isOpen
            ? 'w-72 translate-x-0 border-r opacity-100 pointer-events-auto'
            : 'w-0 -translate-x-full lg:w-0 border-r-0 opacity-0 pointer-events-none'
        }`}
      >
        <div className="w-72 h-full flex flex-col shrink-0">
          {/* National Tricolor Top Accent */}
          <div className="h-1 w-full flex shrink-0 shadow-sm">
            <div className="w-1/3 bg-[#FF9933]"></div>
            <div className="w-1/3 bg-[#FFFFFF]"></div>
            <div className="w-1/3 bg-[#138808]"></div>
          </div>

          {/* Brand Header */}
          <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
            <div className="flex items-center space-x-2.5">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-900 border border-amber-400/40 flex items-center justify-center text-white shadow-md p-1 shrink-0">
                <img src="/bis-emblem.svg" alt="Emblem" className="w-6 h-6 drop-shadow" />
              </div>
              <div className="leading-tight">
                <div className="flex items-center space-x-1.5">
                  <span className="font-extrabold text-base tracking-tight text-slate-900 dark:text-white">GRASK AI</span>
                  <span className="px-1.5 py-0.5 rounded text-[9px] font-bold bg-amber-400/20 text-amber-600 dark:text-amber-300 border border-amber-400/40">
                    SIH26107
                  </span>
                </div>
                <p className="text-[10px] text-slate-500 dark:text-slate-400 font-medium">Bureau of Indian Standards</p>
              </div>
            </div>

            <button
              type="button"
              onClick={onToggle}
              className="p-1.5 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              title="Collapse Sidebar"
              aria-label="Collapse Sidebar"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
          </div>

        {/* New Chat Action Button */}
        <div className="p-3">
          <button
            type="button"
            onClick={onNewChat}
            className="w-full py-2.5 px-3 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold flex items-center justify-center space-x-2 shadow-sm transition-all hover:shadow-blue-500/20 active:scale-[0.99]"
          >
            <Plus className="w-4 h-4" />
            <span>New Consultation</span>
          </button>
        </div>

        {/* Persona Mode Toggle (Industry vs Consumer) */}
        <div className="px-3 pb-3">
          <div className="bg-slate-100 dark:bg-slate-800/80 p-1 rounded-xl border border-slate-200 dark:border-slate-700/60 flex text-xs">
            <button
              type="button"
              onClick={() => onModeChange('industry')}
              className={`flex-1 py-1.5 rounded-lg font-semibold flex items-center justify-center space-x-1 transition-all ${
                currentMode === 'industry'
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
              }`}
            >
              <span>🏭 Industry</span>
            </button>
            <button
              type="button"
              onClick={() => onModeChange('consumer')}
              className={`flex-1 py-1.5 rounded-lg font-semibold flex items-center justify-center space-x-1 transition-all ${
                currentMode === 'consumer'
                  ? 'bg-emerald-600 text-white shadow-sm'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
              }`}
            >
              <span>👥 Citizen</span>
            </button>
          </div>
          <p className="text-[10px] text-slate-500 dark:text-slate-400 px-1 pt-1.5 leading-tight">
            {currentMode === 'industry'
              ? 'Technical clauses, NABL test methods & tolerances.'
              : 'Plain-language safety, ISI & Gold Hallmark checks.'}
          </p>
        </div>

        {/* Scrollable Navigation & BIS Services Hub */}
        <div className="flex-1 overflow-y-auto px-3 space-y-4 text-xs">
          {/* SIH Mandated Core Tools */}
          <div>
            <span className="px-2 text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider block mb-1.5">
              Verified BIS Services (SIH26107)
            </span>
            <div className="space-y-1">
              <button
                type="button"
                onClick={onOpenLicenseVerify}
                className="w-full text-left px-2.5 py-2 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800/80 hover:text-slate-900 dark:hover:text-white flex items-center space-x-2.5 transition-colors group"
              >
                <div className="w-6 h-6 rounded-lg bg-amber-500/10 text-amber-500 dark:text-amber-400 flex items-center justify-center shrink-0 group-hover:bg-amber-500 group-hover:text-white dark:group-hover:text-slate-900 transition-colors">
                  <Search className="w-3.5 h-3.5" />
                </div>
                <div className="flex-1 truncate">
                  <span className="font-semibold block truncate">Verify License / HUID</span>
                  <span className="text-[10px] text-slate-500 dark:text-slate-400 block truncate">MANAK-Vision Mark Scanner</span>
                </div>
              </button>

              <button
                type="button"
                onClick={onOpenComplianceAudit}
                className="w-full text-left px-2.5 py-2 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800/80 hover:text-slate-900 dark:hover:text-white flex items-center space-x-2.5 transition-colors group"
              >
                <div className="w-6 h-6 rounded-lg bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center shrink-0 group-hover:bg-emerald-500 group-hover:text-white dark:group-hover:text-slate-900 transition-colors">
                  <FileCheck2 className="w-3.5 h-3.5" />
                </div>
                <div className="flex-1 truncate">
                  <span className="font-semibold block truncate">Compliance Audit Studio</span>
                  <span className="text-[10px] text-slate-500 dark:text-slate-400 block truncate">Tolerances & Official PDF</span>
                </div>
              </button>

              {onOpenNutriScore && (
                <button
                  type="button"
                  onClick={onOpenNutriScore}
                  className="w-full text-left px-2.5 py-2 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800/80 hover:text-slate-900 dark:hover:text-white flex items-center space-x-2.5 transition-colors group"
                >
                  <div className="w-6 h-6 rounded-lg bg-teal-500/10 text-teal-600 dark:text-teal-400 flex items-center justify-center shrink-0 group-hover:bg-teal-500 group-hover:text-white dark:group-hover:text-slate-900 transition-colors">
                    <span className="text-xs">🥗</span>
                  </div>
                  <div className="flex-1 truncate">
                    <div className="flex items-center space-x-1.5">
                      <span className="font-semibold block truncate">Nutri-Score & Ingredients</span>
                      <span className="px-1 py-0.2 rounded text-[8px] font-bold bg-teal-500/20 text-teal-600 dark:text-teal-400">
                        FSSAI
                      </span>
                    </div>
                    <span className="text-[10px] text-slate-500 dark:text-slate-400 block truncate">Harmful vs Secure Decrypter</span>
                  </div>
                </button>
              )}

              {onOpenApplyModal && (
                <button
                  type="button"
                  onClick={onOpenApplyModal}
                  className="w-full text-left px-2.5 py-2 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800/80 hover:text-slate-900 dark:hover:text-white flex items-center space-x-2.5 transition-colors group"
                >
                  <div className="w-6 h-6 rounded-lg bg-amber-500/10 text-amber-600 dark:text-amber-400 flex items-center justify-center shrink-0 group-hover:bg-amber-500 group-hover:text-white dark:group-hover:text-slate-900 transition-colors">
                    <Award className="w-3.5 h-3.5" />
                  </div>
                  <div className="flex-1 truncate">
                    <div className="flex items-center space-x-1.5">
                      <span className="font-semibold block truncate">Ready to Apply</span>
                      <span className="px-1 py-0.2 rounded text-[8px] font-bold bg-amber-500/20 text-amber-600 dark:text-amber-400">
                        50% MSME
                      </span>
                    </div>
                    <span className="text-[10px] text-slate-500 dark:text-slate-400 block truncate">Certificate & Dossier Studio</span>
                  </div>
                </button>
              )}
            </div>
          </div>

          {/* Educational & Professional Initiatives */}
          <div>
            <span className="px-2 text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider block mb-1.5">
              BIS Initiatives & Training
            </span>
            <div className="space-y-1">
              <button
                type="button"
                onClick={() => onOpenBisService('standards_clubs')}
                className="w-full text-left px-2.5 py-2 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800/80 hover:text-slate-900 dark:hover:text-white flex items-center space-x-2.5 transition-colors group"
              >
                <div className="w-6 h-6 rounded-lg bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center shrink-0 group-hover:bg-blue-500 group-hover:text-white dark:group-hover:text-slate-900 transition-colors">
                  <GraduationCap className="w-3.5 h-3.5" />
                </div>
                <div className="flex-1 truncate">
                  <span className="font-semibold block truncate">Standards Clubs</span>
                  <span className="text-[10px] text-slate-500 dark:text-slate-400 block truncate">Schools & Colleges (Grants)</span>
                </div>
              </button>

              <button
                type="button"
                onClick={() => onOpenBisService('nits_training')}
                className="w-full text-left px-2.5 py-2 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800/80 hover:text-slate-900 dark:hover:text-white flex items-center space-x-2.5 transition-colors group"
              >
                <div className="w-6 h-6 rounded-lg bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 flex items-center justify-center shrink-0 group-hover:bg-indigo-500 group-hover:text-white dark:group-hover:text-slate-900 transition-colors">
                  <Award className="w-3.5 h-3.5" />
                </div>
                <div className="flex-1 truncate">
                  <span className="font-semibold block truncate">NITS Training Programs</span>
                  <span className="text-[10px] text-slate-500 dark:text-slate-400 block truncate">Lead Auditor & QMS Courses</span>
                </div>
              </button>

              <button
                type="button"
                onClick={() => onOpenBisService('lab_recognition')}
                className="w-full text-left px-2.5 py-2 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800/80 hover:text-slate-900 dark:hover:text-white flex items-center space-x-2.5 transition-colors group"
              >
                <div className="w-6 h-6 rounded-lg bg-teal-500/10 text-teal-600 dark:text-teal-400 flex items-center justify-center shrink-0 group-hover:bg-teal-500 group-hover:text-white dark:group-hover:text-slate-900 transition-colors">
                  <FlaskConical className="w-3.5 h-3.5" />
                </div>
                <div className="flex-1 truncate">
                  <span className="font-semibold block truncate">Laboratory Recognition (LRS)</span>
                  <span className="text-[10px] text-slate-500 dark:text-slate-400 block truncate">NABL & ISO/IEC 17025 Labs</span>
                </div>
              </button>

              <button
                type="button"
                onClick={() => onOpenBisService('consumer_protection')}
                className="w-full text-left px-2.5 py-2 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800/80 hover:text-slate-900 dark:hover:text-white flex items-center space-x-2.5 transition-colors group"
              >
                <div className="w-6 h-6 rounded-lg bg-rose-500/10 text-rose-600 dark:text-rose-400 flex items-center justify-center shrink-0 group-hover:bg-rose-500 group-hover:text-white dark:group-hover:text-slate-900 transition-colors">
                  <Scale className="w-3.5 h-3.5" />
                </div>
                <div className="flex-1 truncate">
                  <span className="font-semibold block truncate">Consumer Rights & Grievance</span>
                  <span className="text-[10px] text-slate-500 dark:text-slate-400 block truncate">BIS Care & NCH 1915</span>
                </div>
              </button>

              <button
                type="button"
                onClick={() => onOpenBisService('departments')}
                className="w-full text-left px-2.5 py-2 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800/80 hover:text-slate-900 dark:hover:text-white flex items-center space-x-2.5 transition-colors group"
              >
                <div className="w-6 h-6 rounded-lg bg-purple-500/10 text-purple-600 dark:text-purple-400 flex items-center justify-center shrink-0 group-hover:bg-purple-500 group-hover:text-white dark:group-hover:text-slate-900 transition-colors">
                  <Layers className="w-3.5 h-3.5" />
                </div>
                <div className="flex-1 truncate">
                  <span className="font-semibold block truncate">17 Technical Departments</span>
                  <span className="text-[10px] text-slate-500 dark:text-slate-400 block truncate">24,084 Active Standards</span>
                </div>
              </button>
            </div>
          </div>

          {/* Telemetry / Governance */}
          <div>
            <span className="px-2 text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider block mb-1.5">
              Government Governance
            </span>
            <button
              type="button"
              onClick={onOpenTelemetry}
              className="w-full text-left px-2.5 py-2 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800/80 hover:text-slate-900 dark:hover:text-white flex items-center space-x-2.5 transition-colors group"
            >
              <div className="w-6 h-6 rounded-lg bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 flex items-center justify-center shrink-0 group-hover:bg-cyan-500 group-hover:text-white dark:group-hover:text-slate-900 transition-colors">
                <BarChart3 className="w-3.5 h-3.5" />
              </div>
              <div className="flex-1 truncate">
                <span className="font-semibold block truncate">Oversight Telemetry</span>
                <span className="text-[10px] text-slate-500 dark:text-slate-400 block truncate">Live Conformance Ratios</span>
              </div>
            </button>
          </div>
        </div>

        {/* Footer Area: Theme & Security Shield */}
        <div className="p-3 border-t border-slate-200 dark:border-slate-800 space-y-2.5 bg-slate-50/80 dark:bg-slate-950/60">

          {/* Theme & Privacy Status */}
          <div className="flex items-center justify-between px-1 text-[11px] text-slate-500 dark:text-slate-400">
            <div className="flex items-center space-x-1 text-emerald-600 dark:text-emerald-400">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span className="font-semibold">BIS Act Grounded</span>
            </div>

            <button
              type="button"
              onClick={onToggleDarkMode}
              className="p-1.5 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors"
              title={darkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
            >
              {darkMode ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-slate-600" />}
            </button>
          </div>
        </div>
      </div>
    </aside>
    </>
  );
};
