"use client";

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Mail, MapPin, Phone } from 'lucide-react';
import toast from 'react-hot-toast';

export default function ContactPage() {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate form submission
    setTimeout(() => {
      toast.success("Message sent! We'll get back to you soon.");
      setIsSubmitting(false);
      // Reset form logic would go here
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-background pb-20">
      {/* Header */}
      <div className="bg-card border-b border-border py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl font-bold text-foreground mb-4">Contact Us</h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Have questions or feedback? We're here to help you on your journey.
          </p>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid md:grid-cols-2 gap-12">
          
          {/* Contact Information */}
          <div className="space-y-8">
            <div>
              <h2 className="text-2xl font-bold text-foreground mb-4">Get in Touch</h2>
              <p className="text-muted-foreground mb-6">
                Whether you're a parent needing support, a professional wanting to collaborate, or just have a suggestion for our platform, we'd love to hear from you.
              </p>
            </div>

            <div className="space-y-6">
              <Card className="border-border bg-card">
                <CardContent className="p-6 flex items-start space-x-4">
                  <Mail className="text-primary h-6 w-6 mt-1" />
                  <div>
                    <h3 className="font-semibold text-foreground">Email Us</h3>
                    <p className="text-muted-foreground text-sm mb-1">For general inquiries and support:</p>
                    <a href="mailto:hello@pathwaysforparents.com" className="text-primary hover:underline">hello@pathwaysforparents.com</a>
                  </div>
                </CardContent>
              </Card>

              <Card className="border-border bg-card">
                <CardContent className="p-6 flex items-start space-x-4">
                  <Phone className="text-primary h-6 w-6 mt-1" />
                  <div>
                    <h3 className="font-semibold text-foreground">Call Us</h3>
                    <p className="text-muted-foreground text-sm mb-1">Mon-Fri, 9am - 5pm EST:</p>
                    <a href="tel:+15551234567" className="text-primary hover:underline">(555) 123-4567</a>
                  </div>
                </CardContent>
              </Card>

              <Card className="border-border bg-card">
                <CardContent className="p-6 flex items-start space-x-4">
                  <MapPin className="text-primary h-6 w-6 mt-1" />
                  <div>
                    <h3 className="font-semibold text-foreground">Office</h3>
                    <p className="text-muted-foreground text-sm">
                      123 Wellness Way, Suite 400<br />
                      San Francisco, CA 94103
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Contact Form */}
          <div>
            <Card className="border-border shadow-lg">
              <CardHeader>
                <CardTitle>Send a Message</CardTitle>
                <CardDescription>Fill out the form below and we'll respond within 24 hours.</CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="firstName">First name</Label>
                      <Input id="firstName" placeholder="Jane" required />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="lastName">Last name</Label>
                      <Input id="lastName" placeholder="Doe" required />
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="email">Email</Label>
                    <Input id="email" type="email" placeholder="jane@example.com" required />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="subject">Subject</Label>
                    <Input id="subject" placeholder="How can we help?" required />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="message">Message</Label>
                    <textarea 
                      id="message" 
                      className="flex min-h-[120px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                      placeholder="Tell us more about your inquiry..."
                      required
                    ></textarea>
                  </div>

                  <Button type="submit" className="w-full" disabled={isSubmitting}>
                    {isSubmitting ? 'Sending...' : 'Send Message'}
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>

        </div>
      </div>
    </div>
  );
}
