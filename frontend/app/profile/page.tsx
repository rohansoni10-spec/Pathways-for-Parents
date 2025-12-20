"use client";

import React from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { User, LogOut, Trash2, RefreshCw } from 'lucide-react';
import toast from 'react-hot-toast';

export default function ProfilePage() {
  const { user, logout, updateUser } = useAuth();
  const router = useRouter();

  if (!user) {
    router.push('/login');
    return null;
  }

  const handleLogout = () => {
    logout();
    router.push('/');
    toast.success('Logged out successfully');
  };

  const handleResetProgress = () => {
    if (confirm('Are you sure you want to reset all your progress? This cannot be undone.')) {
      updateUser({ completedMilestones: [] });
      toast.success('Progress reset');
    }
  };

  const handleRetakeOnboarding = () => {
    router.push('/onboarding');
  };

  return (
    <div className="min-h-screen bg-slate-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold text-slate-900 mb-8">Your Profile</h1>

        <div className="space-y-6">
          {/* User Info Card */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <User className="text-sky-500" />
                Account Details
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium text-slate-500">Name</label>
                <p className="text-lg font-medium text-slate-900">{user.name || 'Parent'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-slate-500">Email</label>
                <p className="text-lg font-medium text-slate-900">{user.email}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-slate-500">Milestones Completed</label>
                <p className="text-lg font-medium text-slate-900">{user.completedMilestones.length}</p>
              </div>
            </CardContent>
          </Card>

          {/* Actions Card */}
          <Card>
            <CardHeader>
              <CardTitle>Settings & Actions</CardTitle>
              <CardDescription>Manage your journey settings</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex flex-col sm:flex-row gap-4">
                <Button variant="outline" onClick={handleRetakeOnboarding} className="flex-1 justify-start">
                  <RefreshCw className="mr-2 h-4 w-4" />
                  Retake Onboarding Questionnaire
                </Button>
                <Button variant="outline" onClick={handleResetProgress} className="flex-1 justify-start text-red-600 hover:text-red-700 hover:bg-red-50">
                  <Trash2 className="mr-2 h-4 w-4" />
                  Reset Progress
                </Button>
              </div>
              
              <div className="pt-4 border-t border-slate-100">
                <Button variant="destructive" onClick={handleLogout} className="w-full sm:w-auto">
                  <LogOut className="mr-2 h-4 w-4" />
                  Log Out
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
