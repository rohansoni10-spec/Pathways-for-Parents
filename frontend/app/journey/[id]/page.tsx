"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { useParams, useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { STAGES, MILESTONES } from '@/lib/data';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { CheckCircle2, Circle, ChevronDown, ChevronUp, ArrowLeft, Info, HeartHandshake } from 'lucide-react';
import { cn } from '@/lib/utils';
import toast from 'react-hot-toast';

export default function StageDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { user, toggleMilestone } = useAuth();
  const [expandedMilestone, setExpandedMilestone] = useState<string | null>(null);

  const stageId = params.id as string;
  const stage = STAGES.find(s => s.id === stageId);
  const milestones = MILESTONES.filter(m => m.stageId === stageId);

  if (!stage) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-slate-900">Stage not found</h2>
          <Link href="/journey">
            <Button className="mt-4">Back to Journey</Button>
          </Link>
        </div>
      </div>
    );
  }

  const handleToggle = (id: string) => {
    toggleMilestone(id);
    const isNowComplete = !user?.completedMilestones.includes(id);
    if (isNowComplete) {
      toast.success("Milestone completed! Great job.", {
        icon: '👏',
        style: {
          borderRadius: '10px',
          background: '#333',
          color: '#fff',
        },
      });
    }
  };

  const toggleExpand = (id: string) => {
    if (expandedMilestone === id) {
      setExpandedMilestone(null);
    } else {
      setExpandedMilestone(id);
    }
  };

  const completedCount = milestones.filter(m => user?.completedMilestones.includes(m.id)).length;
  const progress = Math.round((completedCount / milestones.length) * 100);

  return (
    <div className="min-h-screen bg-slate-50 pb-20">
      {/* Header */}
      <div className="bg-white border-b border-slate-200 pt-8 pb-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto">
          <Link href="/journey" className="inline-flex items-center text-slate-500 hover:text-slate-800 mb-6 transition-colors">
            <ArrowLeft size={16} className="mr-2" />
            Back to Timeline
          </Link>
          
          <div className="flex items-center gap-3 mb-4">
            <Badge variant="secondary" className={cn("text-sm px-3 py-1", stage.color)}>
              {stage.ageRange}
            </Badge>
            <span className="text-slate-400 text-sm font-medium">Stage {STAGES.findIndex(s => s.id === stage.id) + 1} of 5</span>
          </div>
          
          <h1 className="text-3xl sm:text-4xl font-bold text-slate-900 mb-4">{stage.title}</h1>
          <p className="text-lg text-slate-600 leading-relaxed max-w-2xl">
            {stage.description}
          </p>

          {/* Progress Bar */}
          <div className="mt-8">
            <div className="flex justify-between text-sm font-medium text-slate-600 mb-2">
              <span>Your Progress</span>
              <span>{progress}%</span>
            </div>
            <div className="w-full bg-slate-100 rounded-full h-3 overflow-hidden">
              <div 
                className="bg-emerald-500 h-3 rounded-full transition-all duration-500 ease-out"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      {/* Milestones List */}
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="space-y-6">
          {milestones.map((milestone) => {
            const isCompleted = user?.completedMilestones.includes(milestone.id);
            const isExpanded = expandedMilestone === milestone.id;

            return (
              <Card 
                key={milestone.id} 
                className={cn(
                  "transition-all duration-300 border-l-4 overflow-hidden",
                  isCompleted ? "border-l-emerald-500 bg-emerald-50/30" : "border-l-slate-300 hover:border-l-sky-400"
                )}
              >
                <div className="p-6">
                  <div className="flex items-start gap-4">
                    <button 
                      onClick={() => handleToggle(milestone.id)}
                      className="mt-1 flex-shrink-0 focus:outline-none transition-transform active:scale-95"
                    >
                      {isCompleted ? (
                        <CheckCircle2 className="text-emerald-500 h-6 w-6" />
                      ) : (
                        <Circle className="text-slate-300 h-6 w-6 hover:text-sky-500" />
                      )}
                    </button>
                    
                    <div className="flex-1">
                      <div 
                        className="cursor-pointer"
                        onClick={() => toggleExpand(milestone.id)}
                      >
                        <h3 className={cn(
                          "text-lg font-semibold mb-1 transition-colors",
                          isCompleted ? "text-slate-500 line-through decoration-slate-400" : "text-slate-900"
                        )}>
                          {milestone.title}
                        </h3>
                        <p className="text-slate-600 mb-2">{milestone.behavior}</p>
                        
                        <div className="flex items-center text-sky-600 text-sm font-medium mt-2 hover:text-sky-700">
                          {isExpanded ? (
                            <>Hide details <ChevronUp size={14} className="ml-1" /></>
                          ) : (
                            <>Why this matters <ChevronDown size={14} className="ml-1" /></>
                          )}
                        </div>
                      </div>

                      {/* Expanded Content */}
                      <div className={cn(
                        "grid transition-all duration-300 ease-in-out",
                        isExpanded ? "grid-rows-[1fr] opacity-100 mt-4" : "grid-rows-[0fr] opacity-0"
                      )}>
                        <div className="overflow-hidden">
                          <div className="bg-white rounded-lg border border-slate-100 p-5 space-y-4 shadow-sm">
                            <div>
                              <h4 className="flex items-center text-sm font-bold text-slate-900 uppercase tracking-wide mb-2">
                                <Info size={14} className="mr-2 text-sky-500" />
                                Why it matters
                              </h4>
                              <p className="text-slate-600 text-sm leading-relaxed">
                                {milestone.whyItMatters}
                              </p>
                            </div>
                            
                            <div className="pt-4 border-t border-slate-100">
                              <h4 className="flex items-center text-sm font-bold text-slate-900 uppercase tracking-wide mb-2">
                                <HeartHandshake size={14} className="mr-2 text-rose-500" />
                                If not yet
                              </h4>
                              <p className="text-slate-600 text-sm leading-relaxed">
                                {milestone.ifNotYet}
                              </p>
                            </div>

                            <div className="bg-emerald-50 rounded-md p-3 text-sm text-emerald-800 italic">
                              "{milestone.reassurance}"
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>

        {/* Next Steps */}
        <div className="mt-12 flex justify-between items-center">
          {progress === 100 ? (
            <div className="w-full text-center bg-emerald-100 rounded-xl p-8">
              <h3 className="text-2xl font-bold text-emerald-900 mb-2">Stage Complete! 🎉</h3>
              <p className="text-emerald-700 mb-6">You've taken amazing steps for your child.</p>
              <Link href="/journey">
                <Button className="bg-emerald-600 hover:bg-emerald-700 text-white">
                  Continue Journey
                </Button>
              </Link>
            </div>
          ) : (
            <p className="text-slate-500 text-sm italic">
              Take your time. There is no deadline for these milestones.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
