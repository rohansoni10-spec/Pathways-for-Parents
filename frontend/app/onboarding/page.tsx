"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowRight, Check } from 'lucide-react';
import { cn } from '@/lib/utils';

const QUESTIONS = [
  {
    id: 'age',
    title: "How old is your child?",
    options: [
      { value: '0-18m', label: '0 - 18 months' },
      { value: '18-36m', label: '18 - 36 months' },
      { value: '3-5y', label: '3 - 5 years' },
      { value: '5-8y', label: '5 - 8 years' }
    ]
  },
  {
    id: 'diagnosis',
    title: "What is your child's diagnosis status?",
    options: [
      { value: 'none', label: 'Not diagnosed / Just concerned' },
      { value: 'waiting', label: 'Referred / Waiting for evaluation' },
      { value: 'recent', label: 'Diagnosed within last 12 months' },
      { value: 'established', label: 'Diagnosed over 12 months ago' }
    ]
  },
  {
    id: 'concern',
    title: "What is your primary concern right now?",
    options: [
      { value: 'speech', label: 'Speech & Communication' },
      { value: 'behavior', label: 'Behavior & Meltdowns' },
      { value: 'school', label: 'School Readiness & IEPs' },
      { value: 'services', label: 'Navigating Services & Insurance' }
    ]
  }
];

export default function OnboardingPage() {
  const router = useRouter();
  const { updateUser, user, register } = useAuth();
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSelect = (value: string) => {
    setAnswers(prev => ({ ...prev, [QUESTIONS[step].id]: value }));
  };

  const handleNext = () => {
    if (step < QUESTIONS.length - 1) {
      setStep(step + 1);
    } else {
      handleSubmit();
    }
  };

  const calculateRecommendedStage = (answers: Record<string, string>) => {
    const { diagnosis, age, concern } = answers;
    
    // Base logic
    let stageId = 's1';
    
    if (diagnosis === 'none') stageId = 's1';
    else if (diagnosis === 'waiting') stageId = 's2';
    else if (diagnosis === 'recent') stageId = 's3';
    else if (diagnosis === 'established') stageId = 's4';

    // Age guardrails
    if (age === '0-18m' && (stageId === 's2' || stageId === 's3' || stageId === 's4')) stageId = 's1'; // Keep very young ones in early signs/early intervention context usually, but PRD says max S1
    // Actually PRD says: 0-18m -> Max S1. 
    if (age === '0-18m') stageId = 's1';
    
    if (age === '18-36m' && (stageId === 's3' || stageId === 's4')) {
       // If diagnosed recently but under 3, S3 is actually perfect (Early Intervention). 
       // PRD says Max S2 for 18-36m? That seems low if they are already diagnosed.
       // Let's follow PRD: "18-36 months → Max stage S2". 
       // Wait, if they are diagnosed, they need EI (S3). 
       // Let's look at PRD again: "Diagnosed within last 12 months → S3".
       // "18-36 months → Max stage S2". This conflict implies if they are 2.5 and diagnosed, we show them S2 (Diagnosis)? 
       // Maybe the logic is strict. I will stick to the PRD logic but maybe relax it if they are explicitly diagnosed.
       // Actually, let's trust the "Diagnosis Status" as primary driver as per PRD, but apply guardrails.
       // If diagnosis is 'recent' (S3) but age is 18-36m (Max S2), we downgrade to S2.
       // This might be because S2 contains "Understand the Report" which is crucial even if diagnosed.
       if (stageId === 's3' || stageId === 's4') stageId = 's2';
    }

    // Concern overrides
    if (concern === 'school' && (age === '5-8y' || age === '3-5y')) stageId = 's4';
    if (concern === 'speech' && age === '0-18m') stageId = 's1';

    return stageId;
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    const recommendedStageId = calculateRecommendedStage(answers);
    
    // If user is not logged in, we might want to register them or just store in local state temporarily
    // For this flow, let's assume we register them anonymously or just update if they exist
    if (!user) {
      // Create a temporary user or ask for email. 
      // For MVP flow simplicity, let's just register a temp user
      register(`guest_${Date.now()}@example.com`, 'Guest Parent');
    }
    
    // We need to wait a bit for the register to propagate in the context if it was async, 
    // but our mock is synchronous-ish.
    
    // Update user with recommendation
    updateUser({ recommendedStageId });
    
    // Simulate processing
    setTimeout(() => {
      router.push('/journey');
    }, 1000);
  };

  const currentQuestion = QUESTIONS[step];

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-lg">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-slate-900 mb-2">Let's find your starting point</h1>
          <p className="text-slate-600">Answer 3 quick questions to get a personalized roadmap.</p>
        </div>

        <Card className="border-0 shadow-xl shadow-slate-200/60 overflow-hidden">
          <div className="h-2 bg-slate-100 w-full">
            <div 
              className="h-full bg-sky-500 transition-all duration-500 ease-out"
              style={{ width: `${((step + 1) / QUESTIONS.length) * 100}%` }}
            ></div>
          </div>
          
          <CardHeader>
            <CardTitle className="text-xl">{currentQuestion.title}</CardTitle>
          </CardHeader>
          
          <CardContent className="space-y-3">
            {currentQuestion.options.map((option) => (
              <div 
                key={option.value}
                onClick={() => handleSelect(option.value)}
                className={cn(
                  "p-4 rounded-lg border-2 cursor-pointer transition-all duration-200 flex items-center justify-between group",
                  answers[currentQuestion.id] === option.value
                    ? "border-sky-500 bg-sky-50"
                    : "border-slate-100 hover:border-sky-200 hover:bg-slate-50"
                )}
              >
                <span className={cn(
                  "font-medium",
                  answers[currentQuestion.id] === option.value ? "text-sky-900" : "text-slate-700"
                )}>
                  {option.label}
                </span>
                {answers[currentQuestion.id] === option.value && (
                  <div className="h-6 w-6 bg-sky-500 rounded-full flex items-center justify-center">
                    <Check size={14} className="text-white" />
                  </div>
                )}
              </div>
            ))}
          </CardContent>
          
          <CardFooter className="flex justify-between pt-2">
            <Button 
              variant="ghost" 
              onClick={() => setStep(Math.max(0, step - 1))}
              disabled={step === 0}
            >
              Back
            </Button>
            <Button 
              onClick={handleNext}
              disabled={!answers[currentQuestion.id] || isSubmitting}
              className="bg-sky-600 hover:bg-sky-700"
            >
              {step === QUESTIONS.length - 1 ? (isSubmitting ? 'Creating Roadmap...' : 'See My Roadmap') : 'Next'}
              {!isSubmitting && <ArrowRight size={16} className="ml-2" />}
            </Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}
