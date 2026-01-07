'use client';

import { ProtectedRoute } from '@/components/auth';
import { DashboardLayout } from '@/components/layout';
import { Card, CardHeader, CardContent } from '@/components/ui';
import { Alert } from '@/components/ui';

function SettingsContent() {
  return (
    <DashboardLayout>
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Settings</h1>

        <div className="space-y-6">
          <Card padding={false}>
            <CardHeader>
              <h2 className="text-xl font-semibold text-gray-900">Account Settings</h2>
            </CardHeader>
            <CardContent>
              <Alert variant="info">
                Advanced settings will be available in Phase 5
              </Alert>
            </CardContent>
          </Card>

          <Card padding={false}>
            <CardHeader>
              <h2 className="text-xl font-semibold text-gray-900">Reading Preferences</h2>
            </CardHeader>
            <CardContent>
              <Alert variant="info">
                Reading preferences (font size, theme, etc.) will be available in Phase 4.5
              </Alert>
            </CardContent>
          </Card>

          <Card padding={false}>
            <CardHeader>
              <h2 className="text-xl font-semibold text-gray-900">Notification Settings</h2>
            </CardHeader>
            <CardContent>
              <Alert variant="info">
                Notification settings will be available in Phase 5.3
              </Alert>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}

export default function SettingsPage() {
  return (
    <ProtectedRoute>
      <SettingsContent />
    </ProtectedRoute>
  );
}

