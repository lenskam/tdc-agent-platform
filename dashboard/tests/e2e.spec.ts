import { test, expect } from "@playwright/test";

test.describe("TDC Agent Platform E2E", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("http://localhost:3000");
  });

  test("has title", async ({ page }) => {
    await expect(page).toHaveTitle(/TDC Agent Platform/);
  });

  test("can switch tabs", async ({ page }) => {
    await page.getByRole("button", { name: "Task Board" }).click();
    await expect(page.getByRole("heading", { name: "TODO" })).toBeVisible();
  });

  test("can send project planning message and receive response", async ({
    page,
  }) => {
    const input = page.getByPlaceholder("Describe your project...");
    await input.fill("Migrate DHIS2 to Cloud");

    const sendButton = page.getByRole("button", { name: "" }).last();
    await sendButton.click();

    await expect(page.getByText("Migrate DHIS2 to Cloud")).toBeVisible();

    await expect(page.getByText("Thinking...")).toBeVisible();

    await expect(page.getByText(/I have received your request/)).toBeVisible({
      timeout: 5000,
    });
  });

  test("can plan project and view tasks in board", async ({ page }) => {
    await page
      .getByPlaceholder("Describe your project...")
      .fill("Build a data analytics dashboard");
    await page.getByRole("button", { name: "" }).last().click();

    await expect(page.getByText("Thinking...")).toBeVisible();
    await expect(page.getByText(/I have received your request/)).toBeVisible({
      timeout: 5000,
    });

    await page.getByRole("button", { name: "Task Board" }).click();

    await expect(page.getByRole("heading", { name: "TODO" })).toBeVisible();
  });
});
