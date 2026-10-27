// Netlify Function for SkillGate
// Deploy: netlify deploy

import { scanCode } from "./skillgate";

export default async (req, res) => {
  // CORS
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { code, language } = req.body;

  if (!code) {
    return res.status(400).json({ error: "Missing code parameter" });
  }

  try {
    const result = scanCode(code, language || "python");
    return res.status(200).json(result);
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
};
