"use client";

import React from 'react';
import { Card, CardContent } from '@/components/ui/card';

export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-background pb-20">
      {/* Header */}
      <div className="bg-card border-b border-border py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold text-foreground mb-4">Privacy Policy</h1>
          <p className="text-muted-foreground">
            Last Updated: October 24, 2023
          </p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <Card className="border-border bg-card">
          <CardContent className="p-8 prose prose-slate max-w-none text-muted-foreground">
            <p className="lead text-lg text-foreground font-medium mb-6">
              At Pathways for Parents, we take your privacy seriously. We understand that the information you share about your family and your child's development is sensitive, and we are committed to protecting it.
            </p>

            <h3 className="text-xl font-bold text-foreground mt-8 mb-4">1. Information We Collect</h3>
            <p>
              We collect information you provide directly to us, such as when you create an account, complete the onboarding questionnaire, or contact us for support. This may include:
            </p>
            <ul className="list-disc pl-6 space-y-2 mt-2 mb-4">
              <li>Name and email address</li>
              <li>Child's age range and diagnosis status (for personalization purposes only)</li>
              <li>Progress data on milestones you check off</li>
            </ul>

            <h3 className="text-xl font-bold text-foreground mt-8 mb-4">2. How We Use Your Information</h3>
            <p>
              We use the information we collect to:
            </p>
            <ul className="list-disc pl-6 space-y-2 mt-2 mb-4">
              <li>Provide, maintain, and improve our services</li>
              <li>Personalize your journey roadmap and recommendations</li>
              <li>Send you technical notices, updates, and support messages</li>
              <li>Monitor and analyze trends and usage</li>
            </ul>

            <h3 className="text-xl font-bold text-foreground mt-8 mb-4">3. Data Security</h3>
            <p>
              We implement appropriate technical and organizational measures to protect your personal data against unauthorized access, alteration, disclosure, or destruction. However, no internet transmission is completely secure, and we cannot guarantee absolute security.
            </p>

            <h3 className="text-xl font-bold text-foreground mt-8 mb-4">4. Sharing of Information</h3>
            <p>
              We do not sell your personal information. We may share your information with third-party vendors and service providers who perform services on our behalf, such as email delivery and hosting services, but only to the extent necessary for them to perform those services.
            </p>

            <h3 className="text-xl font-bold text-foreground mt-8 mb-4">5. Your Rights</h3>
            <p>
              You have the right to access, correct, or delete your personal information at any time. You can manage your profile settings directly within the application or contact us at privacy@pathwaysforparents.com for assistance.
            </p>

            <h3 className="text-xl font-bold text-foreground mt-8 mb-4">6. Contact Us</h3>
            <p>
              If you have any questions about this Privacy Policy, please contact us at:
            </p>
            <p className="mt-2">
              <strong>Pathways for Parents</strong><br />
              123 Wellness Way, Suite 400<br />
              San Francisco, CA 94103<br />
              Email: privacy@pathwaysforparents.com
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
