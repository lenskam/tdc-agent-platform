import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Login - TDC Agent Platform",
  description: "Sign in to your account",
};

export default function LoginLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
