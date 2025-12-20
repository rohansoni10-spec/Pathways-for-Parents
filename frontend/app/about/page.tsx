"use client";

import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Users, Heart, ShieldCheck } from 'lucide-react';

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-background pb-20">
      {/* Header */}
      <div className="bg-card border-b border-border py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl font-bold text-foreground mb-4">About Pathways for Parents</h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Empowering families to navigate the autism journey with confidence, clarity, and compassion.
          </p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-16">
        {/* Mission Section */}
        <section>
          <h2 className="text-3xl font-bold text-foreground mb-6">Our Mission</h2>
          <div className="prose prose-lg text-muted-foreground">
            <p>
              At Pathways for Parents, we believe that every parent deserves a clear roadmap. The journey of raising a child with autism can feel overwhelming, filled with complex medical terms, endless paperwork, and emotional highs and lows.
            </p>
            <p className="mt-4">
              Our mission is to cut through the noise. We provide a structured, step-by-step guide that helps you focus on what matters most right now—your child's growth and your own well-being. We are here to replace anxiety with action and isolation with community.
            </p>
          </div>
        </section>

        {/* Values Section */}
        <section>
          <h2 className="text-3xl font-bold text-foreground mb-8">Our Core Values</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <Card className="bg-accent/30 border-border">
              <CardContent className="p-6 text-center">
                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Heart className="text-primary h-6 w-6" />
                </div>
                <h3 className="text-xl font-semibold text-foreground mb-2">Empathy First</h3>
                <p className="text-muted-foreground">
                  We understand the emotional weight of this journey because we've been there.
                </p>
              </CardContent>
            </Card>
            <Card className="bg-accent/30 border-border">
              <CardContent className="p-6 text-center">
                <div className="w-12 h-12 bg-secondary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <ShieldCheck className="text-secondary h-6 w-6" />
                </div>
                <h3 className="text-xl font-semibold text-foreground mb-2">Trust & Clarity</h3>
                <p className="text-muted-foreground">
                  We provide vetted, evidence-based information free from jargon and fear.
                </p>
              </CardContent>
            </Card>
            <Card className="bg-accent/30 border-border">
              <CardContent className="p-6 text-center">
                <div className="w-12 h-12 bg-destructive/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Users className="text-destructive h-6 w-6" />
                </div>
                <h3 className="text-xl font-semibold text-foreground mb-2">Community</h3>
                <p className="text-muted-foreground">
                  No one should have to navigate this path alone. We build bridges between families.
                </p>
              </CardContent>
            </Card>
          </div>
        </section>

        {/* Team Section */}
        <section>
          <h2 className="text-3xl font-bold text-foreground mb-8">Meet the Team</h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div className="flex items-start space-x-4">
              <div className="w-20 h-20 rounded-full bg-slate-200 flex-shrink-0"></div>
              <div>
                <h3 className="text-xl font-bold text-foreground">Sarah Jenkins</h3>
                <p className="text-primary font-medium mb-2">Founder & CEO</p>
                <p className="text-muted-foreground text-sm">
                  Mom of two, including a son on the spectrum. Built Pathways after struggling to find clear answers during her own diagnosis journey.
                </p>
              </div>
            </div>
            <div className="flex items-start space-x-4">
              <div className="w-20 h-20 rounded-full bg-slate-200 flex-shrink-0"></div>
              <div>
                <h3 className="text-xl font-bold text-foreground">Dr. Marcus Chen</h3>
                <p className="text-primary font-medium mb-2">Clinical Advisor</p>
                <p className="text-muted-foreground text-sm">
                  Developmental Pediatrician with 15 years of experience helping families navigate early intervention and school support systems.
                </p>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
