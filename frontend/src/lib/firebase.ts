import { initializeApp, getApps, getApp } from 'firebase/app';
import { getAnalytics, logEvent, isSupported as isAnalyticsSupported, Analytics } from 'firebase/analytics';
import { getFirestore, collection, addDoc, serverTimestamp, doc, setDoc, Firestore } from 'firebase/firestore';

export const firebaseConfig = {
  apiKey: "AIzaSyB6l6JR_DAMaZdQfRIVv427t6dVm4sZMwc",
  authDomain: "kgupta--kalki-ai.firebaseapp.com",
  projectId: "kgupta--kalki-ai",
  storageBucket: "kgupta--kalki-ai.firebasestorage.app",
  messagingSenderId: "784731367648",
  appId: "1:784731367648:web:0ff1cb879984760b2e8885",
  measurementId: "G-YLNB75RXC9"
};

// Initialize or reuse Firebase App instance
export const app = getApps().length > 0 ? getApp() : initializeApp(firebaseConfig);

let analyticsInstance: Analytics | null = null;
let firestoreInstance: Firestore | null = null;

if (typeof window !== 'undefined') {
  try {
    firestoreInstance = getFirestore(app);
  } catch (e) {
    console.warn('[Firebase] Firestore init notice:', e);
  }

  isAnalyticsSupported().then((supported) => {
    if (supported) {
      analyticsInstance = getAnalytics(app);
    }
  }).catch(() => {});
}

// Generate or retrieve persistent Visitor ID
export function getOrCreateVisitorId(): string {
  if (typeof window === 'undefined') return 'server-side';
  try {
    let vid = localStorage.getItem('kalki_visitor_id');
    if (!vid) {
      vid = 'v-' + Math.random().toString(36).substring(2, 11) + '-' + Date.now().toString(36);
      localStorage.setItem('kalki_visitor_id', vid);
    }
    return vid;
  } catch {
    return 'anon-' + Math.random().toString(36).substring(2, 9);
  }
}

// Generate unique Session ID
let currentSessionId = '';
export function getSessionId(): string {
  if (!currentSessionId) {
    currentSessionId = 'sess-' + Math.random().toString(36).substring(2, 9) + '-' + Date.now().toString(36);
  }
  return currentSessionId;
}

// 1. Record User Arrival / Visit
export async function recordUserVisit(extraMeta: Record<string, any> = {}) {
  if (typeof window === 'undefined') return;
  const visitorId = getOrCreateVisitorId();
  const sessionId = getSessionId();

  const visitData = {
    visitorId,
    sessionId,
    timestamp: new Date().toISOString(),
    url: window.location.href,
    pathname: window.location.pathname,
    referrer: document.referrer || 'direct',
    userAgent: navigator.userAgent,
    language: navigator.language || 'en',
    screenResolution: `${window.screen.width}x${window.screen.height}`,
    viewportSize: `${window.innerWidth}x${window.innerHeight}`,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    createdAt: serverTimestamp(),
    ...extraMeta
  };

  // 1. Log to Google Analytics
  if (analyticsInstance) {
    try {
      logEvent(analyticsInstance, 'page_view', {
        page_location: window.location.href,
        page_title: document.title,
        visitor_id: visitorId,
        session_id: sessionId
      });
    } catch {}
  }

  // 2. Persist in Firestore 'visitors' and 'sessions' collections
  if (firestoreInstance) {
    try {
      // Upsert visitor profile
      const visitorRef = doc(firestoreInstance, 'visitors', visitorId);
      await setDoc(visitorRef, {
        visitorId,
        lastSeen: serverTimestamp(),
        lastUrl: window.location.href,
        userAgent: navigator.userAgent,
        language: navigator.language || 'en'
      }, { merge: true });

      // Append session entry
      await addDoc(collection(firestoreInstance, 'sessions'), visitData);
    } catch (err) {
      console.warn('[Firebase Tracker] Session write note:', err);
    }
  }
}

// 2. Record User Action / Event
export async function recordUserAction(actionName: string, payload: Record<string, any> = {}) {
  if (typeof window === 'undefined') return;
  const visitorId = getOrCreateVisitorId();
  const sessionId = getSessionId();

  const actionData = {
    visitorId,
    sessionId,
    action: actionName,
    payload,
    timestamp: new Date().toISOString(),
    pathname: window.location.pathname,
    createdAt: serverTimestamp()
  };

  // Google Analytics Event
  if (analyticsInstance) {
    try {
      logEvent(analyticsInstance, actionName.replace(/[^a-zA-Z0-9_]/g, '_'), {
        visitor_id: visitorId,
        session_id: sessionId,
        ...payload
      });
    } catch {}
  }

  // Firestore user_actions collection
  if (firestoreInstance) {
    try {
      await addDoc(collection(firestoreInstance, 'user_actions'), actionData);
    } catch (err) {
      console.warn('[Firebase Tracker] Action write note:', err);
    }
  }
}

// 3. Record Agent Execution Log
export async function recordAgentExecution(executionData: {
  prompt: string;
  model: string;
  provider: string;
  status: string;
  latencyMs: number;
  trace?: any;
}) {
  if (typeof window === 'undefined') return;
  const visitorId = getOrCreateVisitorId();
  const sessionId = getSessionId();

  const entry = {
    visitorId,
    sessionId,
    ...executionData,
    timestamp: new Date().toISOString(),
    createdAt: serverTimestamp()
  };

  if (analyticsInstance) {
    try {
      logEvent(analyticsInstance, 'agent_dispatch', {
        model: executionData.model,
        provider: executionData.provider,
        latency_ms: executionData.latencyMs,
        status: executionData.status
      });
    } catch {}
  }

  if (firestoreInstance) {
    try {
      await addDoc(collection(firestoreInstance, 'agent_executions'), entry);
    } catch (err) {
      console.warn('[Firebase Tracker] Execution write note:', err);
    }
  }
}
