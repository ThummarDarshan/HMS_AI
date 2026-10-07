import api from './api';

export interface SourceCitation {
  name: string;
  source_type?: string;
  url: string;
  document_id?: string;
  section?: string;
  last_updated?: string;
}

export interface MedicationCardData {
  name: string;
  generic_name: string;
  brand_names?: string[];
  indications?: string;
  warnings?: string[];
  contraindications?: string[];
  sections?: Record<string, {
    title: string;
    content: string;
    source: string;
    source_url: string;
  }>;
  sources?: SourceCitation[];
}

export interface RedFlagItem {
  category: string;
  matched_term?: string;
  clinical_concern: string;
}

export interface AllergyConflictItem {
  medication: string;
  matched_allergy: string;
  severity: string;
  warning: string;
}

export interface ChatResponse {
  success: boolean;
  session_id: string;
  intent: string;
  answer: string;
  symptoms: string[];
  medications: MedicationCardData[];
  sources: SourceCitation[];
  redFlags: RedFlagItem[];
  allergyConflicts: AllergyConflictItem[];
  doctorReviewRequired: boolean;
  emergency: boolean;
}

export interface ChatMessageRecord {
  id?: number | string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  intent?: string;
  symptoms?: string[];
  medications_data?: MedicationCardData[];
  sources?: SourceCitation[];
  red_flags?: RedFlagItem[];
  allergy_conflicts?: AllergyConflictItem[];
  doctor_review_required?: boolean;
  is_emergency?: boolean;
  created_at?: string;
}

export interface ChatSessionRecord {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  messages?: ChatMessageRecord[];
  last_message?: {
    role: string;
    content: string;
    created_at: string;
  };
}

export const aiAssistantService = {
  async sendMessage(message: string, sessionId?: string): Promise<ChatResponse> {
    const response = await api.post<ChatResponse>('/ai-assistant/chat/', {
      message,
      session_id: sessionId,
    });
    return response.data;
  },

  async getSessions(): Promise<ChatSessionRecord[]> {
    const response = await api.get<ChatSessionRecord[]>('/ai-assistant/sessions/');
    return response.data;
  },

  async getSession(id: string): Promise<ChatSessionRecord> {
    const response = await api.get<ChatSessionRecord>(`/ai-assistant/sessions/${id}/`);
    return response.data;
  },

  async deleteSession(id: string): Promise<void> {
    await api.delete(`/ai-assistant/sessions/${id}/`);
  },

  async searchMedications(query: string) {
    const response = await api.get('/ai-assistant/medications/search/', {
      params: { q: query },
    });
    return response.data;
  },
};
