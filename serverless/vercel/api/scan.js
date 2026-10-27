// Vercel Serverless Function for SkillGate
// Deploy: vercel deploy

import { skillgateScan } from "./lib/skillgate";

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { code, language } = req.body;

  if (!code) {
    return res.status(400).json({ error: "Missing code parameter" });
  }

  try {
    const result = await skillgateScan(code, language || "python");
    return res.status(200).json(result);
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}
