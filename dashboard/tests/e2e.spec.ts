import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  await page.goto('http://localhost:3000');

  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle(/TDC Agent Platform/);
});

test('can switch tabs', async ({ page }) => {
  await page.goto('http://localhost:3000');

  // Click the Task Board button.
  await page.getByRole('button', { name: 'Task Board' }).click();

  // Expects the header "TODO" to be visible
  await expect(page.getByRole('heading', { name: 'TODO' })).toBeVisible();
});
