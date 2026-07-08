/**
 * Vercel Speed Insights Integration
 * This script initializes Speed Insights for the VibeSafe static site
 */

import { injectSpeedInsights } from '@vercel/speed-insights';

// Initialize Speed Insights when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initSpeedInsights);
} else {
  initSpeedInsights();
}

function initSpeedInsights() {
  // Initialize Speed Insights
  // Debug mode is automatically enabled in development
  injectSpeedInsights({
    // Route tracking is handled automatically for static pages
    // beforeSend can be used to filter or modify events if needed
  });
}
