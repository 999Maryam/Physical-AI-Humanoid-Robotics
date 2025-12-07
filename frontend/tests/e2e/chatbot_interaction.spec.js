import { test, expect } from '@playwright/test';

test.describe('Chatbot Interaction', () => {
  test('should send a query and receive a response', async ({ page }) => {
    await page.goto('http://localhost:3000/'); // Assuming chatbot is on the homepage or accessible from it

    // Find the chatbot input and type a message
    const chatInput = page.getByPlaceholder('Ask a question...');
    await expect(chatInput).toBeVisible();
    await chatInput.fill('What is Physical AI?');

    // Click the send button
    await page.getByRole('button', { name: 'Send' }).click();

    // Expect to see the user's message and a bot response
    await expect(page.getByText('What is Physical AI?')).toBeVisible();
    // The mock response in Chatbot.jsx is "Echo: [user_input]"
    await expect(page.getByText('Physical AI integrates AI with physical systems.')).toBeVisible();
  });
});
