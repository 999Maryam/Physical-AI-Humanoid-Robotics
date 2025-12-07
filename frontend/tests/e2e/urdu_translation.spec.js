import { test, expect } from '@playwright/test';

test.describe('Urdu Translation', () => {
  test('should display chapter content in Urdu when selected', async ({ page }) => {
    await page.goto('http://localhost:3000/docs/introduction-to-physical-ai');

    // Check if LanguageSwitcher is present
    const languageSwitcher = page.locator('.language-switcher'); // Assuming a class name or similar locator
    await expect(languageSwitcher).toBeVisible();

    // Click on Urdu language option
    await page.getByRole('link', { name: 'UR' }).click();

    // Expect the URL to reflect the Urdu locale
    await expect(page).toHaveURL(/.*\/ur\/introduction-to-physical-ai/);

    // Expect translated content to be visible
    // This relies on the mock translation service prepending "Translated (ur): "
    await expect(page.locator('.markdown')).toContainText('Translated (ur): Introduction to Physical AI');
    await expect(page.locator('.markdown')).toContainText('Translated (ur): This chapter introduces the fundamental concepts of Physical AI');
  });
});