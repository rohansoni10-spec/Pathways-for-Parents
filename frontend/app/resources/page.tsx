"use client";

import React, { useState, useMemo } from 'react';
import { RESOURCES, Resource } from '@/lib/data';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Search, ExternalLink, Filter, X } from 'lucide-react';
import { cn } from '@/lib/utils';

const CATEGORIES = ['All', 'Early Intervention', 'Diagnosis', 'Insurance', 'IEP', 'Therapy', 'General'];

export default function ResourcesPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');

  const filteredResources = useMemo(() => {
    return RESOURCES.filter(resource => {
      const matchesSearch = resource.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
                            resource.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                            resource.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()));
      
      const matchesCategory = selectedCategory === 'All' || resource.category === selectedCategory;

      return matchesSearch && matchesCategory;
    });
  }, [searchQuery, selectedCategory]);

  return (
    <div className="min-h-screen bg-slate-50 pb-20">
      {/* Header */}
      <div className="bg-white border-b border-slate-200 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto text-center">
          <h1 className="text-3xl font-bold text-slate-900 mb-4">Resource Library</h1>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Curated, trustworthy guides and tools to help you navigate every step of the journey.
          </p>
        </div>
      </div>

      {/* Search and Filter */}
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 -mt-8">
        <Card className="shadow-lg border-0">
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={18} />
                <Input 
                  placeholder="Search resources..." 
                  className="pl-10"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
              <div className="flex gap-2 overflow-x-auto pb-2 md:pb-0 no-scrollbar">
                {CATEGORIES.map(category => (
                  <Button
                    key={category}
                    variant={selectedCategory === category ? "default" : "outline"}
                    onClick={() => setSelectedCategory(category)}
                    className="whitespace-nowrap"
                    size="sm"
                  >
                    {category}
                  </Button>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Results */}
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {filteredResources.length > 0 ? (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {filteredResources.map((resource) => (
              <a 
                key={resource.id} 
                href={resource.url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="block group h-full"
              >
                <Card className="h-full hover:shadow-md transition-all duration-300 hover:-translate-y-1 border-slate-200 group-hover:border-sky-200">
                  <CardHeader>
                    <div className="flex justify-between items-start mb-2">
                      <Badge variant="secondary" className="bg-slate-100 text-slate-600 hover:bg-slate-200">
                        {resource.category}
                      </Badge>
                      <ExternalLink size={16} className="text-slate-400 group-hover:text-sky-500" />
                    </div>
                    <CardTitle className="text-lg group-hover:text-sky-700 transition-colors">
                      {resource.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="text-base mb-4">
                      {resource.description}
                    </CardDescription>
                    <div className="flex flex-wrap gap-2 mt-auto">
                      {resource.tags.map(tag => (
                        <span key={tag} className="text-xs text-slate-400 bg-slate-50 px-2 py-1 rounded-md">
                          #{tag}
                        </span>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </a>
            ))}
          </div>
        ) : (
          <div className="text-center py-20">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-slate-100 mb-4">
              <Search className="text-slate-400" size={32} />
            </div>
            <h3 className="text-lg font-medium text-slate-900">No resources found</h3>
            <p className="text-slate-500 mt-2">Try adjusting your search or filters.</p>
            <Button 
              variant="link" 
              onClick={() => { setSearchQuery(''); setSelectedCategory('All'); }}
              className="mt-4"
            >
              Clear all filters
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
