import { test, expect } from '@playwright/test';

test.describe('Content Personalization', () => {
  test('should display personalized chapter content based on learning style', async ({ page }) => {
    // Navigate to a chapter page
    await page.goto('http://localhost:3000/docs/introduction-to-physical-ai');

    // In a real scenario, user preferences would be set via a UI or API call before this test.
    // For this E2E test, we are relying on the mockUserId and isPersonalizationEnabled flag
    // within frontend/src/theme/DocItem/Content/index.js, which are hardcoded for demonstration.

    // The personalization logic in `DocItem/Content/index.js` currently checks for
    // `mockUserId` and `isPersonalizationEnabled` to be true.
    // And it uses a simplified logic to prepend text based on a hardcoded learning style.

    // We expect the content to be personalized for a "visual" learner based on the mock in backend/src/services/personalization_service.py
    // and the mockUserId in frontend/src/theme/DocItem/Content/index.js

    await expect(page.locator('.markdown')).toContainText('[Personalized for Visual Learner]');
    await expect(page.locator('.markdown')).toContainText('Consider looking for diagrams and charts related to this content.');

    // We should also ensure the original content is still present after the personalization prefix
    await expect(page.locator('.markdown')).toContainText('Introduction to Physical AI');
    await expect(page.locator('.markdown')).toContainText('This chapter introduces the fundamental concepts of Physical AI');
  });
});