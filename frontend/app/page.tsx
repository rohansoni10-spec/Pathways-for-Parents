"use client";

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { MILESTONES } from '@/lib/data';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowRight, CheckCircle2, ShieldCheck, Heart, Users, Loader2, Circle } from 'lucide-react';
import { cn } from '@/lib/utils';
import toast from 'react-hot-toast';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://pathways-backend-9lei.onrender.com/api/v1';

interface Stage {
  id: string;
  title: string;
  description: string;
  ageRange: string;
  color: string;
  icon: string;
  order: number;
  nextStepPrompt?: string;
}

interface Progress {
  completed_milestone_ids: string[];
  stage_progress: Record<string, {
    total_milestones: number;
    completed_milestones: number;
    percentage: number;
  }>;
  total_completed: number;
  total_milestones: number;
  // Legacy fields for backward compatibility
  completedMilestones?: string[];
  progressByStage?: Record<string, number>;
}

export default function LandingPage() {
  const { user, logout } = useAuth();
  const router = useRouter();
  const [stages, setStages] = useState<Stage[]>([]);
  const [progress, setProgress] = useState<Progress | null>(null);
  const [loading, setLoading] = useState(false);
  const [recommendedStage, setRecommendedStage] = useState<Stage | null>(null);

  useEffect(() => {
    fetchRoadmapData();
  }, [user]);

  const fetchRoadmapData = async () => {
    setLoading(true);
    try {
      // Fetch stages
      const stagesRes = await fetch(`${API_BASE_URL}/stages`);
      if (stagesRes.ok) {
        const stagesData = await stagesRes.json();
        setStages(stagesData);
        console.log('Stages fetched:', stagesData);
        
        // Find recommended stage - check both user object and stages data
        if (user?.recommendedStageId) {
          const recommended = stagesData.find((s: Stage) => s.id === user.recommendedStageId);
          console.log('User recommendedStageId:', user.recommendedStageId);
          console.log('Recommended stage found:', recommended);
          setRecommendedStage(recommended || null);
        } else {
          console.log('No user or no recommendedStageId');
          setRecommendedStage(null);
        }
      }

      // Fetch progress if user is authenticated
      if (user) {
        const token = localStorage.getItem('pathways_token');
        if (token) {
          const progressRes = await fetch(`${API_BASE_URL}/progress`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          if (progressRes.ok) {
            const progressData = await progressRes.json();
            console.log('Progress data fetched:', progressData);
            // Transform backend response to match our interface
            const transformedProgress: Progress = {
              completed_milestone_ids: progressData.completed_milestone_ids || [],
              stage_progress: progressData.stage_progress || {},
              total_completed: progressData.total_completed || 0,
              total_milestones: progressData.total_milestones || 0,
              // Legacy format for backward compatibility
              completedMilestones: progressData.completed_milestone_ids || [],
              progressByStage: Object.entries(progressData.stage_progress || {}).reduce((acc, [key, value]: [string, any]) => {
                acc[key] = value.percentage || 0;
                return acc;
              }, {} as Record<string, number>)
            };
            console.log('Transformed progress:', transformedProgress);
            setProgress(transformedProgress);
          }
        }
      } else {
        setProgress(null);
      }
    } catch (error) {
      console.error('Error fetching roadmap data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    toast.success('Logged out successfully');
  };

  const handleStartJourney = () => {
    // Check if user is authenticated
    if (user) {
      // Check if user has an existing journey started
      // A journey is considered "started" if they have completed onboarding (has recommendedStageId)
      const hasStartedJourney = user.recommendedStageId !== undefined && user.recommendedStageId !== null;
      
      if (hasStartedJourney) {
        // User has an existing journey (completed onboarding) - take them to journey page
        router.push('/journey');
      } else {
        // User hasn't completed onboarding yet - take them to onboarding flow
        router.push('/onboarding');
      }
    } else {
      // New user - take them to registration
      router.push('/register');
    }
  };

  const getStageColorClasses = (color: string) => {
    const colorMap: Record<string, string> = {
      'bg-amber-100 text-amber-800': 'bg-amber-50 border-amber-200 hover:bg-amber-100',
      'bg-purple-100 text-purple-800': 'bg-purple-50 border-purple-200 hover:bg-purple-100',
      'bg-emerald-100 text-emerald-800': 'bg-emerald-50 border-emerald-200 hover:bg-emerald-100',
      'bg-blue-100 text-blue-800': 'bg-blue-50 border-blue-200 hover:bg-blue-100',
      'bg-rose-100 text-rose-800': 'bg-rose-50 border-rose-200 hover:bg-rose-100',
    };
    return colorMap[color] || 'bg-accent/50 border-border hover:bg-accent';
  };

  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="relative bg-hero-gradient pt-20 pb-32 overflow-hidden">
        <div className="absolute top-0 right-0 -mr-20 -mt-20 w-96 h-96 bg-primary/20 rounded-full blur-3xl opacity-50"></div>
        <div className="absolute bottom-0 left-0 -ml-20 -mb-20 w-96 h-96 bg-secondary/20 rounded-full blur-3xl opacity-50"></div>
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="text-center max-w-3xl mx-auto">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-card border border-border shadow-sm mb-8">
              <span className="flex h-2 w-2 rounded-full bg-secondary mr-2"></span>
              <span className="text-sm font-medium text-muted-foreground">A guided roadmap for parents</span>
            </div>
            <h1 className="text-5xl md:text-6xl font-bold text-foreground tracking-tight mb-6 leading-tight">
              Navigate the autism journey with <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary">confidence</span>.
            </h1>
            <p className="text-xl text-muted-foreground mb-10 leading-relaxed">
              Stop drowning in information. Get a personalized, step-by-step roadmap that shows you exactly what matters right now for your child.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button
                size="lg"
                className="w-full sm:w-auto text-lg px-8 py-6 bg-primary hover:bg-primary/90 text-primary-foreground shadow-lg shadow-primary/20"
                onClick={handleStartJourney}
              >
                {user ? (user.recommendedStageId ? 'View My Journey' : 'Complete Setup') : 'Start My Journey'}
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              <Link href="/resources">
                <Button variant="outline" size="lg" className="w-full sm:w-auto text-lg px-8 py-6 bg-card/80 backdrop-blur-sm">
                  Browse Resources
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-card">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-foreground mb-4">Why parents trust Pathways for Parents</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              We turn a complex, overwhelming process into manageable steps.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-accent/50 rounded-2xl p-8 border border-border hover:shadow-lg transition-shadow">
              <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center mb-6">
                <ShieldCheck className="text-primary h-6 w-6" />
              </div>
              <h3 className="text-xl font-bold text-foreground mb-3">Trustworthy Guidance</h3>
              <p className="text-muted-foreground">
                Curated by experts and experienced parents. No jargon, no fear-mongering—just clear, actionable advice.
              </p>
            </div>
            <div className="bg-accent/50 rounded-2xl p-8 border border-border hover:shadow-lg transition-shadow">
              <div className="w-12 h-12 bg-secondary/10 rounded-xl flex items-center justify-center mb-6">
                <CheckCircle2 className="text-secondary h-6 w-6" />
              </div>
              <h3 className="text-xl font-bold text-foreground mb-3">Actionable Milestones</h3>
              <p className="text-muted-foreground">
                Break down big goals into small, achievable wins. Track your progress and celebrate every step forward.
              </p>
            </div>
            <div className="bg-accent/50 rounded-2xl p-8 border border-border hover:shadow-lg transition-shadow">
              <div className="w-12 h-12 bg-destructive/10 rounded-xl flex items-center justify-center mb-6">
                <Heart className="text-destructive h-6 w-6" />
              </div>
              <h3 className="text-xl font-bold text-foreground mb-3">Emotional Support</h3>
              <p className="text-muted-foreground">
                We focus on you as much as your child. Find reassurance, community resources, and self-care reminders.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How it Works */}
      <section className="py-24 bg-accent/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold text-foreground mb-6">How it works</h2>
              <div className="space-y-8">
                <div className="flex gap-4">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold">1</div>
                  <div>
                    <h3 className="text-xl font-bold text-foreground mb-2">Tell us about your child</h3>
                    <p className="text-muted-foreground">Answer 3 simple questions about age and diagnosis status to get started.</p>
                  </div>
                </div>
                <div className="flex gap-4">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold">2</div>
                  <div>
                    <h3 className="text-xl font-bold text-foreground mb-2">Get your personalized map</h3>
                    <p className="text-muted-foreground">We'll recommend the right stage for you, from "Early Signs" to "School Readiness".</p>
                  </div>
                </div>
                <div className="flex gap-4">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center font-bold">3</div>
                  <div>
                    <h3 className="text-xl font-bold text-foreground mb-2">Take small steps</h3>
                    <p className="text-muted-foreground">Follow simple checklists and plain-English guides at your own pace.</p>
                  </div>
                </div>
              </div>
              <div className="mt-10">
                <Button
                  className="bg-primary hover:bg-primary/90 text-primary-foreground"
                  onClick={handleStartJourney}
                >
                  Get Started Now
                </Button>
              </div>
            </div>
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-br from-primary/20 to-secondary/20 rounded-2xl transform rotate-3 opacity-50"></div>
              <div className="relative bg-card rounded-2xl shadow-xl p-8 border border-border">
                {loading ? (
                  <div className="flex items-center justify-center h-64">
                    <Loader2 className="h-8 w-8 animate-spin text-primary" />
                  </div>
                ) : user && recommendedStage ? (
                  <div className="space-y-4">
                    <div className="flex items-center gap-2 mb-4">
                      <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                        <CheckCircle2 className="text-primary h-5 w-5" />
                      </div>
                      <div>
                        <h3 className="font-bold text-foreground">Your Journey</h3>
                        <p className="text-sm text-muted-foreground">{recommendedStage.title}</p>
                      </div>
                    </div>
                    
                    <div className="bg-accent/30 rounded-lg p-4 border border-border">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-foreground">Progress</span>
                        <span className="text-sm font-medium text-primary">
                          {progress ? `${progress.total_completed}/${progress.total_milestones}` : '0/0'}
                        </span>
                      </div>
                      <div className="w-full bg-accent rounded-full h-2">
                        <div
                          className="bg-primary h-2 rounded-full transition-all duration-500"
                          style={{
                            width: progress && progress.total_milestones > 0
                              ? `${(progress.total_completed / progress.total_milestones) * 100}%`
                              : '0%'
                          }}
                        ></div>
                      </div>
                    </div>

                    <div className="space-y-2 mt-4">
                      <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-3">
                        Current Milestones
                      </p>
                      {MILESTONES
                        .filter(m => m.stageId === recommendedStage.id)
                        .slice(0, 3)
                        .map((milestone) => {
                          const isCompleted = progress?.completed_milestone_ids?.includes(milestone.id);
                          return (
                            <div key={milestone.id} className="flex items-center gap-3 group">
                              <div className={cn(
                                "w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0 transition-colors",
                                isCompleted
                                  ? "bg-primary text-primary-foreground"
                                  : "border-2 border-border bg-background"
                              )}>
                                {isCompleted && <CheckCircle2 size={14} />}
                              </div>
                              <div className={cn(
                                "text-sm transition-colors",
                                isCompleted
                                  ? "text-muted-foreground line-through"
                                  : "text-foreground group-hover:text-primary"
                              )}>
                                {milestone.title}
                              </div>
                            </div>
                          );
                        })}
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="h-4 bg-accent rounded w-3/4"></div>
                    <div className="h-4 bg-accent rounded w-1/2"></div>
                    <div className="h-32 bg-accent/50 rounded-xl border border-border p-4 flex items-center justify-center">
                      <span className="text-primary font-medium">Journey Preview</span>
                    </div>
                    <div className="space-y-2">
                      <div className="flex items-center gap-3">
                        <div className="w-5 h-5 rounded-full bg-secondary/20 text-secondary flex items-center justify-center">
                          <CheckCircle2 size={12} />
                        </div>
                        <div className="h-3 bg-accent rounded w-full"></div>
                      </div>
                      <div className="flex items-center gap-3">
                        <div className="w-5 h-5 rounded-full bg-secondary/20 text-secondary flex items-center justify-center">
                          <CheckCircle2 size={12} />
                        </div>
                        <div className="h-3 bg-accent rounded w-5/6"></div>
                      </div>
                      <div className="flex items-center gap-3">
                        <div className="w-5 h-5 rounded-full border border-border"></div>
                        <div className="h-3 bg-accent rounded w-4/5"></div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary text-primary-foreground">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">You don't have to do this alone.</h2>
          <p className="text-xl text-primary-foreground/90 mb-10">
            Join thousands of parents finding their way forward, one step at a time.
          </p>
          {!user && (
            <Link href="/register">
              <Button size="lg" className="bg-card text-primary hover:bg-accent text-lg px-8 py-6 shadow-xl">
                Create Free Account
              </Button>
            </Link>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-foreground text-background/60 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="col-span-1 md:col-span-2">
              <span className="text-background font-bold text-xl block mb-4">Pathways for Parents</span>
              <p className="max-w-xs">
                Empowering parents of young children navigating autism with clear, actionable guidance.
              </p>
            </div>
            <div>
              <h4 className="text-background font-bold mb-4">Platform</h4>
              <ul className="space-y-2">
                <li><Link href="/journey" className="hover:text-background">Journey</Link></li>
                <li><Link href="/resources" className="hover:text-background">Resources</Link></li>
                {user ? (
                  <li>
                    <button onClick={handleLogout} className="hover:text-background text-left">
                      Log Out
                    </button>
                  </li>
                ) : (
                  <li><Link href="/login" className="hover:text-background">Login</Link></li>
                )}
              </ul>
            </div>
            <div>
              <h4 className="text-background font-bold mb-4">Support</h4>
              <ul className="space-y-2">
                <li><Link href="/about" className="hover:text-background">About Us</Link></li>
                <li><Link href="/contact" className="hover:text-background">Contact</Link></li>
                <li><Link href="/privacy" className="hover:text-background">Privacy Policy</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-background/20 mt-12 pt-8 text-sm text-center">
            &copy; {new Date().getFullYear()} Pathways for Parents. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
