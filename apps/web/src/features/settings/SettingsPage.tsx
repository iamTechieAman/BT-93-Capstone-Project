import React, { useState } from 'react';
import { Moon, Sun } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';

export function SettingsPage() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const [threshold, setThreshold] = useState('75.0');
  const [gspKey, setGspKey] = useState('••••••••••••••••••••••••');

  const toggleTheme = (newTheme: 'light' | 'dark') => {
    setTheme(newTheme);
    if (newTheme === 'dark') {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-xl font-semibold text-[var(--text-main)]">
          System Configuration & Preferences
        </h1>
        <p className="text-sm text-[var(--text-muted)]">
          Manage compliance confidence thresholds, appearance, live GSP credentials, and security
          controls.
        </p>
      </div>

      {/* Appearance Card */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm">Appearance & Theme</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between text-xs">
            <div>
              <span className="font-semibold text-[var(--text-main)] block">Interface Theme</span>
              <span className="text-[var(--text-muted)]">
                Choose between mature finance SaaS Light mode or Dark mode.
              </span>
            </div>

            <div className="flex items-center gap-2">
              <Button
                variant={theme === 'light' ? 'primary' : 'secondary'}
                size="sm"
                onClick={() => toggleTheme('light')}
              >
                <Sun className="mr-1.5 h-3.5 w-3.5" /> Light
              </Button>
              <Button
                variant={theme === 'dark' ? 'primary' : 'secondary'}
                size="sm"
                onClick={() => toggleTheme('dark')}
              >
                <Moon className="mr-1.5 h-3.5 w-3.5" /> Dark
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Classification Engine Governance */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm">AI Classification Governance</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-xs">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <span className="font-semibold text-[var(--text-main)] block">
                Confidence Review Threshold
              </span>
              <span className="text-[var(--text-muted)]">
                Classifications scoring below this threshold (0-100) are flagged as "Needs review".
              </span>
            </div>

            <div className="flex items-center gap-2">
              <Input
                type="number"
                min="0"
                max="100"
                step="0.5"
                value={threshold}
                onChange={(e) => setThreshold(e.target.value)}
                className="w-24 text-center font-mono"
              />
              <span className="font-mono text-[var(--text-muted)]">%</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Live GSP Provider Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm">GST Portal & GSP API Provider</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-xs">
          <div>
            <span className="font-semibold text-[var(--text-main)] block">
              Licensed GSP API Secret
            </span>
            <span className="text-[var(--text-muted)]">
              When configured, enables live registry taxpayer verification and active status
              retrieval.
            </span>
          </div>

          <div className="flex gap-2">
            <Input
              type="password"
              value={gspKey}
              onChange={(e) => setGspKey(e.target.value)}
              className="font-mono"
              placeholder="Enter GSP API Key..."
            />
            <Button variant="secondary" size="sm">
              Save Key
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
