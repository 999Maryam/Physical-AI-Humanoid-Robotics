import { test, expect } from '@playwright/test';

test.describe('Chapter Navigation', () => {
  test('should navigate through all main chapters', async ({ page }) => {
    await page.goto('http://localhost:3000/');

    const chapters = [
      'Introduction to Physical AI',
      'Basics of Humanoid Robotics',
      'ROS 2 Fundamentals',
      'Digital Twin Simulation (Gazebo + Isaac)',
      'Vision-Language-Action Systems',
      'Capstone',
    ];

    for (const chapterTitle of chapters) {
      // Click on the sidebar link for the chapter
      await page.getByRole('link', { name: chapterTitle }).click();
      // Expect the chapter title to be visible on the page
      await expect(page.getByRole('heading', { name: chapterTitle })).toBeVisible();
      // Add a small wait to visually see the navigation (optional)
      await page.waitForTimeout(500);
    }
  });
});
