"use client";

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/auth';
import { STAGES, MILESTONES } from '@/lib/data';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ArrowRight, CheckCircle2, Circle, Star, Eye, Stethoscope, Sprout, School, Heart } from 'lucide-react';
import { cn } from '@/lib/utils';

const ICON_MAP: Record<string, any> = {
  'Eye': Eye,
  'Stethoscope': Stethoscope,
  'Sprout': Sprout,
  'School': School,
  'Heart': Heart
};

export default function JourneyPage() {
  const { user } = useAuth();
  
  // If no user, we might redirect or show empty state. 
  // For now, let's assume user is there or we show a generic view.
  const recommendedStageId = user?.recommendedStageId || 's1';

  const getProgress = (stageId: string) => {
    const stageMilestones = MILESTONES.filter(m => m.stageId === stageId);
    if (stageMilestones.length === 0) return 0;
    
    const completedCount = stageMilestones.filter(m => user?.completedMilestones?.includes(m.id)).length;
    return Math.round((completedCount / stageMilestones.length) * 100);
  };

  return (
    <div className="min-h-screen bg-slate-50 pb-20">
      {/* Header */}
      <div className="bg-white border-b border-slate-200 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-slate-900 mb-2">Your Journey</h1>
          <p className="text-lg text-slate-600">
            A step-by-step roadmap to help you navigate with confidence.
          </p>
        </div>
      </div>

      {/* Timeline */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="space-y-8 relative">
          {/* Vertical Line */}
          <div className="absolute left-8 top-8 bottom-8 w-0.5 bg-slate-200 hidden sm:block"></div>

          {STAGES.map((stage, index) => {
            const Icon = ICON_MAP[stage.icon] || Circle;
            const isRecommended = stage.id === recommendedStageId;
            const progress = getProgress(stage.id);
            const isComplete = progress === 100;

            return (
              <div key={stage.id} className="relative sm:pl-24">
                {/* Timeline Dot */}
                <div className={cn(
                  "absolute left-0 top-6 w-16 h-16 rounded-full border-4 border-white shadow-md flex items-center justify-center z-10 hidden sm:flex",
                  isRecommended ? "bg-sky-500 text-white" : (isComplete ? "bg-emerald-500 text-white" : "bg-white text-slate-400")
                )}>
                  {isComplete ? <CheckCircle2 size={32} /> : <Icon size={32} />}
                </div>

                <Card className={cn(
                  "transition-all duration-300 hover:shadow-md border-l-4",
                  isRecommended ? "border-l-sky-500 ring-2 ring-sky-500/20 shadow-lg" : "border-l-transparent hover:border-l-slate-300"
                )}>
                  <CardHeader className="pb-2">
                    <div className="flex justify-between items-start">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <Badge variant="outline" className={cn("font-normal", stage.color)}>
                            {stage.ageRange}
                          </Badge>
                          {isRecommended && (
                            <Badge className="bg-amber-100 text-amber-800 hover:bg-amber-200 border-0">
                              <Star size={12} className="mr-1 fill-amber-800" /> Recommended Start
                            </Badge>
                          )}
                        </div>
                        <CardTitle className="text-xl sm:text-2xl">{stage.title}</CardTitle>
                      </div>
                      <div className="text-right hidden sm:block">
                        <span className="text-sm font-medium text-slate-500">{progress}% Complete</span>
                      </div>
                    </div>
                  </CardHeader>
                  
                  <CardContent>
                    <CardDescription className="text-base mb-4">
                      {stage.description}
                    </CardDescription>
                    
                    {/* Mobile Progress Bar */}
                    <div className="w-full bg-slate-100 rounded-full h-2 mb-4 sm:hidden">
                      <div 
                        className="bg-emerald-500 h-2 rounded-full transition-all duration-500"
                        style={{ width: `${progress}%` }}
                      ></div>
                    </div>

                    <div className="flex items-center justify-between mt-4">
                      <div className="flex -space-x-2 overflow-hidden">
                        {/* Avatars or indicators could go here */}
                      </div>
                      <Link href={`/journey/${stage.id}`}>
                        <Button variant={isRecommended ? "default" : "outline"} className="gap-2">
                          {isRecommended ? "Start Here" : "View Steps"}
                          <ArrowRight size={16} />
                        </Button>
                      </Link>
                    </div>
                  </CardContent>
                </Card>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
