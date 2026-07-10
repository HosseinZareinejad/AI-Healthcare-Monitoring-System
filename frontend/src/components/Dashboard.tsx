import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Activity, Brain, User, AlertTriangle } from 'lucide-react';

interface GlucoseRecord {
  id: number;
  patient_id: number;
  timestamp: string;
  glucose_level: number;
  meal_status: string;
}

interface Patient {
  id: number;
  name: string;
  age: number;
  diabetes_type: string;
}

export default function Dashboard() {
  const [records, setRecords] = useState<GlucoseRecord[]>([]);
  const [patient, setPatient] = useState<Patient | null>(null);
  const [aiReport, setAiReport] = useState<string | null>(null);
  const [loadingAi, setLoadingAi] = useState(false);

  useEffect(() => {
    // Fetch patient info
    axios.get('/api/patients/1').then(res => setPatient(res.data)).catch(console.error);
    // Fetch history
    axios.get('/api/patients/1/history').then(res => setRecords(res.data)).catch(console.error);
  }, []);

  const handleAnalyze = async () => {
    setLoadingAi(true);
    try {
      const res = await axios.post('/api/patients/1/analyze');
      setAiReport(res.data.analysis_report);
    } catch (err) {
      console.error(err);
      setAiReport("Failed to generate AI report.");
    }
    setLoadingAi(false);
  };

  const latestRecord = records.length > 0 ? records[records.length - 1] : null;
  const isHigh = latestRecord && latestRecord.glucose_level > 180;

  // Format data for chart
  const chartData = records.map(r => ({
    time: new Date(r.timestamp).toLocaleDateString() + ' ' + new Date(r.timestamp).getHours() + ':00',
    glucose: r.glucose_level
  })).slice(-14); // Last 14 readings

  return (
    <div className="min-h-screen p-8 max-w-7xl mx-auto space-y-8">
      {/* Header */}
      <header className="flex justify-between items-center bg-surface p-6 rounded-2xl shadow-lg border border-surface-hover backdrop-blur-md">
        <div className="flex items-center gap-4">
          <div className="p-3 bg-primary/20 rounded-full text-primary">
            <User size={28} />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-text">{patient ? patient.name : 'Loading...'}</h1>
            <p className="text-muted">{patient ? `${patient.age} yrs • ${patient.diabetes_type}` : 'Patient Profile'}</p>
          </div>
        </div>
        <div className="text-right">
          <p className="text-sm text-muted">System Status</p>
          <div className="flex items-center gap-2 text-success font-medium">
            <span className="w-2 h-2 rounded-full bg-success animate-pulse"></span>
            Live Monitoring Active
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Main Column */}
        <div className="lg:col-span-2 space-y-8">
          
          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className={`p-6 rounded-2xl shadow-lg border ${isHigh ? 'bg-danger/10 border-danger/30' : 'bg-surface border-surface-hover'}`}>
              <div className="flex justify-between items-start">
                <div>
                  <p className="text-muted mb-1">Latest Glucose</p>
                  <h2 className={`text-4xl font-bold ${isHigh ? 'text-danger' : 'text-primary'}`}>
                    {latestRecord ? latestRecord.glucose_level : '--'} <span className="text-lg font-normal text-muted">mg/dL</span>
                  </h2>
                </div>
                <div className={`p-3 rounded-full ${isHigh ? 'bg-danger/20 text-danger' : 'bg-primary/20 text-primary'}`}>
                  {isHigh ? <AlertTriangle size={24} /> : <Activity size={24} />}
                </div>
              </div>
              <p className={`mt-4 text-sm ${isHigh ? 'text-danger' : 'text-muted'}`}>
                {latestRecord ? `Status: ${latestRecord.meal_status}` : 'Waiting for data...'}
              </p>
            </div>
          </div>

          {/* Chart */}
          <div className="bg-surface p-6 rounded-2xl shadow-lg border border-surface-hover">
            <h3 className="text-xl font-semibold mb-6 flex items-center gap-2">
              <Activity className="text-secondary" /> Glucose Trends
            </h3>
            <div className="h-72 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                  <XAxis dataKey="time" stroke="#94a3b8" fontSize={12} tickMargin={10} />
                  <YAxis stroke="#94a3b8" fontSize={12} domain={['dataMin - 20', 'dataMax + 20']} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                    itemStyle={{ color: '#38bdf8' }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="glucose" 
                    stroke="#38bdf8" 
                    strokeWidth={3}
                    dot={{ fill: '#0f172a', stroke: '#38bdf8', strokeWidth: 2, r: 4 }}
                    activeDot={{ r: 6, fill: '#38bdf8' }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* AI Column */}
        <div className="bg-surface p-6 rounded-2xl shadow-lg border border-surface-hover flex flex-col">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl font-semibold flex items-center gap-2">
              <Brain className="text-secondary" /> AI Analyst
            </h3>
            <button 
              onClick={handleAnalyze}
              disabled={loadingAi}
              className="px-4 py-2 bg-secondary text-white rounded-lg font-medium hover:bg-secondary/80 transition-colors disabled:opacity-50 flex items-center gap-2"
            >
              {loadingAi ? 'Analyzing...' : 'Generate Report'}
            </button>
          </div>
          
          <div className="flex-1 bg-background rounded-xl p-4 overflow-y-auto border border-surface-hover">
            {loadingAi ? (
              <div className="h-full flex flex-col items-center justify-center text-muted space-y-4">
                <Brain className="animate-pulse text-secondary" size={48} />
                <p>CrewAI is analyzing your data...</p>
              </div>
            ) : aiReport ? (
              <div className="prose prose-invert prose-sm max-w-none">
                {aiReport.split('\n').map((line, i) => (
                  <p key={i} className="mb-2">{line}</p>
                ))}
              </div>
            ) : (
              <div className="h-full flex items-center justify-center text-muted text-center">
                Click "Generate Report" to get a comprehensive medical assessment powered by Llama 3.
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
