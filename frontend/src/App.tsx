import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { ChatInterface } from './components/ChatInterface';
import { ComplianceWorkspace } from './components/ComplianceWorkspace';
import { TelemetryDashboard } from './components/TelemetryDashboard';
import { LicenseVerifyModal } from './components/LicenseVerifyModal';
import { BisServicesModal } from './components/BisServicesModal';
import { NutriScoreModal } from './components/NutriScoreModal';
import { ReadyToApplyModal } from './components/ReadyToApplyModal';
import { CitationModal } from './components/CitationModal';
import { ToastContainer, ToastMessage } from './components/Toast';
import { ErrorBoundary } from './components/ErrorBoundary';
import { ChatMode, ChatMessage, Citation } from './types';

export const App: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState<boolean>(() => {
    if (typeof window !== 'undefined') {
      return window.innerWidth >= 1024;
    }
    return true;
  });
  const [darkMode, setDarkMode] = useState<boolean>(() => {
    const saved = localStorage.getItem('grask_theme');
    if (saved) return saved === 'dark';
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  });
  const [currentMode, setCurrentMode] = useState<ChatMode>('industry');
  const [selectedLanguage, setSelectedLanguage] = useState<string>('en');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [selectedCitation, setSelectedCitation] = useState<Citation | null>(null);
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  // Modals & Overlays for SIH26107 Tools
  const [isLicenseModalOpen, setIsLicenseModalOpen] = useState(false);
  const [isAuditModalOpen, setIsAuditModalOpen] = useState(false);
  const [isTelemetryModalOpen, setIsTelemetryModalOpen] = useState(false);
  const [isBisServiceModalOpen, setIsBisServiceModalOpen] = useState(false);
  const [isNutriModalOpen, setIsNutriModalOpen] = useState(false);
  const [isApplyModalOpen, setIsApplyModalOpen] = useState(false);
  const [applyModalInitialQuery, setApplyModalInitialQuery] = useState('');
  const [bisServiceSection, setBisServiceSection] = useState<
    'standards_clubs' | 'nits_training' | 'lab_recognition' | 'consumer_protection' | 'departments'
  >('standards_clubs');

  // Apply dark mode class to document element
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('grask_theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('grask_theme', 'light');
    }
  }, [darkMode]);

  const addToast = (type: 'success' | 'error' | 'info', message: string) => {
    const newToast: ToastMessage = {
      id: `toast-${Date.now()}-${Math.random()}`,
      type,
      message,
    };
    setToasts((prev) => [...prev, newToast]);
  };

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  const handleNewChat = () => {
    setMessages([]);
    addToast('info', 'Started fresh consultation session.');
  };

  const handleModeChange = (mode: ChatMode) => {
    if (mode !== currentMode) {
      setCurrentMode(mode);
      setMessages([]);
      addToast('info', `Switched to ${mode === 'industry' ? 'Industry & Engineering' : 'Citizen & Consumer'} Mode (Chat Cleared).`);
    }
  };

  const handleOpenLicenseVerify = () => {
    setIsLicenseModalOpen(true);
  };

  const handleOpenComplianceAudit = () => {
    setIsAuditModalOpen(true);
  };

  const handleOpenNutriScore = () => {
    setIsNutriModalOpen(true);
  };

  const handleOpenApplyModal = (query?: string) => {
    setApplyModalInitialQuery(query || '');
    setIsApplyModalOpen(true);
  };

  const handleOpenBisService = (
    section: 'standards_clubs' | 'nits_training' | 'lab_recognition' | 'consumer_protection' | 'departments'
  ) => {
    setBisServiceSection(section);
    setIsBisServiceModalOpen(true);
  };

  const handleOpenTelemetry = () => {
    setIsTelemetryModalOpen(true);
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-50 dark:bg-slate-950 font-sans antialiased">
      {/* ChatGPT-style Left Sidebar */}
      <Sidebar
        isOpen={sidebarOpen}
        onToggle={() => setSidebarOpen(!sidebarOpen)}
        currentMode={currentMode}
        onModeChange={handleModeChange}
        selectedLanguage={selectedLanguage}
        onLanguageChange={setSelectedLanguage}
        darkMode={darkMode}
        onToggleDarkMode={() => setDarkMode(!darkMode)}
        onNewChat={handleNewChat}
        onOpenLicenseVerify={handleOpenLicenseVerify}
        onOpenComplianceAudit={handleOpenComplianceAudit}
        onOpenNutriScore={handleOpenNutriScore}
        onOpenApplyModal={() => handleOpenApplyModal()}
        onOpenBisService={handleOpenBisService}
        onOpenTelemetry={handleOpenTelemetry}
      />

      {/* ChatGPT-style Dedicated Right Workspace */}
      <main className="flex-1 flex flex-col h-full min-w-0 overflow-hidden relative">
        <ErrorBoundary>
          <ChatInterface
            currentMode={currentMode}
            onModeChange={handleModeChange}
            onSelectCitation={setSelectedCitation}
            addToast={addToast}
            onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
            onOpenLicenseVerify={handleOpenLicenseVerify}
            onOpenComplianceAudit={handleOpenComplianceAudit}
            onOpenNutriScore={handleOpenNutriScore}
            onOpenApplyModal={handleOpenApplyModal}
            selectedLanguage={selectedLanguage}
            onLanguageChange={setSelectedLanguage}
            messages={messages}
            setMessages={setMessages}
          />
        </ErrorBoundary>
      </main>

      {/* MANAK-Vision License & HUID Verification Modal */}
      <LicenseVerifyModal
        isOpen={isLicenseModalOpen}
        onClose={() => setIsLicenseModalOpen(false)}
        addToast={addToast}
      />

      {/* FSSAI Nutri-Score & Hidden Ingredient Decrypter Modal */}
      <NutriScoreModal
        isOpen={isNutriModalOpen}
        onClose={() => setIsNutriModalOpen(false)}
        addToast={addToast}
      />

      {/* Ready to Apply Statutory Certificate & Dossier Modal */}
      <ReadyToApplyModal
        isOpen={isApplyModalOpen}
        onClose={() => setIsApplyModalOpen(false)}
        addToast={addToast}
        initialQuery={applyModalInitialQuery}
      />

      {/* Official BIS Services Modal (Standards Clubs, NITS, LRS, Consumer Rights) */}
      <BisServicesModal
        isOpen={isBisServiceModalOpen}
        onClose={() => setIsBisServiceModalOpen(false)}
        defaultSection={bisServiceSection}
      />

      {/* Compliance Audit Studio Modal Overlay */}
      {isAuditModalOpen && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="relative bg-white dark:bg-slate-900 w-full max-w-6xl rounded-3xl shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden flex flex-col max-h-[92vh]">
            <div className="h-1.5 w-full bg-gradient-to-r from-orange-500 via-white to-emerald-600" />
            <div className="p-6 overflow-y-auto">
              <ComplianceWorkspace
                addToast={addToast}
                onClose={() => setIsAuditModalOpen(false)}
              />
            </div>
          </div>
        </div>
      )}

      {/* Government Oversight Telemetry Modal Overlay */}
      {isTelemetryModalOpen && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="relative bg-white dark:bg-slate-900 w-full max-w-5xl rounded-3xl shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden flex flex-col max-h-[92vh]">
            <div className="h-1.5 w-full bg-gradient-to-r from-orange-500 via-white to-emerald-600" />
            <div className="p-6 overflow-y-auto">
              <TelemetryDashboard
                addToast={addToast}
                onClose={() => setIsTelemetryModalOpen(false)}
              />
            </div>
          </div>
        </div>
      )}

      {/* Citation Detail Modal */}
      {selectedCitation && (
        <CitationModal
          citation={selectedCitation}
          onClose={() => setSelectedCitation(null)}
        />
      )}

      {/* Toast Notifications */}
      <ToastContainer toasts={toasts} removeToast={removeToast} />
    </div>
  );
};

export default App;
