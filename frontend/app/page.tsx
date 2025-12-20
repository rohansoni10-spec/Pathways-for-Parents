"use client";

import React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ArrowRight, CheckCircle2, ShieldCheck, Heart, Users } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-sky-50 via-white to-emerald-50 pt-20 pb-32 overflow-hidden">
        <div className="absolute top-0 right-0 -mr-20 -mt-20 w-96 h-96 bg-sky-100 rounded-full blur-3xl opacity-50"></div>
        <div className="absolute bottom-0 left-0 -ml-20 -mb-20 w-96 h-96 bg-emerald-100 rounded-full blur-3xl opacity-50"></div>
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="text-center max-w-3xl mx-auto">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-white border border-slate-200 shadow-sm mb-8">
              <span className="flex h-2 w-2 rounded-full bg-emerald-500 mr-2"></span>
              <span className="text-sm font-medium text-slate-600">A guided roadmap for parents</span>
            </div>
            <h1 className="text-5xl md:text-6xl font-bold text-slate-900 tracking-tight mb-6 leading-tight">
              Navigate the autism journey with <span className="text-transparent bg-clip-text bg-gradient-to-r from-sky-600 to-emerald-600">confidence</span>.
            </h1>
            <p className="text-xl text-slate-600 mb-10 leading-relaxed">
              Stop drowning in information. Get a personalized, step-by-step roadmap that shows you exactly what matters right now for your child.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/onboarding">
                <Button size="lg" className="w-full sm:w-auto text-lg px-8 py-6 bg-sky-600 hover:bg-sky-700 shadow-lg shadow-sky-200">
                  Start My Journey
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/resources">
                <Button variant="outline" size="lg" className="w-full sm:w-auto text-lg px-8 py-6 bg-white/80 backdrop-blur-sm">
                  Browse Resources
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-slate-900 mb-4">Why parents trust Pathways</h2>
            <p className="text-lg text-slate-600 max-w-2xl mx-auto">
              We turn a complex, overwhelming process into manageable steps.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-slate-50 rounded-2xl p-8 border border-slate-100 hover:shadow-lg transition-shadow">
              <div className="w-12 h-12 bg-sky-100 rounded-xl flex items-center justify-center mb-6">
                <ShieldCheck className="text-sky-600 h-6 w-6" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Trustworthy Guidance</h3>
              <p className="text-slate-600">
                Curated by experts and experienced parents. No jargon, no fear-mongering—just clear, actionable advice.
              </p>
            </div>
            <div className="bg-slate-50 rounded-2xl p-8 border border-slate-100 hover:shadow-lg transition-shadow">
              <div className="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center mb-6">
                <CheckCircle2 className="text-emerald-600 h-6 w-6" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Actionable Milestones</h3>
              <p className="text-slate-600">
                Break down big goals into small, achievable wins. Track your progress and celebrate every step forward.
              </p>
            </div>
            <div className="bg-slate-50 rounded-2xl p-8 border border-slate-100 hover:shadow-lg transition-shadow">
              <div className="w-12 h-12 bg-rose-100 rounded-xl flex items-center justify-center mb-6">
                <Heart className="text-rose-600 h-6 w-6" />
              </div>
              <h3 className="text-xl font-bold text-slate-900 mb-3">Emotional Support</h3>
              <p className="text-slate-600">
                We focus on you as much as your child. Find reassurance, community resources, and self-care reminders.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How it Works */}
      <section className="py-24 bg-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold text-slate-900 mb-6">How it works</h2>
              <div className="space-y-8">
                <div className="flex gap-4">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-sky-600 text-white flex items-center justify-center font-bold">1</div>
                  <div>
                    <h3 className="text-xl font-bold text-slate-900 mb-2">Tell us about your child</h3>
                    <p className="text-slate-600">Answer 3 simple questions about age and diagnosis status to get started.</p>
                  </div>
                </div>
                <div className="flex gap-4">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-sky-600 text-white flex items-center justify-center font-bold">2</div>
                  <div>
                    <h3 className="text-xl font-bold text-slate-900 mb-2">Get your personalized map</h3>
                    <p className="text-slate-600">We'll recommend the right stage for you, from "Early Signs" to "School Readiness".</p>
                  </div>
                </div>
                <div className="flex gap-4">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-sky-600 text-white flex items-center justify-center font-bold">3</div>
                  <div>
                    <h3 className="text-xl font-bold text-slate-900 mb-2">Take small steps</h3>
                    <p className="text-slate-600">Follow simple checklists and plain-English guides at your own pace.</p>
                  </div>
                </div>
              </div>
              <div className="mt-10">
                <Link href="/onboarding">
                  <Button className="bg-sky-600 hover:bg-sky-700">Get Started Now</Button>
                </Link>
              </div>
            </div>
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-br from-sky-200 to-emerald-200 rounded-2xl transform rotate-3 opacity-50"></div>
              <div className="relative bg-white rounded-2xl shadow-xl p-8 border border-slate-100">
                <div className="space-y-4">
                  <div className="h-4 bg-slate-100 rounded w-3/4"></div>
                  <div className="h-4 bg-slate-100 rounded w-1/2"></div>
                  <div className="h-32 bg-sky-50 rounded-xl border border-sky-100 p-4 flex items-center justify-center">
                    <span className="text-sky-600 font-medium">Your Personalized Roadmap</span>
                  </div>
                  <div className="space-y-2">
                    <div className="flex items-center gap-3">
                      <div className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center">
                        <CheckCircle2 size={12} />
                      </div>
                      <div className="h-3 bg-slate-100 rounded w-full"></div>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center">
                        <CheckCircle2 size={12} />
                      </div>
                      <div className="h-3 bg-slate-100 rounded w-5/6"></div>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="w-5 h-5 rounded-full border border-slate-300"></div>
                      <div className="h-3 bg-slate-100 rounded w-4/5"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-sky-600 text-white">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">You don't have to do this alone.</h2>
          <p className="text-xl text-sky-100 mb-10">
            Join thousands of parents finding their way forward, one step at a time.
          </p>
          <Link href="/register">
            <Button size="lg" className="bg-white text-sky-600 hover:bg-sky-50 text-lg px-8 py-6 shadow-xl">
              Create Free Account
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-400 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="col-span-1 md:col-span-2">
              <span className="text-white font-bold text-xl block mb-4">Pathways</span>
              <p className="max-w-xs">
                Empowering parents of young children navigating autism with clear, actionable guidance.
              </p>
            </div>
            <div>
              <h4 className="text-white font-bold mb-4">Platform</h4>
              <ul className="space-y-2">
                <li><Link href="/journey" className="hover:text-white">Journey</Link></li>
                <li><Link href="/resources" className="hover:text-white">Resources</Link></li>
                <li><Link href="/login" className="hover:text-white">Login</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-bold mb-4">Support</h4>
              <ul className="space-y-2">
                <li><Link href="#" className="hover:text-white">About Us</Link></li>
                <li><Link href="#" className="hover:text-white">Contact</Link></li>
                <li><Link href="#" className="hover:text-white">Privacy Policy</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-slate-800 mt-12 pt-8 text-sm text-center">
            &copy; {new Date().getFullYear()} Pathways for Parents. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
